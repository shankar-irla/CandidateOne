"""
Unit Tests

Projection Layer Tests

Verifies that canonical candidate profiles
are correctly projected into configurable
output schemas.
"""

from projection.output_mapper import OutputMapper


# ---------------------------------------------------------
# Sample Candidate
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

    "skills": [
        "Python",
        "Flask"
    ],

    "headline": "AI Engineer",

    "location": {

        "city": "Hyderabad",

        "country": "India"

    },

    "links": {

        "linkedin": "linkedin.com/in/shankar",

        "github": "github.com/shankar"

    },

    "experience": [],

    "education": [],

    "provenance": {},

    "overall_confidence": 0.92
}


# ---------------------------------------------------------
# Default Projection
# ---------------------------------------------------------

def test_default_projection():

    mapper = OutputMapper()

    projected = mapper.project(candidate)

    assert isinstance(projected, dict)

    assert projected["full_name"] == "Shankar Irla"


# ---------------------------------------------------------
# Candidate ID
# ---------------------------------------------------------

def test_candidate_id():

    mapper = OutputMapper()

    projected = mapper.project(candidate)

    assert projected["candidate_id"] == "1001"


# ---------------------------------------------------------
# Skills
# ---------------------------------------------------------

def test_skill_projection():

    mapper = OutputMapper()

    projected = mapper.project(candidate)

    assert "Python" in projected["skills"]


# ---------------------------------------------------------
# Confidence
# ---------------------------------------------------------

def test_confidence_projection():

    mapper = OutputMapper()

    projected = mapper.project(candidate)

    assert projected["overall_confidence"] == 0.92