import os
import sys
import json
from InquirerPy import prompt
import click

from commandeft.constants.consts import CONFIG_FILE_PATH
from commandeft.core.history_cache import HistoryCache
from commandeft.util.gen_util import get_current_os, get_current_shell


def get_configuration(config_property, config_file_path: str = CONFIG_FILE_PATH):
    if os.path.exists(config_file_path):
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            configuration = json.load(config_file)
            return configuration.get(config_property)
    return None


def create_generation_config():
    model = get_configuration("model")
    current_os = get_current_os()
    current_shell = get_current_shell()
    temperature = get_configuration("temperature")
    max_tokens = get_configuration("max_tokens")
    interactive_history = get_configuration("interactive_history")

    generation_config = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "interactive_history": interactive_history,
        "current_os": current_os,
        "current_shell": current_shell,
        "history_cache": HistoryCache(model=model),
    }

    return generation_config


if get_configuration("model") == "gpt-4":
    from commandeft.constants.consts import GPT_4_MAX_TOKENS as MAX_TOKENS
else:
    from commandeft.constants.consts import GPT_3_5_MAX_TOKENS as MAX_TOKENS


def validate_configuration(config_file_path: str = CONFIG_FILE_PATH):
    required_keys = ["model", "temperature", "max_tokens", "accept_command_behavior"]

    if not os.path.exists(config_file_path):
        click.echo(click.style("Configuration file not found.", fg="red"))
        sys.exit(1)

    with open(config_file_path, "r", encoding="utf-8") as config_file:
        configuration = json.load(config_file)

    for key in required_keys:
        if key not in configuration or configuration[key] is None or configuration[key] == "":
            click.echo(click.style(f"Config Error: Missing or empty value for configuration key: '{key}'", fg="red"))
            sys.exit(1)

    if configuration["temperature"] < 0 or configuration["temperature"] > 2:
        click.echo(click.style("Config Error: Invalid temperature value in configuration.", fg="red"))
        sys.exit(1)

    if not 1 <= configuration["max_tokens"] <= MAX_TOKENS:
        click.echo(click.style("Config Error: Invalid max_tokens value in configuration.", fg="red"))
        sys.exit(1)

    if configuration["model"] not in ["gpt-3.5-turbo", "gpt-4"]:
        click.echo(click.style("Config Error: Invalid model value in configuration.", fg="red"))
        sys.exit(1)

    if configuration["accept_command_behavior"] not in ["run", "copy"]:
        click.echo(click.style("Config Error: Invalid model value in configuration.", fg="red"))
        sys.exit(1)

    return configuration


def validate_max_tokens(answers, curr_val):
    if curr_val == "":
        return False

    if answers["model"] == "gpt-4":
        return 1 <= int(curr_val) <= 8192

    return 1 <= int(curr_val) <= 4096


def get_configuration_answers():
    # pylint: disable=unnecessary-lambda
    model_question = [
        {
            "type": "list",
            "name": "model",
            "message": "Choose the model to be used:\n",
            "choices": ["gpt-3.5-turbo", "gpt-4"],
        },
    ]
    model_answer = prompt(model_question)
    questions = [
        {
            "type": "input",
            "name": "temperature",
            "message": "Enter the temperature (0-2 with max 2 decimal places):\n",
            "validate": lambda val: False if val == "" else 0 <= float(val) <= 2,
            "filter": lambda val: False if val == "" else float(val),
        },
        {
            "type": "input",
            "name": "max_tokens",
            "message": "Enter max_tokens (gpt-3.5-turbo:[1-4,096], gpt-4:[1-8,192]).:\n",
            "validate": lambda val: validate_max_tokens(model_answer, val),
            "filter": lambda val: False if val == "" else int(val),
        },
        {
            "type": "confirm",
            "name": "interactive_history",
            "message": "Would you like interactive mode to keep generation history?\n)",
            "default": True,
        },
        {
            "type": "password",
            "name": "api_key",
            "message": "Enter your OpenAI API key:\n",
        },
        {
            "type": "list",
            "name": "accept_command_behavior",
            "message": "When accepting a command in interactive mode, would you like to:\n",
            "choices": [
                {"name": "Copy it to clipboard?", "value": "copy", "short": "copy?"},
                {"name": "Run it?", "value": "run", "short": "run?"},
            ],
        },
    ]
    answers = prompt(questions)
    answers = {**model_answer, **answers}
    return answers
