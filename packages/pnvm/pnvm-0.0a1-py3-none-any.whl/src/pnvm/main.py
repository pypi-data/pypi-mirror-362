#!/usr/bin/env python3
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

import argparse

import utils
import console

from .cli.install import install as cli_install
from .cli.remove import remove as cli_remove
from .cli.switch import switch as cli_switch
from .cli.list import list_versions as cli_list
from .cli.which import which as cli_which


def create_parser() -> argparse.ArgumentParser:
    # --- Argument parsing ---
    parser = argparse.ArgumentParser(prog="pnvm", description="Manages Node.js installations")

    parser.add_argument("--install", "-i", help="install a specific node version")

    parser.add_argument("--remove", "-r", help="remove specific node version")

    parser.add_argument("--switch", "-c", help="switch between node installations")

    parser.add_argument("--version", "-v", help="show CLI version number", action="store_true")

    parser.add_argument("--shut-up", "-q", help="tell the CLI to keep its mouth shut", action="store_true")

    parser.add_argument("--list-versions", "-l", help="list node installations", action="store_true")

    parser.add_argument("--which", "-w", help="see which node version is currently active", action="store_true")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # --- Interesting stuff (I hope) ---

    # --- Set up PNVM ---
    utils.setup_pnvm()

    # -- Flags --

    # Silence output if instructed to
    if args.shut_up:
        console.silenced = True

    if args.which:
        return cli_which()
    if args.list_versions:
        return cli_list()

    if args.version:
        cli_version = utils.get_cli_version()
        return console.log(cli_version)

    if args.install:
        return cli_install(args.install)
    if args.remove:
        return cli_remove(args.remove)
    if args.switch:
        return cli_switch(args.switch)

    # --- If no args were provided ---
    parser.print_usage()
    return 1
