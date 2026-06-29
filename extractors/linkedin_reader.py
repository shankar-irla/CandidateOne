"""
LinkedIn Reader

Reads LinkedIn profile JSON and converts it into the
CandidateOne canonical candidate schema.

"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from extractors.base_reader import BaseReader
from extractors.parser import Parser
from models.canonical_schema import empty_candidate
from utils.logger import get_logger


class LinkedInReader(BaseReader):
    """
    Reads LinkedIn profile JSON and converts it into the
    CandidateOne canonical format.
    """

    SOURCE_NAME = "linkedin"

    def __init__(self, file_path: str):

        super().__init__(file_path)

        self.logger = get_logger(__name__)

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    def read(self) -> Dict[str, Any]:
        """
        Reads LinkedIn JSON file.
        """

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # -----------------------------------------------------
    # Parse
    # -----------------------------------------------------

    def parse(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        candidate = empty_candidate()

        # -------------------------------------------------
        # Basic Information
        # -------------------------------------------------

        candidate["full_name"] = Parser.text(
            Parser.get(data, "full_name")
        )

        if not candidate["full_name"]:
            candidate["full_name"] = Parser.text(
                Parser.get(data, "name")
            )

        # -------------------------------------------------
        # Contact
        # -------------------------------------------------

        email = Parser.text(
            Parser.get(data, "email")
        )

        if email:
            candidate["emails"] = [email]

        phone = Parser.text(
            Parser.get(data, "phone")
        )

        if phone:
            candidate["phones"] = [phone]

        # -------------------------------------------------
        # Headline
        # -------------------------------------------------

        candidate["headline"] = Parser.text(
            Parser.get(data, "headline")
        )

        # -------------------------------------------------
        # Location
        # -------------------------------------------------

        candidate["location"]["city"] = Parser.text(
            Parser.get(data, "city")
        )

        candidate["location"]["region"] = Parser.text(
            Parser.get(data, "region")
        )

        candidate["location"]["country"] = Parser.text(
            Parser.get(data, "country")
        )

        # -------------------------------------------------
        # Profile Links
        # -------------------------------------------------

        candidate["links"]["linkedin"] = Parser.text(
            Parser.get(data, "profile_url")
        )

        candidate["links"]["github"] = Parser.text(
            Parser.get(data, "github")
        )

        candidate["links"]["portfolio"] = Parser.text(
            Parser.get(data, "portfolio")
        )

        # -------------------------------------------------
        # Skills
        # -------------------------------------------------

        candidate["skills"] = Parser.split_skills(
            Parser.get(data, "skills")
        )

        # -------------------------------------------------
        # Experience
        # -------------------------------------------------

        experience = Parser.list(
            Parser.get(data, "experience")
        )

        candidate["experience"] = experience

        # Years of Experience
        years = Parser.years(
            Parser.get(data, "years_experience")
        )

        if years is None:
            years = len(experience)

        candidate["years_experience"] = years

        # -------------------------------------------------
        # Education
        # -------------------------------------------------

        candidate["education"] = Parser.list(
            Parser.get(data, "education")
        )

        # -------------------------------------------------
        # Certifications
        # -------------------------------------------------

        certifications = Parser.list(
            Parser.get(data, "certifications")
        )

        if certifications:

            candidate.setdefault(
                "metadata",
                {}
            )

            candidate["metadata"][
                "certifications"
            ] = certifications

        # -------------------------------------------------
        # Provenance
        # -------------------------------------------------

        candidate["provenance"] = {

            "full_name": [self.SOURCE_NAME],

            "emails": [self.SOURCE_NAME],

            "phones": [self.SOURCE_NAME],

            "headline": [self.SOURCE_NAME],

            "skills": [self.SOURCE_NAME],

            "experience": [self.SOURCE_NAME],

            "education": [self.SOURCE_NAME],

            "location": [self.SOURCE_NAME],

            "links": [self.SOURCE_NAME]
        }

        # -------------------------------------------------
        # Initial Confidence
        # -------------------------------------------------

        candidate["overall_confidence"] = 0.95

        self.logger.info(
            "LinkedIn profile parsed successfully."
        )

        return candidate