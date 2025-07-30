"""Choppr refines the components in a Software Bill of Materials (SBOM).

It does not replace SBOM generation tools.  Mainly, Choppr analyses a build or runtime to verify
which components are used, and remove the SBOM components not used.  Starting with file accesses, it
works backwards from how an SBOM generation tool typically would.  For example SBOM generators use
the yum database to determine which packages yum installed.  Choppr looks at all the files accessed
and queries sources like yum to determine the originating package.
"""

from __future__ import annotations

import shutil

from typing import TYPE_CHECKING, Any

from hoppr import (
    BomAccess,
    ComponentType,
    HopprLoadDataError,
)
from hoppr.base_plugins.hoppr import HopprPlugin, hoppr_process
from hoppr.models.types import PurlType
from hoppr.result import Result
from hoppr_cyclonedx_models.cyclonedx_1_6 import Scope

from choppr import __version__
from choppr.deb_handler import DebHandler
from choppr.rpm_handler import RpmHandler
from choppr.types import ChopprConfig, ChopprConfigModel, ChopprShares
from choppr.utils import get_component_type, log_header, output_list


if TYPE_CHECKING:
    from hoppr import Component, HopprContext, Sbom


__all__ = ["ChopprPlugin"]
__author__ = "Jesse Boswell <jesse.a.boswell@lmco.com>"
__copyright__ = "Copyright (C) 2024 Lockheed Martin Corporation"
__license__ = "MIT License"


