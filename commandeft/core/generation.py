import sys
import re
import click
import openai


from commandeft.core.history_cache import HistoryCache
from commandeft.util.config_util import get_configuration

if get_configuration("model") == "gpt-4":
    from commandeft.constants.consts import GPT_4_MAX_TOKENS as MAX_TOKENS
else:
    from commandeft.constants.consts import GPT_3_5_MAX_TOKENS as MAX_TOKENS


class Generation:
    def __init__(self, config):
        self.__session_gen_count = 0
        self.__config = config
        self.__history_cache: HistoryCache = config.get("history_cache", HistoryCache(model=self.model))

        if self.mode == "interactive" and self.interactive_history:
            self.__set_keep_history(True)
        else:
            self.__set_keep_history(False)

    def __set_keep_history(self, value):
        self.__keep_history = value

    @property
    def mode(self):
        return self.__config.get("mode", "inline")

    @property
    def model(self):
        return self.__config.get("model")

    @property
    def current_os(self):
        return self.__config.get("current_os")

    @property
    def current_shell(self):
        return self.__config.get("current_shell")

    @property
    def temperature(self):
        return self.__config.get("temperature")

    @property
    def max_tokens(self):
        return self.__config.get("max_tokens")

    @property
    def interactive_history(self):
        return self.__config.get("interactive_history", False)

    def generate_command(self, user_prompt: str):
        system_message = {
            "role": "system",
            "content": f"""Assume the role of a shell scripting expert with the given specifications: Shell: {self.current_shell}, OS: {self.current_os}""",
        }

        user_message = {
            "role": "user",
            "content": f"""Provide only the raw command inside a code block that best fulfills the following request: {user_prompt}. Prefer oneliners. No other text is allowed.""",
        }

        if self.mode == "interactive":
            res = self.__generate_interactive_command(user_message, user_prompt, system_message)
        else:
            res = self.__generate_inline_command(user_message, system_message)

        try:
            command: str | None = self.__parse_code_block(res)
            return command
        except ValueError:
            click.echo(click.style(res.replace(". ", ".\n"), fg="red"))
            if self.mode == "inline":
                sys.exit(1)
            return None

    def __generate_interactive_command(self, user_message, user_prompt=None, system_message=None):
        self.__session_gen_count += 1

        if self.__keep_history:
            if self.__session_gen_count == 1:
                self.__history_cache.append(system_message)
                self.__history_cache.append(user_message)
            else:
                # Fom the second time history is used in a session,
                # shorten token use by including only user_prompt in history without further instructions
                short_user_message = {
                    "role": "user",
                    "content": user_prompt,
                }
                self.__history_cache.append(short_user_message)
            messages = self.__history_cache.get_cache()
        else:
            messages = [system_message, user_message]

        completion = self.__get_completion(messages)

        if not completion:
            return None

        if self.__keep_history:
            self.__history_cache.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion.choices[0].message.content

    def __generate_inline_command(self, user_message, system_message=None):
        messages = [system_message, user_message]
        completion = self.__get_completion(messages)

        if not completion:
            return None

        return completion.choices[0].message.content

    def __get_completion(self, messages):
        openai.api_key = get_configuration("api_key")

        if self.__keep_history:
            cur_total_tokens = self.__history_cache.size
            max_tokens = MAX_TOKENS - cur_total_tokens
        else:
            max_tokens = self.max_tokens + 130

        try:
            return openai.ChatCompletion.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=self.temperature,
                messages=messages,
            )
        # pylint: disable=W0703
        except Exception as exception:
            msg = f"An error occurred during completion generation: {str(exception)}"

            click.echo(click.style(msg, fg="red"))
            return None

    def __parse_code_block(self, gpt_response):
        if not gpt_response:
            return None

        pattern = r"```(?:[a-z]+\n)?(.*?)```"
        match = re.search(pattern, gpt_response, re.DOTALL)
        if match:
            return match.group(1).strip()
        raise ValueError("No code block found in response")
