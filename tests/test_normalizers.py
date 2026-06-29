"""
Unit Tests

Normalizer Tests

Verifies all normalization modules produce
clean, standardized candidate data.
"""

from normalizer.email import EmailNormalizer
from normalizer.phone import PhoneNormalizer
from normalizer.skills import SkillNormalizer
from normalizer.location import LocationNormalizer
from normalizer.dates import DateNormalizer


# ---------------------------------------------------------
# Email
# ---------------------------------------------------------

def test_email_normalization():

    emails = [
        " TEST@GMAIL.COM ",
        "test@gmail.com",
        "invalid-email"
    ]

    result = EmailNormalizer.normalize(emails)

    assert isinstance(result, list)

    assert "test@gmail.com" in result

    assert "invalid-email" not in result


# ---------------------------------------------------------
# Phone
# ---------------------------------------------------------

def test_phone_normalization():

    phones = [
        "9010376352",
        "+91 90103 76352"
    ]

    result = PhoneNormalizer.normalize(
        phones,
        default_country="IN"
    )

    assert isinstance(result, list)

    assert len(result) >= 1


# ---------------------------------------------------------
# Skills
# ---------------------------------------------------------

def test_skill_normalization():

    skills = [

        "python",

        "Python",

        "PYTHON",

        "Machine Learning",

        "machine learning"

    ]

    normalized = SkillNormalizer.normalize(skills)

    assert "Python" in normalized

    assert normalized.count("Python") == 1


# ---------------------------------------------------------
# Location
# ---------------------------------------------------------

def test_location_normalization():

    location = {

        "city": "hyderabad",

        "region": "telangana",

        "country": "india"

    }

    normalized = LocationNormalizer.normalize(location)

    assert normalized["city"] == "Hyderabad"

    assert normalized["country"] == "India"


# ---------------------------------------------------------
# Dates
# ---------------------------------------------------------

def test_date_normalization():

    assert DateNormalizer.normalize("2023-05") == "2023-05"

    assert DateNormalizer.normalize("May 2023") == "2023-05"

    assert DateNormalizer.normalize("") is None