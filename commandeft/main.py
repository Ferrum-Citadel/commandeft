import sys
import click


from commandeft.core.cli import CustomCommand, configuration_mode, prompt_in_line, interactive_mode


def custom_exception_handler(exc_value):
    # Handle the exception
    click.echo(click.style(f"An error occurred:{str(exc_value),}", fg="red"))
    sys.exit(1)


sys.excepthook = custom_exception_handler


@click.command(cls=CustomCommand)
@click.help_option("-h", "--help")
@click.option("-v", "--version", help="Show version and exit", is_flag=True)
@click.option("-c", "--configure", help="Configure commandeft", is_flag=True)
@click.option("-i", "--interactive", help="Run in interactive mode", is_flag=True)
@click.option("-p", "--prompt", help="Specify your prompt inline")
def commandeft(version, configure, interactive, prompt):
    if version:
        click.echo("v0.0.1")
    elif configure:
        configuration_mode()
    elif interactive:
        interactive_mode()
    elif prompt:
        prompt_in_line(prompt)
    else:
        click.echo("Run with -h or --help for usage information.")


if __name__ == "__main__":
    commandeft()  # pylint: disable=no-value-for-parameter
