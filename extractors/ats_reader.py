"""
ATS Reader

Reads Applicant Tracking System (ATS) JSON files and converts
them into the CandidateOne canonical candidate schema.

"""

from __future__ import annotations

from typing import Any, Dict
import json

from extractors.base_reader import BaseReader
from extractors.parser import Parser
from models.canonical_schema import empty_candidate
from utils.logger import get_logger


class ATSReader(BaseReader):
    """
    Reads ATS JSON exports.

    Expected Input:
    {
        "candidate_id": "...",
        "full_name": "...",
        "email": "...",
        ...
    }
    """

    def __init__(self, file_path: str):

        super().__init__(file_path)

        self.logger = get_logger(__name__)

    # ---------------------------------------------------------
    # Read JSON
    # ---------------------------------------------------------

    def read(self) -> Dict[str, Any]:
        """
        Reads the ATS JSON file.
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
        """
        Converts ATS JSON into canonical schema.
        """

        candidate = empty_candidate()

        # -----------------------------------------------------
        # Basic Information
        # -----------------------------------------------------

        candidate["candidate_id"] = Parser.text(
            Parser.get(data, "candidate_id")
        )

        candidate["full_name"] = Parser.text(
            Parser.get(data, "full_name")
        )

        # -----------------------------------------------------
        # Contact
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Headline
        # -----------------------------------------------------

        candidate["headline"] = Parser.text(
            Parser.get(data, "headline")
        )

        # -----------------------------------------------------
        # Experience
        # -----------------------------------------------------

        candidate["years_experience"] = Parser.years(
            Parser.get(data, "years_experience")
        )

        # -----------------------------------------------------
        # Skills
        # -----------------------------------------------------

        candidate["skills"] = Parser.split_skills(
            Parser.get(data, "skills")
        )

        # -----------------------------------------------------
        # Location
        # -----------------------------------------------------

        candidate["location"]["city"] = Parser.text(
            Parser.get(data, "city")
        )

        candidate["location"]["region"] = Parser.text(
            Parser.get(data, "region")
        )

        candidate["location"]["country"] = Parser.text(
            Parser.get(data, "country")
        )

        # -----------------------------------------------------
        # Links
        # -----------------------------------------------------

        candidate["links"]["linkedin"] = Parser.text(
            Parser.get(data, "linkedin")
        )

        candidate["links"]["github"] = Parser.text(
            Parser.get(data, "github")
        )

        candidate["links"]["portfolio"] = Parser.text(
            Parser.get(data, "portfolio")
        )

        # -----------------------------------------------------
        # Experience Records
        # -----------------------------------------------------

        candidate["experience"] = Parser.list(
            Parser.get(data, "experience")
        )

        # -----------------------------------------------------
        # Education Records
        # -----------------------------------------------------

        candidate["education"] = Parser.list(
            Parser.get(data, "education")
        )

        # -----------------------------------------------------
        # Provenance
        # -----------------------------------------------------

        candidate["provenance"] = {
            "candidate_id": ["ats"],
            "full_name": ["ats"],
            "emails": ["ats"],
            "phones": ["ats"],
            "headline": ["ats"],
            "years_experience": ["ats"],
            "skills": ["ats"],
            "location": ["ats"],
            "links": ["ats"],
            "experience": ["ats"],
            "education": ["ats"]
        }

        # -----------------------------------------------------
        # Initial Confidence
        # -----------------------------------------------------

        candidate["overall_confidence"] = 0.90

        self.logger.info(
            "Successfully parsed ATS candidate '%s'",
            candidate["full_name"]
        )

        return candidate