import os
import json
import pytest

from commandeft.constants.consts import Models
from commandeft.core.history_cache import HistoryCache
from commandeft.util.config_util import create_generation_config, get_configuration_answers, validate_configuration, validate_max_tokens
from unittest.mock import patch

# Replace 'your_module' with the actual module where the functions are defined

def create_temp_config_file(config):
    # Helper function to create a temporary config file for testing
    with open("temp_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f)

def delete_temp_config_file():
    # Helper function to delete the temporary config file after testing
    if os.path.exists("temp_config.json"):
        os.remove("temp_config.json")

def test_validate_configuration_valid():
    config = {
        "model": Models.GPT_3_5_TURBO,
        "temperature": 0.7,
        "max_tokens": 50,
        "accept_command_behavior": "run",
    }
    create_temp_config_file(config)

    try:
        # Assert that the function doesn't raise any exception for valid configuration
        assert validate_configuration("temp_config.json") == config
    finally:
        delete_temp_config_file()

def test_validate_configuration_missing_key():
    # Test for missing required key in the configuration
    config = {
        "model": Models.GPT_3_5_TURBO,
        "temperature": 0.7,
        # max_tokens key is missing
        "accept_command_behavior": "run",
    }
    create_temp_config_file(config)

    with pytest.raises(SystemExit):
        validate_configuration("temp_config.json")

    delete_temp_config_file()

def test_validate_configuration_invalid_model():
    # Test for invalid model value in the configuration
    config = {
        "model": "invalid_model",
        "temperature": 0.7,
        "max_tokens": 50,
        "accept_command_behavior": "run",
    }
    create_temp_config_file(config)

    with pytest.raises(SystemExit):
        validate_configuration("temp_config.json")

    delete_temp_config_file()

def test_validate_configuration(tmp_path):
    # Test the validate_configuration function.

    config_data = {
        "model": "gpt-4",
        "temperature": 1.5,
        "max_tokens": 200,
        "accept_command_behavior": "copy",
    }

    # Create a temporary JSON config file.
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    # Call the function under test.
    config = validate_configuration(config_file_path=str(config_file))

    # Check if the function does not raise any exceptions.

    # Check if the returned config matches the expected configuration.
    assert config == config_data

    # Test invalid configurations.
    invalid_config_data = {
        "model": "invalid_model",
        "temperature": -1.0,
        "max_tokens": 500,
        "accept_command_behavior": "invalid_value",
    }
    config_file_invalid = tmp_path / "config_invalid.json"
    config_file_invalid.write_text(json.dumps(invalid_config_data))

    with pytest.raises(SystemExit) as exc_info:
        validate_configuration(config_file_path=str(config_file_invalid))

    assert exc_info.value.code == 1

def test_validate_max_tokens_valid():
    assert validate_max_tokens({"model": Models.GPT_3_5_TURBO}, 50) is True
    assert validate_max_tokens({"model": Models.GPT_4}, 200) is True

def test_validate_max_tokens_invalid():
    # Test for invalid max_tokens value for GPT-4
    assert validate_max_tokens({"model": Models.GPT_4}, 10000) is False
    assert validate_max_tokens({"model": Models.GPT_4}, -5) is False

    # Test for invalid max_tokens value for GPT-3.5 Turbo
    assert validate_max_tokens({"model": Models.GPT_3_5_TURBO}, 0) is False
    assert validate_max_tokens({"model": Models.GPT_3_5_TURBO}, 100000) is False


def test_create_generation_config():
    # Test the create_generation_config function.

    # For simplicity, we will mock the calls to get_configuration and get_current_os/get_current_shell.
    with patch("commandeft.util.config_util.get_configuration") as mock_get_config:
        with patch("commandeft.util.config_util.get_current_os") as mock_get_os:
            with patch("commandeft.util.config_util.get_current_shell") as mock_get_shell:
                with patch("commandeft.util.config_util.HistoryCache") as mock_history_cache:
                    mock_get_config.side_effect = ["gpt-3.5", 1.0, 100, True]
                    mock_get_os.return_value = "Linux"
                    mock_get_shell.return_value = "bash"
                    mock_history_cache.return_value = HistoryCache(model="gpt-3.5")

                    # Call the function under test.
                    generation_config = create_generation_config()

                    # Check if the returned generation_config matches the expected configuration.
                    expected_config = {
                        "model": "gpt-3.5",
                        "temperature": 1.0,
                        "max_tokens": 100,
                        "interactive_history": True,
                        "current_os": "Linux",
                        "current_shell": "bash",
                        "history_cache": mock_history_cache.return_value,
                    }
                    assert generation_config == expected_config


def test_get_configuration_answers():
    # For simplicity, we will mock the calls to prompt and provide fixed answers.
    with patch("commandeft.util.config_util.prompt") as mock_prompt:
        mock_prompt.return_value = {
            "model": "gpt-4",
            "temperature": 1.0,
            "max_tokens": 100,
            "interactive_history": True,
            "api_key": "your_api_key",
            "accept_command_behavior": "copy",
        }

        # Call the function under test.
        answers = get_configuration_answers()

        # Check if the returned answers match the expected values.
        expected_answers = {
            "model": "gpt-4",
            "temperature": 1.0,
            "max_tokens": 100,
            "interactive_history": True,
            "api_key": "your_api_key",
            "accept_command_behavior": "copy",
        }
        assert answers == expected_answers
