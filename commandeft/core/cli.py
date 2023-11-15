import os
import shutil
import json
import click
import pyperclip


from commandeft.constants.consts import COMMANDEFT_ASCII_DESC, COMMANDEFT_NORMAL_DESC, CONFIG_FILE_PATH, Mode
from commandeft.core.decision import decide_and_apply_action
from commandeft.core.generation import Generation
from commandeft.util.config_util import create_generation_config, get_configuration_answers, validate_configuration
from commandeft.util.interactive_util import display_command, get_prompt
from commandeft.util.config_util import get_configuration


COMMANDEFT_DESCRIPTION = COMMANDEFT_ASCII_DESC if shutil.get_terminal_size().columns >= 50 else COMMANDEFT_NORMAL_DESC


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
        + "To change the configuration, run `commandeft --configure (or -c)`\n"
    )


def interactive_core(is_first_prompt, generation):
    user_prompt: str = get_prompt(is_first_prompt)
    command: str | None = generation.generate_command(user_prompt)

    accept_command_behavior = get_configuration("accept_command_behavior")
    history = get_configuration("interactive_history")
    if command:
        display_command(command)
        return decide_and_apply_action(command, history, accept_command_behavior)
    return "exit"


def interactive_mode():
    if not os.path.exists(CONFIG_FILE_PATH):
        configuration_mode()
    else:
        validate_configuration()

    generation_config = create_generation_config()
    generation_config["mode"] = Mode.INTERACTIVE
    generation = Generation(generation_config)

    next_action = interactive_core(is_first_prompt=True, generation=generation)
    while next_action == "continue":
        next_action = interactive_core(is_first_prompt=False, generation=generation)


def prompt_in_line(prompt):
    if not os.path.exists(CONFIG_FILE_PATH):
        configuration_mode()
    else:
        validate_configuration()

    generation_config = create_generation_config()
    generation_config["mode"] = Mode.INLINE
    generation = Generation(generation_config)

    command = generation.generate_command(prompt)
    click.echo(click.style("> " + command, fg="green"))
    pyperclip.copy(command)
    click.echo("Command copied to clipboard!")
