"""
Canonical Schema

Defines the fixed internal schema used throughout the CandidateOne
pipeline. Every extractor, normalizer, merger and projection layer
works with this schema before any custom output mapping is applied.

"""

from copy import deepcopy
from typing import Dict, Any


# ---------------------------------------------------------
# Canonical Candidate Schema
# ---------------------------------------------------------

CANONICAL_SCHEMA: Dict[str, Any] = {
    "candidate_id": None,

    "full_name": None,

    "emails": [],

    "phones": [],

    "location": {
        "city": None,
        "region": None,
        "country": None
    },

    "links": {
        "linkedin": None,
        "github": None,
        "portfolio": None,
        "other": []
    },

    "headline": None,

    "years_experience": None,

    "skills": [],

    "experience": [],

    "education": [],

    "provenance": {},

    "overall_confidence": 0.0
}


# ---------------------------------------------------------
# JSON Schema Validation Rules
# ---------------------------------------------------------

JSON_SCHEMA = {
    "type": "object",

    "required": [
        "candidate_id",
        "full_name",
        "emails",
        "phones",
        "location",
        "links",
        "headline",
        "years_experience",
        "skills",
        "experience",
        "education",
        "provenance",
        "overall_confidence"
    ],

    "properties": {

        "candidate_id": {
            "type": ["string", "null"]
        },

        "full_name": {
            "type": ["string", "null"]
        },

        "emails": {
            "type": "array",
            "items": {"type": "string"}
        },

        "phones": {
            "type": "array",
            "items": {"type": "string"}
        },

        "location": {
            "type": "object",
            "properties": {

                "city": {
                    "type": ["string", "null"]
                },

                "region": {
                    "type": ["string", "null"]
                },

                "country": {
                    "type": ["string", "null"]
                }
            }
        },

        "links": {
            "type": "object",
            "properties": {

                "linkedin": {
                    "type": ["string", "null"]
                },

                "github": {
                    "type": ["string", "null"]
                },

                "portfolio": {
                    "type": ["string", "null"]
                },

                "other": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },

        "headline": {
            "type": ["string", "null"]
        },

        "years_experience": {
            "type": ["number", "null"]
        },

        "skills": {
            "type": "array",
            "items": {"type": "string"}
        },

        "experience": {
            "type": "array",
            "items": {"type": "object"}
        },

        "education": {
            "type": "array",
            "items": {"type": "object"}
        },

        "provenance": {
            "type": "object"
        },

        "overall_confidence": {
            "type": "number"
        }
    }
}


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def empty_candidate() -> Dict[str, Any]:
    """
    Returns a fresh empty candidate dictionary.

    deepcopy() ensures mutable fields such as lists and
    dictionaries are not shared across candidate instances.
    """
    return deepcopy(CANONICAL_SCHEMA)


def required_fields():
    """
    Returns all mandatory canonical fields.
    """
    return list(JSON_SCHEMA["required"])


def has_field(field_name: str) -> bool:
    """
    Checks whether a field exists in the canonical schema.
    """
    return field_name in CANONICAL_SCHEMA


def default_value(field_name: str):
    """
    Returns the default value for a canonical field.
    """
    if field_name not in CANONICAL_SCHEMA:
        raise KeyError(f"Unknown canonical field: {field_name}")

    return deepcopy(CANONICAL_SCHEMA[field_name])