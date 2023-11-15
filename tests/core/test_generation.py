# test_generation.py

import pytest
from unittest.mock import patch, MagicMock
from commandeft.constants.consts import Mode, Models
from commandeft.core.generation import Generation


def mock_openai_chat_completion(*args, **kwargs):
    # Mock the behavior of openai.ChatCompletion.create function.
    # For simplicity, let's return a MagicMock object for completion.choices[0].message.content.
    completion_mock = MagicMock()
    completion_mock.choices[0].message.content = "Generated command content"
    return completion_mock


@pytest.mark.skip(reason="TODO: Implement this test.")
def test_generate_command_inline():
    # Test generate_command in INLINE mode.

    # Create a mock config dictionary.
    config = {
        "mode": Mode.INLINE,
        "model": Models.GPT_4,
        "current_os": "Linux",
        "current_shell": "bash",
        "temperature": 0.8,
        "max_tokens": 100,
        "interactive_history": False,
    }

    # Create a Generation object with the mock config.
    with patch("commandeft.core.generation.openai.ChatCompletion.create", side_effect=mock_openai_chat_completion):
        generation = Generation(config)

        # Call the function under test.
        generated_command = generation.generate_command("Test prompt")

        # Check if the generated_command matches the expected content from the mock.
        assert generated_command == "Generated command content"


@pytest.mark.skip(reason="TODO: Implement this test.")
def test_generate_command_interactive():
    # Test generate_command in INTERACTIVE mode.

    # Create a mock config dictionary.
    config = {
        "mode": Mode.INTERACTIVE,
        "model": Models.GPT_3_5_TURBO,
        "current_os": "Linux",
        "current_shell": "bash",
        "temperature": 0.5,
        "max_tokens": 150,
        "interactive_history": True,
    }

    # Create a Generation object with the mock config.
    with patch("commandeft.core.generation.openai.ChatCompletion.create", side_effect=mock_openai_chat_completion):
        generation = Generation(config)

        # Call the function under test.
        generated_command = generation.generate_command("Test prompt")

        # Check if the generated_command matches the expected content from the mock.
        assert generated_command == "Generated command content"


def test_generate_command_invalid_response():
    # Test generate_command with an invalid response.

    # Create a mock config dictionary.
    config = {
        "mode": Mode.INTERACTIVE,
        "model": Models.GPT_3_5_TURBO,
        "current_os": "Linux",
        "current_shell": "bash",
        "temperature": 0.5,
        "max_tokens": 150,
        "interactive_history": True,
    }

    # Create a Generation object with the mock config.
    with patch("commandeft.core.generation.openai.ChatCompletion.create", return_value=None):
        with patch("commandeft.core.generation.get_configuration") as mock_get_config:
            generation = Generation(config)

            # Call the function under test.
            generated_command = generation.generate_command("Test prompt")

            # Check if the generated_command is None when there is no valid response.
            assert generated_command is None


def test_parse_code_block():
    # Test __parse_code_block method.

    # Create a mock config dictionary.
    config = {
        "mode": Mode.INLINE,
        "model": Models.GPT_4,
        "current_os": "Linux",
        "current_shell": "bash",
        "temperature": 0.8,
        "max_tokens": 100,
        "interactive_history": False,
    }

    # Create a Generation object with the mock config.
    with patch("commandeft.core.generation.openai.ChatCompletion.create", side_effect=mock_openai_chat_completion):
        generation = Generation(config)

        # Call the __parse_code_block method with a mock gpt_response.
        gpt_response = "This is a test response with a code block:\n```bash\necho 'Hello, World!'\n```"
        with patch("commandeft.core.generation.re.search") as mock_search:
            mock_search.return_value = MagicMock(group=lambda x: "echo 'Hello, World!'")
            parsed_code_block = generation._Generation__parse_code_block(gpt_response)

        # Check if the parsed_code_block matches the expected content from the mock_search.
        assert parsed_code_block == "echo 'Hello, World!'"

        # Test the case when there is no code block in the response.
        gpt_response_no_block = "This is a test response without a code block."
        with patch("commandeft.core.generation.re.search") as mock_search:
            mock_search.return_value = None
            with pytest.raises(ValueError) as exc_info:
                parsed_code_block = generation._Generation__parse_code_block(gpt_response_no_block)

        # Check if a ValueError is raised when there is no code block.
        assert str(exc_info.value) == "No code block found in response"
