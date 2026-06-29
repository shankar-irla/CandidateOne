"""
Unit Tests

Extractor Tests

Verifies all supported extractors can successfully
read and parse candidate sources.
"""

import os

from extractors.resume_reader import ResumeReader
from extractors.ats_reader import ATSReader
from extractors.linkedin_reader import LinkedInReader
from extractors.github_reader import GitHubReader
from extractors.csv_reader import CSVReader


DATA = "tests/sample_data"


def test_resume_reader():

    reader = ResumeReader(
        os.path.join(DATA, "resume.pdf")
    )

    candidate = reader.extract()

    assert isinstance(candidate, dict)

    assert "full_name" in candidate

    assert "emails" in candidate

    assert "skills" in candidate


def test_ats_reader():

    reader = ATSReader(
        os.path.join(DATA, "ats.json")
    )

    candidate = reader.extract()

    assert isinstance(candidate, dict)

    assert candidate["full_name"] is not None


def test_linkedin_reader():

    reader = LinkedInReader(
        os.path.join(DATA, "linkedin.json")
    )

    candidate = reader.extract()

    assert isinstance(candidate, dict)

    assert "skills" in candidate


def test_github_reader():

    reader = GitHubReader(
        os.path.join(DATA, "github.json")
    )

    candidate = reader.extract()

    assert isinstance(candidate, dict)

    assert "links" in candidate


def test_csv_reader():

    reader = CSVReader(
        os.path.join(DATA, "recruiter.csv")
    )

    candidates = reader.extract()

    assert isinstance(candidates, list)

    assert len(candidates) > 0

    assert isinstance(candidates[0], dict)