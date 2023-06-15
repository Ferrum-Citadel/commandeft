import json
from commandeft.constants.consts import CONFIG_FILE_PATH
from pathlib import Path
from commandeft.constants.config_constants import (REQUIRED_KEYS, TEMPERATURE, 
                                                   MAX_TOKENS, MODEL, 
                                                   ACCEPT_COMMAND_BEHAVIOR, 
                                                   GPT_3_5_TURBO, GPT4, 
                                                   MODELS_LIST, MODELS_MAX_TOKENS,
                                                   COMMAND_BEHAVIOURS)
from commandeft import CommandeftException

class Configuration(str):
    def __eq__(self, other):
        allowed_values = ["model", "temperature", "max_tokens"]
        return str(self) in allowed_values


def get_configuration(config_property):
    if CONFIG_FILE_PATH.exists():
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_file:
            configuration = json.load(config_file)
            return configuration.get(config_property)


def validate_configuration(config_file_path: Path = CONFIG_FILE_PATH):

    if not config_file_path.exists():
        raise CommandeftException("Config Error: Configuration file not found.")

    try:
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            configuration_json = json.load(config_file)
    except json.JSONDecodeError:
        raise CommandeftException("Config Error: Invalid JSON in configuration file.")

    __has_valid_contents(configuration_json)

    return configuration_json

def __has_valid_contents(configuration_json: str) -> bool:
    for key in REQUIRED_KEYS:
        if key not in configuration_json or configuration_json[key] is None or configuration_json[key] == "":
            raise CommandeftException(f"Config Error: Missing or empty value for configuration key: '{key}'")

    if configuration_json[TEMPERATURE] < 0 or configuration_json[TEMPERATURE] > 1:
        raise CommandeftException("Config Error: Invalid temperature value in configuration.")

    if not 1 <= configuration_json[MAX_TOKENS] <= MODELS_MAX_TOKENS[configuration_json[MODEL]]:
        raise CommandeftException("Config Error: Invalid max_tokens value in configuration.")

    if configuration_json[MODEL] not in MODELS_LIST:
        raise CommandeftException("Config Error: Invalid model value in configuration.")

    if configuration_json[ACCEPT_COMMAND_BEHAVIOR] not in COMMAND_BEHAVIOURS:
        raise CommandeftException("Config Error: Invalid accept_command_behavior value in configuration.")
    return True
