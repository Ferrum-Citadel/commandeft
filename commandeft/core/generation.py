import sys
import click
import openai

from commandeft.util.gen_util import (
    get_current_shell,
    get_current_os,
    parse_code_block,
)
from commandeft.util.config_util import get_configuration

openai.api_key = get_configuration("api_key")


def generate_command(user_prompt):
    current_shell = get_current_shell()
    current_os = get_current_os()
    temperature = get_configuration("temperature")
    max_tokens = get_configuration("max_tokens")

    assistane_message = [
        {
            "role": "system",
            "content": f"""
                Assume the role of a shell scripting expert with the given specifications:
                Shell: {current_shell}
                OS: {current_os}
            """,
        }
    ]

    user_message = [
        {
            "role": "user",
            "content": f"""
                Provide only the raw command inside a code block that best fulfills the following request: {user_prompt}
                Prefer oneliners. No other text is allowed.
            """,
        }
    ]

    messages = assistane_message + user_message

    completion = openai.ChatCompletion.create(
        model=get_configuration("model"),
        max_tokens=max_tokens + 55,
        temperature=temperature,
        messages=messages,
    )

    res = completion.choices[0].message.content
    try:
        command = parse_code_block(res)
        return command
    except ValueError:
        click.echo(click.style(res.replace(". ", ".\n"), fg="red"))
        sys.exit(1)
