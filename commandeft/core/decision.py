import subprocess
import random
import click
import pyperclip

from commandeft.constants.consts import fail_messages
from commandeft.util.config_util import get_configuration
from commandeft.util.interactive_util import get_decision


def decide_and_apply_action(command):
    accept_command_behavior = get_configuration("accept_command_behavior")

    decision = get_decision(accept_command_behavior)
    if decision:
        if accept_command_behavior == "run":
            subprocess.run(command, shell=True, check=False)
        elif accept_command_behavior == "copy":
            pyperclip.copy(command)
            click.echo(click.style("> Command copied to clipboard!", fg="green"))
    else:
        random_fail_message = random.choice(fail_messages)
        click.echo(click.style(random_fail_message, fg="red"))
