import json
import random
import shutil

from InquirerPy import prompt
import click
from commandeft.constants.consts import AcceptCommandBehavior, init_messages


def display_command(command):
    terminal_cols = shutil.get_terminal_size().columns
    num_of_tildes = len(command.splitlines()[0]) + 2
    click.echo("~" * min(num_of_tildes, terminal_cols))
    click.echo(click.style("> " + command, fg="green", bold=True))
    click.echo("~" * min(num_of_tildes, terminal_cols))


def get_prompt(first_prompt=True):
    random_prompt_message = random.choice(init_messages)
    questions = [
        {
            "type": "input",
            "name": "prompt",
            "message": random_prompt_message if first_prompt is True else "Clarify or expand on your previous prompt:\n",
            "qmark": "-",
            "default": "",
            "filter": lambda val: json.dumps(val.strip()),
        },
    ]
    answers = prompt(questions)
    return answers["prompt"]


def get_decision(accept_command_behavior, history):
    if history is False:
        if accept_command_behavior == AcceptCommandBehavior.RUN:
            choice_question = [
                {
                    "type": "confirm",
                    "name": "interact",
                    "message": "Do you want to execute the command?",
                    "default": True,
                }
            ]
        elif accept_command_behavior == AcceptCommandBehavior.COPY:
            choice_question = [
                {
                    "type": "confirm",
                    "name": "interact",
                    "message": "Do you want to copy the command to clipboard?",
                    "default": True,
                }
            ]
    else:
        choice_question = [
            {
                "type": "rawlist",
                "name": "interact",
                "choices": [
                    {
                        "name": ("Run it." if accept_command_behavior == "run" else "Copy to clipboard."),
                        "value": "action",
                    },
                    {"name": "Continue session.", "value": "continue"},
                    {"name": "Exit session.", "value": "exit"},
                ],
                "message": "What would you like to do?\n",
                "default": 1,
                "mandatory": True,
                "multiselect": False,
            },
        ]
    choice_answer = prompt(choice_question)
    return choice_answer["interact"]
