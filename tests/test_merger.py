"""
Unit Tests

Merge Engine Tests

Verifies that multiple candidate profiles
are correctly merged into one canonical profile.
"""

from merger.merge_engine import MergeEngine


# ---------------------------------------------------------
# Test Data
# ---------------------------------------------------------

candidate_resume = {

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

    "experience": [],

    "education": [],

    "links": {},

    "provenance": {
        "full_name": ["resume"]
    },

    "overall_confidence": 0.0
}


candidate_linkedin = {

    "candidate_id": "1001",

    "full_name": "Irla Ganga Siva Shankar",

    "emails": [
        "shankar@gmail.com"
    ],

    "phones": [],

    "skills": [
        "Python",
        "Machine Learning"
    ],

    "headline": "Machine Learning Engineer",

    "location": {
        "city": "Hyderabad",
        "country": "India"
    },

    "experience": [],

    "education": [],

    "links": {},

    "provenance": {
        "full_name": ["linkedin"]
    },

    "overall_confidence": 0.0
}


# ---------------------------------------------------------
# Merge
# ---------------------------------------------------------

def test_merge_candidates():

    engine = MergeEngine()

    merged = engine.merge([

        candidate_resume,

        candidate_linkedin

    ])

    assert isinstance(merged, dict)

    assert merged["candidate_id"] == "1001"

    assert len(merged["skills"]) >= 2

    assert merged["overall_confidence"] > 0


# ---------------------------------------------------------
# Email Preservation
# ---------------------------------------------------------

def test_email_preserved():

    engine = MergeEngine()

    merged = engine.merge([

        candidate_resume,

        candidate_linkedin

    ])

    assert "shankar@gmail.com" in merged["emails"]


# ---------------------------------------------------------
# Skill Merge
# ---------------------------------------------------------

def test_duplicate_skill_removed():

    engine = MergeEngine()

    merged = engine.merge([

        candidate_resume,

        candidate_linkedin

    ])

    assert merged["skills"].count("Python") == 1


# ---------------------------------------------------------
# Confidence
# ---------------------------------------------------------

def test_confidence_exists():

    engine = MergeEngine()

    merged = engine.merge([

        candidate_resume,

        candidate_linkedin

    ])

    assert merged["overall_confidence"] >= 0.0


# ---------------------------------------------------------
# Provenance
# ---------------------------------------------------------

def test_provenance_exists():

    engine = MergeEngine()

    merged = engine.merge([

        candidate_resume,

        candidate_linkedin

    ])

    assert "provenance" in merged

    assert isinstance(

        merged["provenance"],

        dict

    )