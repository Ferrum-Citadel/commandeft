import os
import sys
import json
import click

from commandeft.constants.consts import CONFIG_FILE_PATH


class Configuration(str):
    def __eq__(self, other):
        allowed_values = ["model", "temperature", "max_tokens"]
        return str(self) in allowed_values


def get_configuration(config_property: Configuration, config_file_path: str = CONFIG_FILE_PATH):
    if os.path.exists(config_file_path):
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            configuration = json.load(config_file)
            return configuration.get(config_property)


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

    if not 1 <= configuration["max_tokens"] <= 4096:
        click.echo(click.style("Config Error: Invalid max_tokens value in configuration.", fg="red"))
        sys.exit(1)

    if configuration["model"] not in ["gpt-3.5-turbo", "gpt4"]:
        click.echo(click.style("Config Error: Invalid model value in configuration.", fg="red"))
        sys.exit(1)

    if configuration["accept_command_behavior"] not in ["run", "copy"]:
        click.echo(click.style("Config Error: Invalid model value in configuration.", fg="red"))
        sys.exit(1)

    return configuration
