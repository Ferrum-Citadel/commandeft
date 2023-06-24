import os
import shutil
import json
from importlib.metadata import version
import click
import pyperclip


from commandeft.constants.consts import COMMANDEFT_ASCII_DESC, COMMANDEFT_NORMAL_DESC, CONFIG_FILE_PATH
from commandeft.core.decision import decide_and_apply_action
from commandeft.core.generation import generate_command
from commandeft.util.config_util import get_configuration_answers, validate_configuration
from commandeft.util.interactive_util import get_prompt

COMMANDEFT_DESCRIPTION = COMMANDEFT_ASCII_DESC if shutil.get_terminal_size((80, 20)).columns >= 50 else COMMANDEFT_NORMAL_DESC


class CustomCommand(click.Command):
    def get_help(self, ctx):
        # Get the default help message
        help_message = super().get_help(ctx)

        # Customize the usage message
        custom_usage = COMMANDEFT_DESCRIPTION

        # Prepend the custom string to the usage message
        return custom_usage + help_message


def configuration_mode():
    if os.path.exists(CONFIG_FILE_PATH):
        click.confirm(
            "Warning: Running the configuration flow will overwrite your previous configuration. \nAre you sure you want to continue?",
            abort=True,
            default=True,
        )

    answers = get_configuration_answers()

    # Save the configuration options to the file
    os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as config_file:
        json.dump(answers, config_file)

    click.echo(
        "-------------------------------------\n"
        + click.style("Configuration completed successfully.\n", fg="green")
        + "To change the configuration, edit ~/.commandeft/config or run `commandeft --configure (or -c)]`\n"
    )


def interactive_core(first_prompt):
    user_prompt = get_prompt(first_prompt)
    command = generate_command(user_prompt, mode="interactive")
    if command:
        click.echo("~" * (len(command) + 2))
        click.echo(click.style("> " + command, fg="green", bold=True))
        click.echo("~" * (len(command) + 2))

    return decide_and_apply_action(command)


def interactive_mode():
    if not os.path.exists(CONFIG_FILE_PATH):
        configuration_mode()
    else:
        validate_configuration()

    next_action = interactive_core(first_prompt=True)
    while next_action == "continue":
        next_action = interactive_core(first_prompt=False)


def prompt_in_line(prompt):
    if not os.path.exists(CONFIG_FILE_PATH):
        configuration_mode()
    else:
        validate_configuration()
    command = generate_command(prompt, mode="inline")
    click.echo(click.style("> " + command, fg="green"))
    pyperclip.copy(command)
    click.echo("Command copied to clipboard!")


def print_version():
    click.echo(version("commandeft"))
