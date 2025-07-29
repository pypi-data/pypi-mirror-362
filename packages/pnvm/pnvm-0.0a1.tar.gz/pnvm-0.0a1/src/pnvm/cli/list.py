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

from pathlib import Path

from pnvm import console, utils


def _is_listed_version_selected_version(item: Path) -> bool:
    return item.name == utils.get_selected_node_version()


def _list_version(entry: Path, indentation: str) -> None:
    # Indicate the currently selected version
    if _is_listed_version_selected_version(entry):
        console.log("*" + indentation[1:], color="blue", bold=True, end="")
        console.log(entry.name, bold=True)

    else:
        console.log(f"{indentation}{entry.name}")


def list_versions() -> None:
    path = utils.get_pnvm_directory_path()

    # Value reflecting the indentation amount as a number
    indent_steps = 2

    # Do not list these directories as versions.
    excluded_directories = ["bin"]

    # Indent the list if there is a selected version available.
    indentation = " " * indent_steps if utils.get_selected_node_version() else ""

    # Iterate over each folder (version) in the PNVM base directory.
    for entry in path.glob("*"):
        # Versions are represented internally as directories.
        if entry.is_dir() and entry.name not in excluded_directories:
            _list_version(entry, indentation)
