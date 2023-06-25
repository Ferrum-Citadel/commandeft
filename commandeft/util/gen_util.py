import os


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
