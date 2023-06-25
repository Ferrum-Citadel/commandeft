import os
import sys
import json
from InquirerPy import prompt
import click

from commandeft.constants.consts import CONFIG_FILE_PATH, MAX_TOKENS


def get_configuration(config_property, config_file_path: str = CONFIG_FILE_PATH):
    if os.path.exists(config_file_path):
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            configuration = json.load(config_file)
            return configuration.get(config_property)
    return None


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

    if configuration["temperature"] < 0 or configuration["temperature"] > 1:
        click.echo(click.style("Config Error: Invalid temperature value in configuration.", fg="red"))
        sys.exit(1)

    if not 1 <= configuration["max_tokens"] <= MAX_TOKENS:
        click.echo(click.style("Config Error: Invalid max_tokens value in configuration.", fg="red"))
        sys.exit(1)

    if configuration["model"] not in ["gpt-3.5-turbo", "gpt4"]:
        click.echo(click.style("Config Error: Invalid model value in configuration.", fg="red"))
        sys.exit(1)

    if configuration["accept_command_behavior"] not in ["run", "copy"]:
        click.echo(click.style("Config Error: Invalid model value in configuration.", fg="red"))
        sys.exit(1)

    return configuration


def get_configuration_answers():
    # pylint: disable=unnecessary-lambda
    questions = [
        {
            "type": "list",
            "name": "model",
            "message": "Choose the model to be used:\n",
            "choices": ["gpt-3.5-turbo", "gpt-4"],
        },
        {
            "type": "input",
            "name": "temperature",
            "message": "Enter the temperature (0-1 with max 2 decimal places):\n",
            "validate": lambda val: 0 <= float(val) <= 1,
            "filter": lambda val: float(val),
        },
        {
            "type": "confirm",
            "name": "interactive_history",
            "message": "Would you like interactive mode to keep generation history?\n)",
            "default": True,
        },
        {
            "type": "input",
            "name": "max_tokens",
            "message": "Enter max_tokens [1-4,096].:\n(in interactive mode with history enabled, this value is ignored)\n",
            "validate": lambda val: 1 <= float(val) <= MAX_TOKENS,
            "filter": lambda val: int(val),
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
        }
        # Add more questions as needed
    ]
    answers = prompt(questions)
    return answers
