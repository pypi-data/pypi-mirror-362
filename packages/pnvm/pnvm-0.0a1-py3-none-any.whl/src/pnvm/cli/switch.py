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
from typing import Literal
from pnvm import console, utils


# NOTE: this function is a quick fix, please help me out with this one.
def _correct_require_path_of(node_script: Literal["npm", "npx", "corepack"]) -> None:
    path = shutil.which(node_script)

    if not path:
        return console.error(f"Failed to find {node_script} location.", fatal=True)

    with open(path, "r+") as f:
        code = f.read()

        # Change relative path to be correct, as to avoid "Module Not Found" errors.
        if node_script == "npm" or node_script == "npx":
            code = code.replace("('../lib/cli.js')", "('../lib/node_modules/npm/lib/cli.js')")

        elif node_script == "corepack":
            code = code.replace("('../lib/corepack.cjs')", "('../lib/node_modules/corepack/dist/corepack.js')")

        # Go to start and overwrite the file(s)
        f.seek(0)
        f.write(code)
        f.truncate()

    return None


def switch(new_version: str) -> None:
    if not utils.is_version_installed(new_version):
        console.error("You tried to select a node version which you don't have installed.", fatal=True)

    current_version = utils.get_selected_node_version()

    if current_version == new_version:
        console.error("You've already selected this version.", fatal=True)

    utils.set_selected_node_version(new_version)
    utils.clear_existing_node_binaries()

    path = utils.get_pnvm_directory_path() / new_version / f"node-{new_version}-linux-x64"

    node_path = utils.get_pnvm_bin_path() / "node-js"
    shutil.copytree(path, node_path)

    _correct_require_path_of("npm")
    _correct_require_path_of("npx")
    _correct_require_path_of("corepack")

    console.ok(f"You're now using node {new_version}.")
