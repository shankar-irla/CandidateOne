"""
Unit Tests

Schema Validator Tests

Ensures canonical candidate profiles satisfy
the required JSON schema.
"""

from validator.schema_validator import SchemaValidator


# ---------------------------------------------------------
# Valid Candidate
# ---------------------------------------------------------

candidate = {

    "candidate_id": "1001",

    "full_name": "Shankar Irla",

    "emails": [
        "shankar@gmail.com"
    ],

    "phones": [
        "+919010376352"
    ],

    "location": {

        "city": "Hyderabad",

        "region": "Telangana",

        "country": "India"

    },

    "links": {

        "linkedin": None,

        "github": None,

        "portfolio": None,

        "other": []

    },

    "headline": "AI Engineer",

    "years_experience": 2,

    "skills": [

        "Python",

        "Flask"

    ],

    "experience": [],

    "education": [],

    "provenance": {},

    "overall_confidence": 0.90
}


# ---------------------------------------------------------
# Valid Schema
# ---------------------------------------------------------

def test_schema_validation():

    validator = SchemaValidator()

    assert validator.validate(candidate) is True


# ---------------------------------------------------------
# Missing Required Field
# ---------------------------------------------------------

def test_missing_field():

    validator = SchemaValidator()

    invalid = candidate.copy()

    invalid.pop("full_name")

    assert validator.validate(invalid) is False


# ---------------------------------------------------------
# Wrong Type
# ---------------------------------------------------------

def test_wrong_type():

    validator = SchemaValidator()

    invalid = candidate.copy()

    invalid["skills"] = "Python"

    assert validator.validate(invalid) is False