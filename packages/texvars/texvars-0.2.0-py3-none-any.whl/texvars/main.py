import re
import os

from typing import Callable
from datetime import datetime

from texvars import __version__

__author__ = "Marcel Kempf"
__copyright__ = "Marcel Kempf"
__license__ = "MIT"


class TexVarsGenerator:
    """
    A class to generate LaTeX commands for variable definitions.
    """

    commands = []

    def __init__(self, prefix: str = "", suffix: str = ""):
        self.prefix = prefix
        self.suffix = suffix

    def add_command(self, key: str, value: str | int | float, prefix: str = "", suffix: str = "",
                    comment: str = "", formatter: Callable[[str | int | float], str] = None, override: bool = False) -> "TexVarsGenerator":
        """
        Add a command to the generator.

        :param key: The name of the variable.
        :param value: The value of the variable.
        :param prefix: An optional prefix for the command.
        :param suffix: An optional suffix for the command.
        :param comment: An optional comment for the command.
        :param formatter: A function to format the value before adding it.
        :param override: If True, will override an existing command with the same key.
        """
        prefix = prefix or self.prefix
        suffix = suffix or self.suffix
        cmd = get_latex_value_cmd(key, value, prefix, suffix, comment, formatter)
        cmd_key_re = r'\\newcommand{\\([a-zA-Z]+)}'
        cmd_key = re.search(cmd_key_re, cmd).group(1)
        if cmd_key in [re.search(cmd_key_re, c).group(1) for c in self.commands]:
            if not override:
                raise ValueError(f"Command with key '{cmd_key}' already exists. Use override=True to replace it.")
            self.commands = [c for c in self.commands if re.search(cmd_key_re, c).group(1) != cmd_key]
        self.commands.append(cmd)
        return self

    def get_commands(self) -> list[str]:
        """
        Get the list of commands generated.

        :return: A list of LaTeX commands.
        """
        return self.commands

    def store_commands(self, filename: str, overwrite: bool = False, mkdir: bool = False) -> None:
        """
        Store the generated commands in a file.

        :param filename: The name of the file to store the commands.
        :param overwrite: Whether to overwrite the file if it exists.
        """
        header = "% =============================================================\n"
        header += f"% This file was created with {__name__.split('.')[0]} version {__version__}\n"
        header += f"% Creation date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "% =============================================================\n"

        if self.commands is not None and len(self.commands) > 0:
            if os.path.exists(filename) and not overwrite:
                raise FileExistsError(f"The file {filename} already exists. Use overwrite=True to overwrite it.")
            dir_name = os.path.dirname(filename)
            if dir_name and not os.path.exists(dir_name):
                if mkdir:
                    os.makedirs(dir_name)
                else:
                    raise FileNotFoundError(
                        f"The directory {dir_name} does not exist. "
                        "Please create it or set mkdir=True."
                    )
            with open(filename, "w") as f:
                f.write(header)
                f.write("\n")
                for cmd in self.commands:
                    f.write(cmd + "\n")


def get_latex_value_cmd(key: str, value: str | int | float, prefix: str = "", suffix: str = "",
                        comment: str = "", formatter: Callable[[str | int | float], str] = None) -> str:
    for var_name, s in zip(["key", "prefix", "suffix"], [key, prefix, suffix]):
        if not isinstance(s, str) or not re.match(r'^[a-zA-Z]*$', s):
            raise ValueError(f"{var_name} should be a string containing only alphabetic characters.")
    complete_key = f"{prefix}{key}{suffix}"
    if len(complete_key) < 1:
        raise ValueError("The key, prefix and suffix must not be empty.")
    if formatter:
        value = formatter(value)
    elif isinstance(value, float):
        value = f"{value:.2f}"
    r = f"\\newcommand{{\\{complete_key}}}{{{value}}}"
    if comment:
        r += f"  % {comment}"
    return r
