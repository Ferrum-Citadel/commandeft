from importlib.metadata import version
from functools import lru_cache
import packaging.version
import requests
import click


def get_version():
    return version("commandeft")


@lru_cache(maxsize=1)
def get_latest_version(package_name):
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        latest_version = data["info"]["version"]
        return latest_version
    # pylint: disable=[W0612]
    # pylint: disable=[W0718]
    except Exception as err:
        return None


def is_latest_version(package_name, current_version):
    latest_version = get_latest_version(package_name)
    if latest_version is None:
        return None

    return packaging.version.parse(current_version) >= packaging.version.parse(latest_version)


def check_for_updates():
    if is_latest_version("commandeft", get_version()) is False:
        click.echo(
            click.style(
                f"New version of commandeft available: {get_latest_version('commandeft')}.\nRun 'pip install commandeft --upgrade' to update.",
                fg="yellow",
            )
        )
