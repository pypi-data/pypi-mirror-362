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

import shutil
import os

from pathlib import Path

from .console import error
from . import __version__ as package_version


def _get_home_directory_path() -> str:
    path_to_home = os.environ.get("HOME")

    if not path_to_home:
        raise TypeError("Expected variable 'pathToHome' to be of type 'str', not 'None'.")

    return path_to_home


# Get the path where all PNVM-related stuff is kept.
def get_pnvm_directory_path() -> Path:
    return Path(_get_home_directory_path(), ".pnvm")


def get_pnvm_bin_path() -> Path:
    return get_pnvm_directory_path() / "bin"


def clear_existing_node_binaries() -> None:
    shutil.rmtree(get_pnvm_bin_path())


# Create required directories needed for PNVM if they don't already exist.
def setup_pnvm() -> None:
    # Create ~/.pnvm
    path = get_pnvm_directory_path()

    if not path.exists():
        Path.mkdir(path)

    # Create ~/.pnvm/bin
    bin_path = get_pnvm_bin_path()

    if not bin_path.exists():
        Path.mkdir(bin_path)

    # Add ~/.pnvm/bin to $PATH

    shell = os.environ.get("SHELL", "")
    home = _get_home_directory_path()

    rc_file = ""

    if "bash" in shell:
        rc_file = Path(home, ".bashrc")
    elif "zsh" in shell:
        rc_file = Path(home, ".zshrc")
    elif "fish" in shell:
        rc_file = Path(home, ".config/fish/config.fish")
    else:
        return

    command = "\n# --- Added by PNVM ---\n" + f'export PATH="{str(get_pnvm_bin_path())}/node-js/bin:$PATH"\n'

    with open(rc_file, "r") as f:
        # Don't add command since it's already present.
        if command in f.read():
            return

    with open(rc_file, "a") as f:
        f.write(command)


def get_selected_node_version() -> str | None:
    # Path to file where the current version is listed
    path = get_pnvm_directory_path() / "selected_version"

    version = None

    try:
        with open(path, "r") as f:
            version = f.read()
    except FileNotFoundError:
        with open(path, "w") as f:
            f.write("")
    except:
        error("Failed to get version.", fatal=True)
        raise  # Re-raise the exception for further handling

    return version


def set_selected_node_version(version: str | None) -> None:
    # Path to file where the current version is listed
    path = get_pnvm_directory_path() / "selected_version"

    with open(path, "w") as f:
        f.write("" if not version else version)


def get_cli_version() -> str:
    return package_version


# Checks if a node version is already installed
def is_version_installed(which_version: str) -> bool:
    return (get_pnvm_directory_path() / which_version).exists()
