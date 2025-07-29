"""
pnvm -- A pythonic node version manager
Copyright (C) 2025  Axel H. Karlsson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys

from typing import Literal, Optional

from .config import get_config

# ---
# Global flag indicating if I/O should be silenced, can be modified externally

# NOTE:
# I know global variables are very frowned upon, but this is the most KISS solution
# I can come up without passing a bunch of arguments to the console functions.


def _terminal_supports_color() -> bool:
    term = os.environ.get("TERM")

    supports_color = False

    if term == "xterm-256color":
        supports_color = True

    return supports_color


def _create_escape_sequence(color: str | None = None, bold: bool = False) -> str:
    escape_sequence = "\033["

    if bold and not color:
        escape_sequence += "1"
    elif bold and color:
        escape_sequence += "1;"

    if color == "red":
        escape_sequence += "31m"
    elif color == "green":
        escape_sequence += "32m"
    elif color == "blue":
        escape_sequence += "34m"
    else:
        escape_sequence += "m"

    return escape_sequence


def log(
    message: str,
    to_stderr: bool = False,
    color: Optional[Literal["red", "green", "blue", "default"]] = "default",
    bold: bool = False,
    end: str = "\n",
) -> None:
    if get_config().silenced:
        return

    file = sys.stderr if to_stderr else sys.stdout

    colors = {
        "red": _create_escape_sequence("red", bold),
        "green": _create_escape_sequence("green", bold),
        "blue": _create_escape_sequence("blue", bold),
        "default": _create_escape_sequence(None, bold),
    }

    colorized = True if color in colors and _terminal_supports_color() else False

    if colorized:
        # Yes, I know you shouldn't disable type checking but Pylance is a
        # complete piece of sh*t right now.
        file.write(colors[color])  # type: ignore

    print(message, file=file, end=end if not colorized else "")

    if colorized:
        file.write(f"\033[0m{end}")


def ok(message: str) -> None:
    if get_config().silenced:
        return

    supports_color = _terminal_supports_color()

    if not supports_color:
        print(f"SUCCESS: {message}")
        return

    print(f"\033[1;34mSUCCESS: \033[0m{message}")


def error(message: str, fatal: bool = False) -> None:
    if get_config().silenced:
        if fatal:
            sys.exit(1)
        return

    supports_color = _terminal_supports_color()

    if not supports_color:
        print(f"ERROR: {message}", file=sys.stderr)
    else:
        print(f"\033[1;31mERROR: \033[0m{message}", file=sys.stderr)

    if fatal:
        sys.exit(1)


def warning(message: str) -> None:
    if get_config().silenced:
        return

    supports_color = _terminal_supports_color()

    if not supports_color:
        print(f"WARNING: {message}", file=sys.stderr)
        return

    print(f"\033[1;33mWARNING: \033[0m{message}", file=sys.stderr)
