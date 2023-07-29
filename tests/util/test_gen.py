import os
from commandeft.util.gen_util import get_current_os, get_current_shell

# Replace 'your_module' with the actual module where the functions are defined

def test_get_current_shell_nt():
    # Test for Windows (nt) OS
    expected_shell = "cmd.exe"  # The expected shell for Windows is cmd.exe
    os.environ["SHELL"] = expected_shell
    assert get_current_shell() == expected_shell

def test_get_current_shell_posix():
    # Test for POSIX (Linux, macOS, etc.) OS
    expected_shell = "bash"  # The expected shell for POSIX is bash
    os.environ["SHELL"] = expected_shell
    assert get_current_shell() == expected_shell

def test_get_current_os():
    # Test the get_current_os function
    assert get_current_os() in ["posix", "nt"]
    # The returned value should be either 'posix' for Linux/macOS or 'nt' for Windows
