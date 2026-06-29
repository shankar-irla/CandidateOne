"""
GitHub Reader

Reads GitHub profile JSON and converts it into the
CandidateOne canonical schema.

"""

from __future__ import annotations

import json
from typing import Any, Dict

from extractors.base_reader import BaseReader
from extractors.parser import Parser
from models.canonical_schema import empty_candidate
from utils.logger import get_logger


class GitHubReader(BaseReader):
    """
    Reads GitHub profile JSON.
    """

    SOURCE_NAME = "github"

    def __init__(self, file_path: str):

        super().__init__(file_path)

        self.logger = get_logger(__name__)

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def read(self) -> Dict[str, Any]:
        """
        Reads GitHub JSON.
        """

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # ---------------------------------------------------------
    # Parse
    # ---------------------------------------------------------

    def parse(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        candidate = empty_candidate()

        # -----------------------------------------------------
        # Name
        # -----------------------------------------------------

        candidate["full_name"] = (
            Parser.text(
                Parser.get(data, "name")
            )
            or
            Parser.text(
                Parser.get(data, "full_name")
            )
        )

        # -----------------------------------------------------
        # Email
        # -----------------------------------------------------

        email = Parser.text(
            Parser.get(data, "email")
        )

        if email:
            candidate["emails"] = [email]

        # -----------------------------------------------------
        # GitHub Profile
        # -----------------------------------------------------

        github_url = (
            Parser.text(
                Parser.get(data, "html_url")
            )
            or
            Parser.text(
                Parser.get(data, "profile_url")
            )
        )

        candidate["links"]["github"] = github_url

        # -----------------------------------------------------
        # Headline
        # -----------------------------------------------------

        candidate["headline"] = (
            Parser.text(
                Parser.get(data, "bio")
            )
        )

        # -----------------------------------------------------
        # Location
        # -----------------------------------------------------

        location = Parser.text(
            Parser.get(data, "location")
        )

        if location:
            candidate["location"]["city"] = location

        # -----------------------------------------------------
        # Skills
        # -----------------------------------------------------

        skills = Parser.get(data, "skills")

        if not skills:

            repos = Parser.list(
                Parser.get(data, "repositories")
            )

            detected_skills = []

            for repo in repos:

                if not isinstance(repo, dict):
                    continue

                language = Parser.text(
                    repo.get("language")
                )

                if language:
                    detected_skills.append(language)

                topics = Parser.list(
                    repo.get("topics")
                )

                detected_skills.extend(topics)

            candidate["skills"] = Parser.split_skills(
                detected_skills
            )

        else:

            candidate["skills"] = Parser.split_skills(
                skills
            )

        # -----------------------------------------------------
        # Experience
        # -----------------------------------------------------

        candidate["years_experience"] = Parser.years(
            Parser.get(data, "years_experience")
        )

        # -----------------------------------------------------
        # Provenance
        # -----------------------------------------------------

        candidate["provenance"] = {

            "full_name": [self.SOURCE_NAME],

            "emails": [self.SOURCE_NAME],

            "headline": [self.SOURCE_NAME],

            "skills": [self.SOURCE_NAME],

            "links": [self.SOURCE_NAME],

            "location": [self.SOURCE_NAME]
        }

        # -----------------------------------------------------
        # Confidence
        # -----------------------------------------------------

        candidate["overall_confidence"] = 0.85

        self.logger.info(
            "GitHub profile parsed successfully."
        )

        return candidate