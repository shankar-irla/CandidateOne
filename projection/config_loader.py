"""
Configuration Loader

Loads projection configuration files used by the output
mapper.

Responsibilities
----------------
Load default configuration
Load custom configuration
Validate configuration format
Provide mapping access
Support future configuration extensions

"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from utils.logger import get_logger
from utils.exceptions import (
    ConfigurationError,
    FileMissingError
)


class ConfigLoader:
    """
    Loads projection configuration files.
    """

    def __init__(
        self,
        config_path: str | Path
    ):

        self.config_path = Path(config_path)

        self.logger = get_logger(__name__)

        self.config: Dict[str, Any] = {}

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def exists(self) -> bool:
        """
        Checks whether the configuration file exists.
        """

        return self.config_path.exists()

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    def load(self) -> Dict[str, Any]:
        """
        Loads the JSON configuration file.
        """

        if not self.exists():

            raise FileMissingError(
                str(self.config_path)
            )

        try:

            with open(
                self.config_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.config = json.load(file)

            self.logger.info(
                "Configuration loaded: %s",
                self.config_path.name
            )

            return self.config

        except json.JSONDecodeError as exc:

            raise ConfigurationError(
                f"Invalid JSON configuration: {exc}"
            ) from exc

    # ---------------------------------------------------------
    # Get Mapping
    # ---------------------------------------------------------

    def get_mapping(self) -> Dict[str, str]:
        """
        Returns the field mapping dictionary.
        """

        return self.config.get(
            "field_mapping",
            {}
        )

    # ---------------------------------------------------------
    # Get Defaults
    # ---------------------------------------------------------

    def get_defaults(self) -> Dict[str, Any]:
        """
        Returns default field values.
        """

        return self.config.get(
            "defaults",
            {}
        )

    # ---------------------------------------------------------
    # Get Required Fields
    # ---------------------------------------------------------

    def get_required_fields(self) -> list:
        """
        Returns required output fields.
        """

        return self.config.get(
            "required_fields",
            []
        )

    # ---------------------------------------------------------
    # Generic Getter
    # ---------------------------------------------------------

    def get(
        self,
        key: str,
        default: Optional[Any] = None
    ) -> Any:
        """
        Returns a configuration value.
        """

        return self.config.get(
            key,
            default
        )

    # ---------------------------------------------------------
    # Reload
    # ---------------------------------------------------------

    def reload(self) -> Dict[str, Any]:
        """
        Reloads the configuration from disk.
        """

        self.logger.info(
            "Reloading configuration..."
        )

        return self.load()

    # ---------------------------------------------------------
    # String Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"ConfigLoader("
            f"path='{self.config_path}')"
        )