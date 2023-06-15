import guidance
import tiktoken
from openai.error import InvalidRequestError
from commandeft import CommandeftException
from commandeft.constants.config_constants import API_KEY, MAX_TOKENS, MODEL, MODELS_MAX_TOKENS, TEMPERATURE

from commandeft.util.gen_util import (
    get_current_shell,
    get_current_os,
    parse_code_block,
)
from commandeft.util.config_util import get_configuration


def generate_command(user_prompt: str) -> str:
    model = get_configuration(MODEL)
    api_key = get_configuration(API_KEY)
    llm = guidance.llms.OpenAI(
        model=model,
        api_key=api_key,
    )

    current_shell_conf = get_current_shell()
    current_os_conf = get_current_os()
    temperature_conf = get_configuration(TEMPERATURE)
    max_tokens_conf = get_configuration(MAX_TOKENS)

    template_default = """{{#system~}}
        Assume the role of a shell scripting expert with the given specifications:
        Shell: {{current_shell}}
        OS: {{current_os}}
        {{~/system}}
        {{#user~}}
        Provide only the raw command inside a code block that best fulfills the following request: {{user_prompt}}
        Prefer oneliners. No other text is allowed.
        {{~/user}}
        {{#assistant~}}
        {{gen 'result' max_tokens=chosen_max_tokens temperature=chosen_temperature}}
        {{~/assistant}}"""

    # pylint: disable=not-callable

    try:
        program = guidance(
           template_default,
            llm=llm,
        )
        prompt_tokens: int = __num_tokens_from_string(user_prompt, model)
        model_max_token_limit = MODELS_MAX_TOKENS[model]
        if prompt_tokens + 55 > model_max_token_limit or prompt_tokens + 55 > max_tokens_conf:
            raise CommandeftException(
                f"""Your prompt is too long ({prompt_tokens} tokens). The maximum number of tokens for model {model} is {model_max_token_limit}.
                Your max_tokens configuration is {max_tokens_conf}. Please shorten your prompt."""
            )
        chosen_max_tokens = max_tokens_conf + 55 + prompt_tokens
            

        res = program(
            user_prompt=user_prompt,
            chosen_temperature=temperature_conf,
            current_shell=current_shell_conf,
            current_os=current_os_conf,
            # 55 is the number of tokens consumed by the guided prompt
            chosen_max_tokens=chosen_max_tokens,
            caching=True,
        )
        command = parse_code_block(res["result"])
        return command
    except ValueError:
        raise CommandeftException(res["result"].replace(". ", ".\n"))
    except InvalidRequestError as e:
        raise CommandeftException("OpenAI API Error: " + str(e))

def __num_tokens_from_string(string: str, model) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens