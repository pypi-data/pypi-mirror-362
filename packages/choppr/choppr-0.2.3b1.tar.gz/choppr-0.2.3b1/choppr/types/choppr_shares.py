"""Class definition for ChopprShares, a singleton class to share commonly access objects."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hoppr import PurlType


if TYPE_CHECKING:
    from hoppr import Component, HopprContext, HopprLogger
    from typing_extensions import Self

    from choppr.types import ChopprConfig


__all__ = ["ChopprShares"]
__author__ = "Jesse Boswell <jesse.a.boswell@lmco.com>"
__copyright__ = "Copyright (C) 2024 Lockheed Martin Corporation"
__license__ = "MIT License"


class ChopprShares:
    """Singleton class to hold commonly accessed Choppr objects.

    Members:
        - components
        - config
        - context
        - log

    Methods:
        - initialized
    """

    _instance: ChopprShares | None = None

    def __new__(cls, config: ChopprConfig, context: HopprContext, log: HopprLogger, *args, **kwargs) -> Self:
        """Initialize ChopprShares singleton.

        Arguments:
            config: Instance of ChopprConfig
            context: Instance of HopprContext
            log: Instance of HopprLogger

        Returns:
            Self: Singleton instance of ChopprShares
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

            cls.components: dict[PurlType, list[Component]] = {
                purl_type: [
                    component
                    for component in context.delivered_sbom.components
                    if component.purl and component.purl.lower().startswith(f"pkg:{purl_type.value.lower()}")
                ]
                for purl_type in PurlType
            }
            cls.config: ChopprConfig = config
            cls.context: HopprContext = context
            cls.log: HopprLogger = log

            for purl_type, component_list in cls.components.items():
                cls.log.debug(f"{purl_type.name} component count: {len(component_list)}")
        return cls._instance

    @classmethod
    def initialized(cls) -> bool:
        """Check if the class has been initialized.

        Returns:
            bool: True if the class is initialized, otherwise False
        """
        return cls._instance is not None
