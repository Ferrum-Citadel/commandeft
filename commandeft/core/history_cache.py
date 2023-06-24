import tiktoken


class HistoryCache:
    def __init__(self, model):
        self.cache = []
        self.model = model
        self.token_count = 0
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def append(self, message):
        self.cache.append(message)

    def prepend(self, message):
        self.cache.insert(0, message)

    def is_empty(self):
        return len(self.cache) == 0

    def total_tokens(self):
        return self.num_tokens_from_messages(self.cache)

    def clear(self):
        self.cache = []

    def get_cache(self):
        return self.cache

    # Taken from: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    def num_tokens_from_messages(self, messages):
        """Returns the number of tokens used by a list of messages."""

        if self.model == "gpt-3.5-turbo":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif self.model == "gpt-4":
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for self.model {self.model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(self.encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens
