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

from pnvm import console, utils


def remove(version: str) -> None:
    path_to_node_version = utils.get_pnvm_directory_path() / version

    if not utils.is_version_installed(version):
        console.error("Version not installed.", fatal=True)

    shutil.rmtree(path_to_node_version)

    if utils.get_selected_node_version() == version:
        utils.clear_existing_node_binaries()
        utils.set_selected_node_version(None)

    console.ok(f"Removed node {version}.")
