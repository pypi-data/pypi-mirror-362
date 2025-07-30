"""Class definition for ChopprConfig."""

from __future__ import annotations

import re

from datetime import timedelta
from hashlib import sha256
from pathlib import Path
from typing import Any

from hoppr import Component, PurlType
from pydantic import (  # noqa: TC002
    BaseModel,
    Field,
    HttpUrl,
    PositiveFloat,
    PositiveInt,
    PrivateAttr,
    parse_obj_as,
    validator,
)

from choppr import strace
from choppr.constants import COMPONENT_LIST_FORMATS, DEFAULT_RECURSION_LIMIT


__all__ = ["ChopprConfig", "ChopprConfigModel", "DebianDistribution", "DebianRepository"]
__author__ = "Jesse Boswell <jesse.a.boswell@lmco.com>"
__copyright__ = "Copyright (C) 2024 Lockheed Martin Corporation"
__license__ = "MIT License"


def _validate_file_path(value: str) -> Path:
    path = Path(value)

    if not path.is_file():
        raise ValueError(f"File does not exist: {path}")
    return path


def _validate_http_url(value: str) -> HttpUrl:
    return parse_obj_as(HttpUrl, value.rstrip("/"))


def _validate_regex(value: str) -> re.Pattern:
    try:
        return re.compile(value)
    except re.error as e:
        raise ValueError(f"Invalid regular expression: {value}") from e


def _default_excluded_components() -> dict[PurlType, ExcludedComponentsFile]:
    return {
        purl_type: ExcludedComponentsFile(
            file=Path(f"choppr_excluded_components_{purl_type.name.lower()}.txt"),
            component_format=COMPONENT_LIST_FORMATS.get(purl_type, "{name}={version}"),
        )
        for purl_type in PurlType
    }


class Certificate(BaseModel):
    # Required Attributes
    url: str
    certificate: Path

    # Validators
    _validate_certificate = validator("certificate", pre=True, allow_reuse=True)(_validate_file_path)


class DebianDistribution(BaseModel):
    """Class representation for a debian distribution, to include its name and components.

    Members:
        - name
        - components
    """

    name: str
    components: list[str]


class DebianRepository(BaseModel):
    """Class representation for a debian repository, to include its URL and distributions.

    Members:
        - url
        - distributions
    """

    url: HttpUrl
    distributions: list[DebianDistribution]

    _validate_url = validator("url", pre=True, allow_reuse=True)(_validate_http_url)


class HttpRequestLimits(BaseModel):
    """Class with values to configure HTTP request limits.

    Members:
        - retries
        - retry_interval
        - timeout
    """

    retries: PositiveInt = 3
    retry_interval: PositiveFloat = 5.0
    timeout: PositiveFloat = 60.0


class ExcludedComponentsFile(BaseModel):
    """The filename to output excluded components to, and what format to write them as.

    Members:
        - file
        - format
    """

    file: Path
    component_format: str = ""


class OutputFiles(BaseModel):
    """Class with values for the output files for Choppr.

    Members:
        - excluded_components
    """

    excluded_components: dict[PurlType, ExcludedComponentsFile] = Field(default_factory=_default_excluded_components)

    @validator("excluded_components", pre=True, allow_reuse=True)
    @classmethod
    def _validate_excluded_components(cls, value: dict[str, dict[str, str]]) -> dict[PurlType, ExcludedComponentsFile]:
        excluded_components: dict[PurlType, ExcludedComponentsFile] = _default_excluded_components()
        try:
            for purl, file_and_format in value.items():
                purl_type = PurlType[purl.upper()]
                excluded_components_file = ExcludedComponentsFile(**file_and_format)
                excluded_components[purl_type].file = excluded_components_file.file
                if excluded_components_file.component_format:
                    excluded_components[purl_type].component_format = excluded_components_file.component_format
        except KeyError as e:
            raise ValueError(
                f"Invalid purl type: {e} - Accpeted values: [{', '.join(m.name for m in PurlType)}]"
            ) from e
        else:
            return excluded_components


class PackagePattern(BaseModel):
    """Class with the name, version, and purl type for a package.

    Members:
        - name
        - version
    """

    name: re.Pattern
    version: re.Pattern

    _validate_patterns = validator("name", "version", pre=True, allow_reuse=True)(_validate_regex)

    def __eq__(self, other: PackagePattern | Component) -> bool:
        if isinstance(other, PackagePattern):
            return self.name == other.name and self.version == other.version
        if isinstance(other, Component):
            return self.name.match(other.name) and self.version.match(other.version)
        return False

    def __hash__(self) -> int:
        sha = sha256()
        sha.update(str(self.name).encode())
        sha.update(str(self.version).encode())
        return int(sha.hexdigest(), 16)


