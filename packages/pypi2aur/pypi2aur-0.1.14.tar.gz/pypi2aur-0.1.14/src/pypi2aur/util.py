# - This is a Python 3.13 application
# - Enforce static typing (type hints) in all functions
# - Enable rich terminal output using `rich`
# - Manage Python dependencies and builds with `uv`
# - Adhere to PEP8 code style standards
# - Maintain English-only documentation and code comments
# - Apply camelCase convention for variables, methods and functions
# **Note**: While camelCase conflicts with PEP8's snake_case recommendation
# for Python, this requirement takes precedence per project specifications
# Utils Functions
#
import os
import subprocess
from rich.console import Console
from pypi2aur.constants import SPACES_DEFAULT


cl = Console(log_time_format="[%Y-%m-%d %H:%M:%S]")
# Força o Rich a não omitir timestamps repetidos
cl._log_render.omit_repeated_times = False


def printLog(message: str) -> None:
    cl.log(f"🗸 {message}")


def printLine() -> None:
    cl.print("[cyan]=[/cyan]" * 80)


def showStatus(preamble: str, message: str) -> None:
    cl.print(f"[bold yellow]{preamble:<{SPACES_DEFAULT}}[/bold yellow]: {message}")


def showError(message: str) -> None:
    error = "ERROR"
    cl.print(f"⛔ [bold red]{error:<{SPACES_DEFAULT}}[/bold red]: {message}")


def fileExists(file: str) -> bool:
    if os.path.isfile(file):
        return True
    else:
        return False


def configDirExists(configDir: str) -> bool:
    if os.path.isdir(configDir):
        return True
    else:
        return False


def executeCommand(command: str) -> tuple[int, str, str]:
    """
    Executes a shell command and returns its exit code, standard output, and standard error.

    Args:
        command (str): The shell command to execute.

    Returns:
        tuple[int, str, str]: A tuple containing the exit code, stdout, and stderr.
    """
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr
