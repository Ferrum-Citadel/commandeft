import sys
import click
import guidance

from commandeft.util.gen_util import (
    get_current_shell,
    get_current_os,
    parse_code_block,
)
from commandeft.util.config_util import get_configuration


def generate_command(user_prompt):
    api_key = get_configuration("api_key")
    llm = guidance.llms.OpenAI(
        get_configuration("model"),
        api_key=api_key,
    )

    current_shell = get_current_shell()
    current_os = get_current_os()
    temperature = get_configuration("temperature")
    max_tokens = get_configuration("max_tokens")

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
    program = guidance(
        template_default,
        llm=llm,
    )

    res = program(
        user_prompt=user_prompt,
        chosen_temperature=temperature,
        current_shell=current_shell,
        current_os=current_os,
        # 55 is the number of tokens consumed by the guided prompt
        chosen_max_tokens=max_tokens + 55,
        caching=True,
    )
    try:
        command = parse_code_block(res["result"])
        return command
    except ValueError:
        click.echo(click.style(res["result"].replace(". ", ".\n"), fg="red"))
        sys.exit(1)
