import pytest
from unittest.mock import patch, MagicMock, create_autospec
from commandeft.constants.consts import EXIT, AcceptCommandBehavior, Decision
from commandeft.core.decision import decide_and_apply_action
from subprocess import CompletedProcess


@pytest.fixture
def var(mocker):
    return mocker.patch("commandeft.core.config_util.get_configuration", new="value", autospec=False)


def test_decide_and_apply_empty_command():
    command = ""
    result = decide_and_apply_action(command, True, AcceptCommandBehavior.RUN)
    assert result == "exit"


def test_decide_and_apply_action_action_run():
    command = "ls -l"
    mock_completed_process = create_autospec(CompletedProcess, instance=True, returncode=0)

    # Mock the get_decision function to return Decision.ACTION.

    with patch("commandeft.core.decision.get_decision", side_effect=[Decision.ACTION, Decision.EXIT]):
        # Mock the subprocess.run function.
        with patch("subprocess.run", return_value=mock_completed_process) as mock_subprocess_run:
            mock_subprocess_run.return_value = MagicMock(returncode=0)
            result = decide_and_apply_action(command, True, AcceptCommandBehavior.RUN)

    # Check if the subprocess.run function was called with the correct command.
    mock_subprocess_run.assert_called_once_with(command, shell=True, check=False)

    # The function should return "exit" because history is not enabled.
    assert result == EXIT


def test_decide_and_apply_action_action_copy():
    # Create a mock command.
    command = "echo 'Hello, World!'"

    # Mock the get_decision function to return Decision.ACTION.
    with patch("commandeft.core.decision.get_decision", side_effect=[Decision.ACTION, Decision.EXIT]):
        # Mock the pyperclip.copy function.
        with patch("pyperclip.copy") as mock_pyperclip_copy:
            result = decide_and_apply_action(command, True, AcceptCommandBehavior.COPY)

    # Check if the pyperclip.copy function was called with the correct command.
    mock_pyperclip_copy.assert_called_once_with(command)

    # The function should return "continue" because history is enabled.
    assert result == "exit"


def test_decide_and_apply_action_decision_false():
    # Test when the decision is False (not taking the action).

    # Create a mock command.
    command = "python script.py"

    # Mock the get_decision function to return False.
    with patch("commandeft.core.decision.get_decision", return_value=False):
        # Mock the random.choice function for the fail_messages.
        with patch("random.choice") as mock_random_choice:
            mock_random_choice.return_value = "Failure message"
            result = decide_and_apply_action(command, False, AcceptCommandBehavior.RUN)

    # The function should print the failure message and return "exit".
    assert result == EXIT
    mock_random_choice.assert_called_once()