class ChopprPlugin(HopprPlugin):
    """Plugin implementation of Choppr to integrate with Hoppr."""

    supported_purl_types = ["rpm", "deb"]  # noqa: RUF012
    products = []  # noqa: RUF012
    bom_access = BomAccess.FULL_ACCESS

    def __init__(self, context: HopprContext, config: dict[Any, Any] | None = None) -> None:
        """Initialize plugin with Hoppr framework arguments (context and config).

        Arguments:
            context: Hoppr context
            config: Hoppr configuration
        """
        super().__init__(context, config)

        self.log = self.get_logger()
        self.log.flush_immed = True

        # Parse configuration
        self.valid_config = False
        try:
            plugin_config = ChopprConfig(ChopprConfigModel.parse_obj(config))
            ChopprShares(plugin_config, self.context, self.log)
            self.valid_config = True
        except (HopprLoadDataError, FileNotFoundError) as e:
            self.log.error(f"Invalid Configuration: {e}")  # noqa: TRY400

        self.file_provided_by: dict[str, str] = {}
        self.search_repositories = dict.fromkeys(PurlType, False)

        self.rpm = RpmHandler()
        self.deb = DebHandler()

    def get_version(self) -> str:  # noqa: PLR6301
        """Return the version of the Choppr plugin.

        Returns:
            str: Plugin version
        """
        return __version__

    ################################################################################################
    # Pre-Stage Process
    ################################################################################################

    @hoppr_process
    def pre_stage_process(self) -> Result:
        """Collect repository information.

        Returns:
            Result: Skip if the config is invalid, or the modified SBOM
        """
        if not self.valid_config:
            return Result.skip()

        self._output_excluded_components([])

        self._populate_repositories()
        self._populate_potential_packages()
        self._populate_required_packages()
        self._populate_nested_dependencies()

        choppd_sbom = self._filter_sbom()

        self._output_excluded_components(choppd_sbom.components)

        return Result.success(return_obj=choppd_sbom)

    def _populate_repositories(self) -> None:
        log_header("Populate Repositories")
        self.search_repositories[PurlType.RPM] = self.rpm.populate_repositories()
        self.search_repositories[PurlType.DEB] = self.deb.populate_repositories()

    def _populate_potential_packages(self, required_files: set[str] | None = None) -> None:
        log_header("Populate Potential Packages")
        using_strace_files = False

        if not required_files:
            using_strace_files = True
            required_files = ChopprShares.config.strace_files

        for file in required_files:
            if self.search_repositories[PurlType.RPM]:
                self.rpm.populate_potential_packages(file, using_strace_files)
            if self.search_repositories[PurlType.DEB]:
                self.deb.populate_potential_packages(file)

        if self.search_repositories[PurlType.RPM]:
            ChopprShares.log.info(f"Found {len(self.rpm.potential_packages)} potential rpm packages")

            with ChopprShares.config.cache_dir.joinpath("rpm", "potential_packages.txt").open("w") as output:
                output.writelines([f"{pkg}\n" for pkg in sorted(self.rpm.potential_packages, key=lambda p: p.name)])

        if self.search_repositories[PurlType.DEB]:
            ChopprShares.log.info(f"Found {len(self.deb.potential_packages)} potential deb packages")

            with ChopprShares.config.cache_dir.joinpath("deb", "potential_packages.txt").open("w") as output:
                output.writelines([f"{pkg}\n" for pkg in sorted(self.deb.potential_packages, key=lambda p: p.name)])

    def _populate_required_packages(self) -> None:
        log_header("Populate Required Packages")

        if self.search_repositories[PurlType.RPM]:
            self.rpm.populate_required_packages()
        if self.search_repositories[PurlType.DEB]:
            self.deb.populate_required_packages()

    def _populate_nested_dependencies(self) -> None:
        log_header("Populate Nested Dependencies")

        if self.search_repositories[PurlType.RPM]:
            self.rpm.populate_all_nested_dependencies()
        if self.search_repositories[PurlType.DEB]:
            self.deb.populate_all_nested_dependencies()

    def _filter_sbom(self) -> Sbom:
        log_header("Filter SBOM")
        choppd_sbom = ChopprShares.context.delivered_sbom.copy(deep=True)
        choppd_sbom.components.clear()

        for component in ChopprShares.context.delivered_sbom.components or []:
            component_id = f"{component.name}-{component.version}"

            if component_type := get_component_type(component):
                if (
                    component_type in ChopprShares.config.allowlist
                    and component in ChopprShares.config.allowlist[component_type]
                ):
                    component.scope = Scope.REQUIRED
                    ChopprShares.log.info(f"Component accepted by allowlist: {component_id}")
                    choppd_sbom.components.append(component)
                    continue
                if (
                    component_type in ChopprShares.config.denylist
                    and component in ChopprShares.config.denylist[component_type]
                ):
                    component.scope = Scope.EXCLUDED
                    ChopprShares.log.info(f"Component blocked by denylist: {component_id}")
                    continue

            if component_scope := self._get_component_scope(component):
                component.scope = component_scope
                match component_scope:
                    case Scope.REQUIRED:
                        ChopprShares.log.info(f"Component required: {component_id}")
                        choppd_sbom.components.append(component)
                    case Scope.EXCLUDED:
                        ChopprShares.log.info(f"Component not required: {component_id}")
            else:
                ChopprShares.log.warning(f"Unable to determine if component is required: {component_id}")

        if ChopprShares.config.delete_excluded:
            ChopprShares.log.debug("Deleted excluded components")
            return choppd_sbom
        return ChopprShares.context.delivered_sbom

    @staticmethod
    def _output_excluded_components(filtered_components: list[Component]) -> None:
        excluded_components_all = [
            c for c in ChopprShares.context.delivered_sbom.components if c not in filtered_components
        ]

        for purl_type in PurlType:
            output_format = ChopprShares.config.output_files.excluded_components[purl_type].component_format
            if excluded_components := [
                output_format.format(**c.dict()) for c in excluded_components_all if get_component_type(c) is purl_type
            ]:
                output_file = ChopprShares.config.output_files.excluded_components[purl_type].file
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_list(output_file, excluded_components)

    def _get_component_scope(self, component: Component) -> Scope | None:
        if ChopprShares.config.keep_essential_os_components and component.type is ComponentType.OPERATING_SYSTEM:
            return Scope.REQUIRED
        if not ChopprShares.config.allow_version_mismatch and not component.version:
            return None
        return next(
            (
                Scope.REQUIRED
                for package in self.rpm.required_packages
                | self.rpm.nested_dependencies
                | self.deb.required_packages
                | self.deb.nested_dependencies
                if (ChopprShares.config.allow_version_mismatch and str(package).startswith(component.name))
                or str(package) == f"{component.name}-{component.version}"
            ),
            Scope.EXCLUDED,
        )

    ################################################################################################
    # Post-Stage Process
    ################################################################################################

    @hoppr_process
    def post_stage_process(self) -> Result:
        """Perform cleanup tasks after running Choppr.

        Returns:
            Result: The updated SBOM with the unused packages removed
        """
        if not self.valid_config:
            return Result.skip()

        if ChopprShares.config.clear_cache:
            shutil.rmtree(ChopprShares.config.cache_dir)

        return Result.success()
