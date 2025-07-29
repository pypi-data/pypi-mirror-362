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

import tarfile
import sys

from pathlib import Path

import requests

from pnvm import console, utils
from pnvm.verification import VerificationStatus, verify_node_version
from pnvm.constants import BASE_INSTALL_URL


# Extract tar archive at `tar_path` to the directory
# `tar_path` is located in.
def _extract_tar_gz(tar_path: Path) -> None:
    extraction_path = tar_path.parent

    with tarfile.open(tar_path) as tar:
        tar.extractall(path=extraction_path, filter="data")


# Clean up useless garbage if the request to download
# the node archive fails.
def _cleanup_on_req_failure(path_to_remove: Path) -> None:
    Path.rmdir(path_to_remove)
    sys.exit(1)


# Some, especially those with a background in OOP, will see this as an
# anti-pattern, however, I believe this improves readability and organizes
# the code. Feel free to flame me if you disagree, or, even better, open a merge
# request on GitLab and help me out.
# Sorry for ranting...
class InstallStep:
    @staticmethod
    def fetch_node_tar(install_path: Path, node_version: str) -> requests.Response:
        """Fetches the specified version of a Node.js tar.gz"""

        response: requests.Response | None = None

        # Non-linux-x64 platforms may be supported in the future...
        # (I apologize to users using Mac, Windows and Raspberry Pi,
        # although if you're using Windows you should probably stop
        # reading the source code and get f'kn going installing
        # GNU/Linux. (see https://endof10.org/))

        target = f"node-{node_version}-linux-x64.tar.gz"
        url = f"{BASE_INSTALL_URL}/{node_version}/{target}"

        try:
            # --- Request initiated here ---
            response = requests.get(url, stream=True)

            # Needed for catching HTTP-related exceptions
            response.raise_for_status()

        except requests.exceptions.HTTPError as http_error:
            console.error(str(http_error))
            _cleanup_on_req_failure(install_path)

        except requests.exceptions.ConnectionError as connection_error:
            console.error(f"Connection Error: {connection_error}")
            _cleanup_on_req_failure(install_path)

        except requests.exceptions.Timeout as timeout_error:
            console.error(f"Timed out: {timeout_error}")
            _cleanup_on_req_failure(install_path)

        except requests.exceptions.RequestException as req_error:
            console.error(f"Request Error: {req_error}")
            _cleanup_on_req_failure(install_path)

        console.ok(f"Fetched Node.js {node_version} successfully.")

        # Yet another appeasement to Pylance...
        assert response
        return response

    @staticmethod
    def write_tar(response: requests.Response, tar_path: Path) -> None:
        """Writes the installed tar archive to the ~/.pnvm directory"""

        # Write the tar.gz file to the correct path
        with open(str(tar_path), "wb") as file:
            if not response:
                console.error("Bad response received.", fatal=True)
                return

            file.write(response.raw.read())

    @staticmethod
    def verify_installed_tar_archive(node_version: str) -> None:
        """Verifies the integrity of the installed tar archive"""

        console.log("Verifying the downloaded archive...")

        status = verify_node_version(node_version)

        if status == VerificationStatus.MISMATCH:
            console.error("Failed to verify the integrity of downloaded archive.", fatal=True)
        elif status == VerificationStatus.REQUEST_ERROR:
            console.error("Failed to complete request to fetch SHASUMS256.txt file.", fatal=True)
        elif status == VerificationStatus.RESPONSE_ERROR:
            console.error("Malformed response.", fatal=True)
        elif status == VerificationStatus.NO_DIGEST_FOUND:
            console.error("Couldn't find any hash associated with this version.")
            console.log(
                "If you believe that this was a mistake on behalf of the CLI, please open an issue on GitLab.",
                bold=True,
                to_stderr=True,
            )
            sys.exit(1)
        elif status == VerificationStatus.TAR_NOT_FOUND:
            console.error("Failed to find the tar archive to verify.", fatal=True)
        else:
            console.ok("Verified integrity of node archive.")

    @staticmethod
    def extract_installed_tar_archive(tar_path: Path) -> None:
        # Extract tar file archive
        try:
            _extract_tar_gz(tar_path)
        except Exception as e:
            console.error("Failed to extract tar archive.")
            console.log(f"DETAILS: {e}", to_stderr=True)
            sys.exit(1)

        console.ok("Extracted tar.gz archive successfully.")


# --- This is the function you're looking for ---
def install(version: str) -> None:
    install_path = utils.get_pnvm_directory_path() / version

    tar_path = install_path / "archive.tar.gz"

    # This is an indication of an unsucessful previous installation.
    if tar_path.exists():
        console.log("NOTE: ", bold=True, end="")
        console.log(
            "You've already downloaded the node archive for this version, but it seems like\n"
            + "either the verification or extraction process had previously failed.\n"
            + "PNVM will now retry to install this version of node.\n"
            + "----------------------------------------------------"
        )

        InstallStep.verify_installed_tar_archive(version)
        InstallStep.extract_installed_tar_archive(tar_path)
        return

    # Node version is already installed.
    if install_path.exists():
        console.error("It seems like you've already got this version installed.", fatal=True)

    Path.mkdir(install_path)

    # ---

    response = InstallStep.fetch_node_tar(install_path, version)

    InstallStep.write_tar(response, tar_path)
    InstallStep.verify_installed_tar_archive(version)
    InstallStep.extract_installed_tar_archive(tar_path)

    console.log("Done.")