class ChopprConfigModel(BaseModel):
    """Class to validate and parse the configuration values provided to ChopprPlugin.

    Members:
        - strace_results
        - allow_version_mismatch
        - allowlist
        - cache_dir
        - cache_timeout
        - certificates
        - clear_cache
        - deb_repositories
        - delete_excluded
        - denylist
        - http_limits
        - keep_essential_os_components
        - output_files
        - recursion_limit
        - strace_regex_excludes

    Methods:
        - strace_files
    """

    HttpRequestLimits.update_forward_refs()

    # Required Attributes
    strace_results: Path
    # Optional Attributes
    allow_version_mismatch: bool = False
    allowlist: dict[PurlType, set[PackagePattern]] = Field(default={})
    cache_dir: Path = Field(default_factory=lambda: Path.cwd() / ".cache" / "choppr")
    cache_timeout: timedelta = Field(default=timedelta(days=7))
    certificates: dict[str, Path] = Field(default={})
    clear_cache: bool = False
    deb_repositories: list[DebianRepository] = Field(default=[])
    delete_excluded: bool = True
    denylist: dict[PurlType, set[PackagePattern]] = Field(default={})
    http_limits: HttpRequestLimits = Field(default=HttpRequestLimits())
    keep_essential_os_components: bool = False
    output_files: OutputFiles = Field(default=OutputFiles())
    recursion_limit: PositiveInt = DEFAULT_RECURSION_LIMIT
    strace_regex_excludes: list[re.Pattern] = Field(default=[])
    # Private Attributes
    _strace_files: set[str] = PrivateAttr(default=set())

    # Validators
    _validate_strace_results = validator("strace_results", allow_reuse=True)(_validate_file_path)
    _validate_strace_regex_excludes = validator("strace_regex_excludes", pre=True, each_item=True, allow_reuse=True)(
        _validate_regex
    )

    @validator("cache_timeout", pre=True, allow_reuse=True)
    @classmethod
    def _validate_cache_timeout(cls, cache_timeout: str) -> timedelta:
        timedelta_pattern = re.compile(r"^(?P<duration>\d+)\s?(?P<unit>d|h|m|s)$", re.IGNORECASE)

        timeout_match = timedelta_pattern.match(cache_timeout)

        error_message = "Invalid 'cache_timeout' value: Expected a number followed by a unit (d, h, m, s)"

        if not timeout_match:
            raise ValueError(error_message)

        timeout_duration = int(timeout_match["duration"])
        timeout_unit = timeout_match["unit"].lower()

        unit_map = {
            "d": "days",
            "h": "hours",
            "m": "minutes",
            "s": "seconds",
        }

        if timeout_unit not in unit_map:
            raise ValueError(error_message)

        return timedelta(**{unit_map[timeout_unit]: timeout_duration})

    @validator("certificates", pre=True, allow_reuse=True)
    @classmethod
    def _validate_certificates(cls, certificates: list[dict[str, str]]) -> dict[str, Path]:
        certificate_map: dict[str, Path] = {}

        for certificate in certificates:
            c = Certificate(**certificate)
            certificate_map[c.url] = c.certificate

        return certificate_map

    @validator("allowlist", "denylist", pre=True, allow_reuse=True)
    @classmethod
    def _validate_exception_list(cls, value: dict[str, set[PackagePattern]]) -> dict[PurlType, set[PackagePattern]]:
        try:
            return {PurlType[purl_type.upper()]: packages for purl_type, packages in value.items()}
        except KeyError as e:
            raise ValueError(
                f"Invalid purl type: {e} - Accpeted values: [{', '.join(m.name for m in PurlType)}]"
            ) from e

    @validator("denylist", allow_reuse=True)
    @classmethod
    def _validate_exception_overlap(
        cls, denylist: dict[PurlType, set[PackagePattern]], values: dict[str, Any]
    ) -> dict[PurlType, set[PackagePattern]]:
        allowlist: dict[PurlType, set[PackagePattern]] = values.get("allowlist")

        for purl_type in PurlType:
            if allowlist.get(purl_type, set()) & denylist.get(purl_type, set()):
                raise ValueError(f"The allowlist and denylist have at least one overlapping {purl_type.name} package")

        return denylist

    def strace_files(self) -> set[str]:
        """List of files parsed from the provided strace results.

        Returns:
            set[str]: List of files found from strace
        """
        if not self._strace_files:
            parsed_strace_files = strace.get_files(self.strace_results)

            if self.strace_regex_excludes:
                self._strace_files = {
                    file
                    for file in parsed_strace_files
                    if not any(bool(re.search(exclude, file)) for exclude in self.strace_regex_excludes)
                }
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                with self.cache_dir.joinpath("filtered_strace_results.txt").open("w") as output:
                    output.writelines([f"{file}\n" for file in self._strace_files])
            else:
                self._strace_files = parsed_strace_files

        return self._strace_files


class ChopprConfig:
    """A class to store the Choppr configuration.

    Members:
        - allow_version_mismatch
        - allowlist
        - cache_dir
        - cache_timeout
        - certificates
        - clear_cache
        - deb_repositories
        - delete_excluded
        - denylist
        - http_limits
        - keep_essential_os_components
        - output_files
        - recursion_limit
        - strace_files
    """

    def __init__(self, model: ChopprConfigModel) -> None:
        self.allow_version_mismatch: bool = model.allow_version_mismatch
        self.allowlist: dict[PurlType, list[PackagePattern]] = model.allowlist
        self.cache_dir: Path = model.cache_dir
        self.cache_timeout: timedelta = model.cache_timeout
        self.certificates: dict[str, Path] = model.certificates
        self.clear_cache: bool = model.clear_cache
        self.deb_repositories: list[DebianRepository] = model.deb_repositories
        self.delete_excluded: bool = model.delete_excluded
        self.denylist: dict[PurlType, list[PackagePattern]] = model.denylist
        self.http_limits: HttpRequestLimits = model.http_limits
        self.keep_essential_os_components: bool = model.keep_essential_os_components
        self.output_files: OutputFiles = model.output_files
        self.recursion_limit: PositiveInt = model.recursion_limit
        self.strace_files: set[str] = model.strace_files()
