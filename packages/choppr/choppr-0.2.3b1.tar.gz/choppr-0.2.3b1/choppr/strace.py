"""Module containing functions to call strace and analyze output."""

from __future__ import annotations

import re

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pathlib import Path


__all__ = ["get_files"]
__author__ = "Jesse Boswell <jesse.a.boswell@lmco.com>"
__copyright__ = "Copyright (C) 2024 Lockheed Martin Corporation"
__license__ = "Lockheed Martin Proprietary Information"


def get_files(strace_location: Path) -> set[str]:
    """Get the list of touched files from strace.

    Arguments:
        strace_location: Output file from strace (default strace_output.txt)

    Returns:
        set[str]: Set of touched files
    """
    with strace_location.open() as file:
        text = file.read()

    flags = re.MULTILINE | re.IGNORECASE

    dir_regex = (
        r"^.*?"
        r"(?:(?:mkdir).*?"
        r"(?:(?:\'|\")(?P<mkdir>.*?)(?:\'|\")))"
        r"|"
        r"(?:(?:(?:\'|\")(?P<dirname>.*?)(?:\'|\"))"
        r"(?=.*?(?:S_IFDIR|O_DIRECTORY))(?!.*(?:ENOENT|unfinished)))"
    )
    dir_matches = re.finditer(dir_regex, text, flags)
    directories: set[str] = {dm.group(g) for dm in dir_matches for g in ["dirname", "mkdir"]}

    regex = r"^.*?(?:(?:\'|\")(?P<filename>.*?)(?:\'|\"))(?!.*(?:S_IFDIR|ENOENT|O_DIRECTORY|unfinished))"
    return {match.group("filename") for match in re.finditer(regex, text, flags)} - directories
