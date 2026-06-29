"""
Schema Validator

Validates canonical and projected candidate profiles against
the expected schema.

Responsibilities
----------------
Validate candidate schema
Validate projected schema
Validate required fields
Raise descriptive validation errors
"""

from __future__ import annotations

from typing import Dict, Any

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from utils.logger import get_logger
from utils.exceptions import SchemaValidationError


class SchemaValidator:
    """
    Validates candidate profiles using JSON Schema.
    """

    logger = get_logger(__name__)

    # ---------------------------------------------------------
    # Canonical Candidate Schema
    # ---------------------------------------------------------

    CANONICAL_SCHEMA = {

        "type": "object",

        "properties": {

            "candidate_id": {
                "type": ["string", "null"]
            },

            "full_name": {
                "type": ["string", "null"]
            },

            "emails": {
                "type": "array"
            },

            "phones": {
                "type": "array"
            },

            "headline": {
                "type": ["string", "null"]
            },

            "years_experience": {
                "type": ["number", "null"]
            },

            "skills": {
                "type": "array"
            },

            "location": {
                "type": "object"
            },

            "experience": {
                "type": "array"
            },

            "education": {
                "type": "array"
            },

            "links": {
                "type": "object"
            },

            "provenance": {
                "type": "object"
            },

            "overall_confidence": {
                "type": ["number", "null"]
            }
        },

        "required": [

            "full_name",

            "emails",

            "phones",

            "skills"

        ]
    }

    # ---------------------------------------------------------
    # Validate Generic Schema
    # ---------------------------------------------------------

    @classmethod
    def validate_schema(
        cls,
        candidate: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> bool:
        """
        Validates an object against a schema.
        """

        try:

            validate(
                instance=candidate,
                schema=schema
            )

            cls.logger.info(
                "Schema validation successful."
            )

            return True

        except ValidationError as exc:

            cls.logger.error(
                "Schema validation failed: %s",
                exc.message
            )

            raise SchemaValidationError(
                exc.message
            ) from exc

    # ---------------------------------------------------------
    # Canonical Candidate
    # ---------------------------------------------------------

    @classmethod
    def validate_candidate(
        cls,
        candidate: Dict[str, Any]
    ) -> bool:
        """
        Validates canonical candidate.
        """

        return cls.validate_schema(

            candidate,

            cls.CANONICAL_SCHEMA

        )

    # ---------------------------------------------------------
    # Projected Candidate
    # ---------------------------------------------------------

    @classmethod
    def validate_projected(
        cls,
        candidate: Dict[str, Any],
        config: Dict[str, Any]
    ) -> bool:
        """
        Validates projected candidate.

        Uses required_fields from configuration.
        """

        required = config.get(

            "required_fields",

            []

        )

        for field in required:

            if field not in candidate:

                raise SchemaValidationError(

                    f"Missing required field: {field}"

                )

        cls.logger.info(

            "Projected profile validation successful."

        )

        return True

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def has_required_fields(
        candidate: Dict[str, Any],
        fields: list
    ) -> bool:
        """
        Checks if all required fields exist.
        """

        for field in fields:

            if field not in candidate:

                return False

        return True