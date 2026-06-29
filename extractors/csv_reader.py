"""
CSV Reader

Reads recruiter CSV files and converts each row into the
CandidateOne canonical schema.

"""

from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from extractors.base_reader import BaseReader
from extractors.parser import Parser
from models.canonical_schema import empty_candidate
from utils.logger import get_logger


class CSVReader(BaseReader):
    """
    Reads recruiter CSV files.

    Each row represents one candidate profile.
    """

    SOURCE_NAME = "recruiter_csv"

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.logger = get_logger(__name__)

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def read(self) -> pd.DataFrame:
        """
        Reads recruiter CSV.
        """
        return pd.read_csv(self.file_path).fillna("")

    # ---------------------------------------------------------
    # Parse
    # ---------------------------------------------------------

    def parse(
        self,
        dataframe: pd.DataFrame
    ) -> List[Dict[str, Any]]:
        """
        Converts DataFrame rows into canonical candidates.
        """

        candidates = []

        for _, row in dataframe.iterrows():

            record = row.to_dict()

            candidate = empty_candidate()

            # ----------------------------------------------
            # Basic Information
            # ----------------------------------------------

            candidate["candidate_id"] = Parser.text(
                Parser.get(record, "candidate_id")
            )

            candidate["full_name"] = Parser.text(
                Parser.get(record, "full_name")
            )

            # ----------------------------------------------
            # Contact
            # ----------------------------------------------

            email = Parser.text(
                Parser.get(record, "email")
            )

            if email:
                candidate["emails"] = [email]

            phone = Parser.text(
                Parser.get(record, "phone")
            )

            if phone:
                candidate["phones"] = [phone]

            # ----------------------------------------------
            # Headline
            # ----------------------------------------------

            candidate["headline"] = Parser.text(
                Parser.get(record, "headline")
            )

            # ----------------------------------------------
            # Experience
            # ----------------------------------------------

            candidate["years_experience"] = Parser.years(
                Parser.get(record, "years_experience")
            )

            # ----------------------------------------------
            # Skills
            # ----------------------------------------------

            candidate["skills"] = Parser.split_skills(
                Parser.get(record, "skills")
            )

            # ----------------------------------------------
            # Location
            # ----------------------------------------------

            candidate["location"]["city"] = Parser.text(
                Parser.get(record, "city")
            )

            candidate["location"]["region"] = Parser.text(
                Parser.get(record, "region")
            )

            candidate["location"]["country"] = Parser.text(
                Parser.get(record, "country")
            )

            # ----------------------------------------------
            # Links
            # ----------------------------------------------

            candidate["links"]["linkedin"] = Parser.text(
                Parser.get(record, "linkedin")
            )

            candidate["links"]["github"] = Parser.text(
                Parser.get(record, "github")
            )

            candidate["links"]["portfolio"] = Parser.text(
                Parser.get(record, "portfolio")
            )

            # ----------------------------------------------
            # Optional Experience & Education
            # ----------------------------------------------

            candidate["experience"] = Parser.list(
                Parser.get(record, "experience")
            )

            candidate["education"] = Parser.list(
                Parser.get(record, "education")
            )

            # ----------------------------------------------
            # Provenance
            # ----------------------------------------------

            candidate["provenance"] = {
                "candidate_id": [self.SOURCE_NAME],
                "full_name": [self.SOURCE_NAME],
                "emails": [self.SOURCE_NAME],
                "phones": [self.SOURCE_NAME],
                "headline": [self.SOURCE_NAME],
                "years_experience": [self.SOURCE_NAME],
                "skills": [self.SOURCE_NAME],
                "location": [self.SOURCE_NAME],
                "links": [self.SOURCE_NAME],
                "experience": [self.SOURCE_NAME],
                "education": [self.SOURCE_NAME]
            }

            # ----------------------------------------------
            # Initial Confidence
            # ----------------------------------------------

            candidate["overall_confidence"] = 0.80

            candidates.append(candidate)

        self.logger.info(
            "Successfully parsed %d candidate(s) from %s",
            len(candidates),
            self.file_path.name
        )

        return candidates