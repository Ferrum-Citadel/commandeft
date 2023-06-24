import sys
import click
import openai


from commandeft.core.history_cache import HistoryCache
from commandeft.util.gen_util import (
    get_current_shell,
    get_current_os,
    parse_code_block,
)
from commandeft.util.config_util import get_configuration

model = get_configuration("model")
current_shell = get_current_shell()
current_os = get_current_os()
temperature = get_configuration("temperature")
max_tokens = get_configuration("max_tokens")
interactive_history = get_configuration("interactive_history")


openai.api_key = get_configuration("api_key")
history_cache = HistoryCache(model=model)


def generate_command(user_prompt, mode="inline"):
    generate_command.count += 1
    keep_history = False

    if mode == "interactive" and interactive_history:
        keep_history = True

    system_message = {
        "role": "system",
        "content": f"""Assume the role of a shell scripting expert with the given specifications: Shell: {current_shell}, OS: {current_os}""",
    }

    user_message = {
        "role": "user",
        "content": f"""Provide only the raw command inside a code block that best fulfills the following request: {user_prompt}.Prefer oneliners. No other text is allowed.""",
    }

    if keep_history:
        if generate_command.count == 1:
            history_cache.append(system_message)
        history_cache.append(user_message)

    messages = history_cache.get_cache() if keep_history else [system_message, user_message]

    completion = openai.ChatCompletion.create(
        model=model,
        max_tokens=max_tokens + 130 if keep_history is False else (4096 - history_cache.total_tokens()),
        temperature=temperature,
        messages=messages,
    )

    if keep_history:
        history_cache.append({"role": "assistant", "content": completion.choices[0].message.content})

    res = completion.choices[0].message.content
    try:
        command = parse_code_block(res)
        return command
    except ValueError:
        click.echo(click.style(res.replace(". ", ".\n"), fg="red"))
        if mode == "inline":
            sys.exit(1)


generate_command.count = 0
