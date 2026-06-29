"""
Configuration Validator

Validates projection configuration files before they are
used by the ETL pipeline.

Responsibilities
----------------
Validate configuration structure
Validate required keys
Validate field mapping
Validate defaults
Raise descriptive configuration errors

"""

from __future__ import annotations

from typing import Any, Dict

from utils.logger import get_logger
from utils.exceptions import ConfigurationError


class ConfigValidator:
    """
    Validates configuration dictionaries.
    """

    logger = get_logger(__name__)

    REQUIRED_TOP_LEVEL_KEYS = [

        "field_mapping",

        "required_fields",

        "defaults"

    ]

    # ---------------------------------------------------------
    # Validate Configuration
    # ---------------------------------------------------------

    @classmethod
    def validate(
        cls,
        config: Dict[str, Any]
    ) -> bool:
        """
        Validates an entire configuration dictionary.
        """

        cls.validate_top_level(config)

        cls.validate_field_mapping(
            config["field_mapping"]
        )

        cls.validate_required_fields(
            config["required_fields"]
        )

        cls.validate_defaults(
            config["defaults"]
        )

        cls.logger.info(
            "Configuration validation successful."
        )

        return True

    # ---------------------------------------------------------
    # Top Level Keys
    # ---------------------------------------------------------

    @classmethod
    def validate_top_level(
        cls,
        config: Dict[str, Any]
    ) -> None:
        """
        Validates required top-level keys.
        """

        for key in cls.REQUIRED_TOP_LEVEL_KEYS:

            if key not in config:

                raise ConfigurationError(

                    f"Missing configuration key: '{key}'"

                )

    # ---------------------------------------------------------
    # Field Mapping
    # ---------------------------------------------------------

    @staticmethod
    def validate_field_mapping(
        mapping: Dict[str, Any]
    ) -> None:
        """
        Validates field mapping section.
        """

        if not isinstance(mapping, dict):

            raise ConfigurationError(

                "field_mapping must be a dictionary."

            )

        if len(mapping) == 0:

            raise ConfigurationError(

                "field_mapping cannot be empty."

            )

        for source_field, target_field in mapping.items():

            if not isinstance(source_field, str):

                raise ConfigurationError(

                    "Invalid source field name."

                )

            if not isinstance(target_field, str):

                raise ConfigurationError(

                    "Invalid target field name."

                )

    # ---------------------------------------------------------
    # Required Fields
    # ---------------------------------------------------------

    @staticmethod
    def validate_required_fields(
        fields: Any
    ) -> None:
        """
        Validates required_fields.
        """

        if not isinstance(fields, list):

            raise ConfigurationError(

                "required_fields must be a list."

            )

        for field in fields:

            if not isinstance(field, str):

                raise ConfigurationError(

                    "Invalid required field."

                )

    # ---------------------------------------------------------
    # Default Values
    # ---------------------------------------------------------

    @staticmethod
    def validate_defaults(
        defaults: Dict[str, Any]
    ) -> None:
        """
        Validates defaults section.
        """

        if not isinstance(defaults, dict):

            raise ConfigurationError(

                "defaults must be a dictionary."

            )

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @classmethod
    def validate_mapping_exists(
        cls,
        config: Dict[str, Any],
        canonical_field: str
    ) -> bool:
        """
        Checks if a canonical field has a mapping.
        """

        mapping = config.get(
            "field_mapping",
            {}
        )

        return canonical_field in mapping

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @classmethod
    def validate_required_mapping(
        cls,
        config: Dict[str, Any]
    ) -> bool:
        """
        Ensures every required field exists in the
        mapping dictionary.
        """

        mapping = config.get(
            "field_mapping",
            {}
        )

        required = config.get(
            "required_fields",
            []
        )

        mapped_fields = set(mapping.values())

        for field in required:

            if field not in mapped_fields:

                raise ConfigurationError(

                    f"Required output field '{field}' "
                    f"is not mapped."

                )

        return True

    # ---------------------------------------------------------
    # Full Validation
    # ---------------------------------------------------------

    @classmethod
    def validate_all(
        cls,
        config: Dict[str, Any]
    ) -> bool:
        """
        Performs complete configuration validation.
        """

        cls.validate(config)

        cls.validate_required_mapping(config)

        cls.logger.info(

            "Complete configuration validation successful."

        )

        return True