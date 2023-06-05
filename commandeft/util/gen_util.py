import os
import re


def parse_code_block(gpt_response):
    pattern = r"```(?:[a-z]+\n)?(.*?)```"
    match = re.search(pattern, gpt_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    raise ValueError("No code block found in response")


def get_current_shell():
    shell = os.environ["SHELL"]
    shell_type = shell.split("/")[-1]
    return shell_type


def get_current_os():
    return os.uname().sysname
