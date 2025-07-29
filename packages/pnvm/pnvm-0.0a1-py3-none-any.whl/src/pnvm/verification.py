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

import enum
import hashlib

from typing import List

import requests

from .constants import BASE_INSTALL_URL, CHUNK_SIZE_BYTES
from .utils import get_pnvm_directory_path


class VerificationStatus(enum.Enum):
    OK = 0
    MISMATCH = 1
    REQUEST_ERROR = 2
    RESPONSE_ERROR = 3
    NO_DIGEST_FOUND = 4
    TAR_NOT_FOUND = 5


def _find_matching_node_version_in_shasum_file(contents: str, node_version: str) -> str | None:
    chunks: List[str] = []

    for chunk in contents.split():
        if chunk == f"node-{node_version}-linux-x64.tar.gz":
            return chunks[-1].strip()

        chunks.append(chunk)
    return None


def verify_node_version(node_version: str) -> VerificationStatus:
    # --- Fetch SHASUMS256.txt file ---

    url = f"{BASE_INSTALL_URL}/{node_version}/SHASUMS256.txt"

    response: requests.Response | None = None

    try:
        # --- Request initiated here ---
        response = requests.get(url, stream=True)

        # Needed for catching HTTP-related exceptions
        response.raise_for_status()

    except requests.exceptions.RequestException:
        return VerificationStatus.REQUEST_ERROR

    if not response:
        return VerificationStatus.RESPONSE_ERROR

    # --- Hash-matching ---

    node_digest = _find_matching_node_version_in_shasum_file(response.text, node_version)

    # No digest was found alongside the node version provided.
    if not node_digest:
        return VerificationStatus.NO_DIGEST_FOUND

    path_to_archive = get_pnvm_directory_path() / node_version / "archive.tar.gz"

    if not path_to_archive.exists():
        return VerificationStatus.TAR_NOT_FOUND

    hasher = hashlib.sha256()

    # Iterate over chunks and update the hash for each chunk.
    with open(str(path_to_archive), "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE_BYTES), b""):
            hasher.update(chunk)

    if hasher.hexdigest() == node_digest:
        return VerificationStatus.OK

    return VerificationStatus.MISMATCH
