import subprocess
import random
import click
import pyperclip

from commandeft.constants.consts import EXIT, AcceptCommandBehavior, Decision, fail_messages
from commandeft.util.config_util import get_configuration
from commandeft.util.interactive_util import get_decision


def decide_and_apply_action(command, history, accept_command_behavior):
    if not command:
        return EXIT

    decision = get_decision(accept_command_behavior, history)
    if history:
        if decision == Decision.EXIT:
            return EXIT
        if decision == Decision.ACTION:
            if accept_command_behavior == AcceptCommandBehavior.RUN:
                subprocess.run(command, shell=True, check=False)
                return decide_and_apply_action(command, history, accept_command_behavior)
            elif accept_command_behavior == AcceptCommandBehavior.COPY:
                pyperclip.copy(command)
                click.echo(click.style("> Command copied to clipboard!", fg="green"))
                return decide_and_apply_action(command, history, accept_command_behavior)
        return "continue"

    if decision:
        if accept_command_behavior == AcceptCommandBehavior.RUN:
            subprocess.run(command, shell=True, check=False)
        elif accept_command_behavior == AcceptCommandBehavior.COPY:
            pyperclip.copy(command)
            click.echo(click.style("> Command copied to clipboard!", fg="green"))
    else:
        random_fail_message = random.choice(fail_messages)
        click.echo(click.style(random_fail_message, fg="red"))
    return EXIT
