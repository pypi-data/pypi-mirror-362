"""PackagesFile implementation."""

from __future__ import annotations

import json

from typing import TYPE_CHECKING

from choppr.apt_api._utils import get_value
from choppr.apt_api.binary_package import BinaryPackage


if TYPE_CHECKING:
    from pathlib import Path


__all__ = ["PackagesFile"]
__author__ = "Jesse Boswell <jesse.a.boswell@lmco.com>"
__copyright__ = "Copyright (C) 2024 Lockheed Martin Corporation"
__license__ = "MIT License"


class PackagesFile:
    """Class that represents a Packages file."""

    def __init__(self, packages_file: Path, content_file: Path, repo_url: str) -> None:
        """Initialize an instance of PackagesFile.

        Arguments:
            packages_file: The list of packages with their metadata
            content_file: The list of files internal to this specific package
            repo_url: The URL for the repository
        """
        self.packages: list[BinaryPackage] = []

        if packages_file.is_file():
            with packages_file.open(encoding="utf-16") as f:
                content = f.read().strip()

            with content_file.open() as f:
                file_list: dict[str, list[str]] = json.load(f)

            if packages_content := content.split("\n\n"):
                for package_content in packages_content:
                    if package_content:
                        name = str(get_value(package_content, "Package"))
                        if name in file_list:
                            bp = BinaryPackage(package_content, file_list[name], repo_url)
                        else:
                            bp = BinaryPackage(package_content, package_url=repo_url)

                        self.packages.append(bp)
