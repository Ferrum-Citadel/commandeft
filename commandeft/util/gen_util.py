import os
import re


def parse_code_block(gpt_response):
    pattern = r"```(?:[a-z]+\n)?(.*?)```"
    match = re.search(pattern, gpt_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    raise ValueError("No code block found in response")


def get_current_shell():
    shell = "Unknown"
    os_name = get_current_os()
    if os_name == "nt":
        shell = os.environ.get("COMSPEC")
        shell = shell.rsplit("\\", 1)[-1]

    elif os_name == "posix":
        shell = os.environ.get("SHELL")
        shell = shell.rsplit("/", 1)[-1]

    return shell


def get_current_os():
    return os.name
