import random

from InquirerPy import prompt
from commandeft.constants.consts import init_messages


def handle_escape(event):
    if event.name == "esc":
        raise KeyboardInterrupt()


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
            "type": "input",
            "name": "max_tokens",
            "message": "Enter max_tokens(1-4,096). Keep in mind that guided prompt consumes ~55 tokens.:\n",
            "validate": lambda val: 1 <= float(val) <= 4096,
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


def get_prompt():
    random_prompt_message = random.choice(init_messages)
    questions = [
        {
            "type": "input",
            "name": "prompt",
            "message": random_prompt_message + "\n",
            "default": "",
            "filter": lambda val: '"' + val.strip() + '"',
        },
    ]
    answers = prompt(questions)
    return answers["prompt"]


def get_decision(accept_command_behavior):
    if accept_command_behavior == "run":
        choice_question = [
            {
                "type": "confirm",
                "name": "execute",
                "message": "Do you want to execute the command?",
                "default": True,
            }
        ]
    elif accept_command_behavior == "copy":
        choice_question = [
            {
                "type": "confirm",
                "name": "execute",
                "message": "Do you want to copy the command to clipboard?",
                "default": True,
            }
        ]
    choice_answer = prompt(choice_question)
    return choice_answer["execute"]
