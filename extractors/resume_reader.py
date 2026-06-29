"""
Resume Reader

Reads PDF resumes and converts them into the CandidateOne
canonical schema.

This module extracts raw resume text and performs the first
stage of information extraction.

Stage 1
-------
 PDF Reading
 Text Cleaning
 Name Extraction
 Email Extraction
 Phone Extraction
 URL Extraction
 Section Detection


"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from PyPDF2 import PdfReader

from extractors.base_reader import BaseReader
from extractors.parser import Parser
from models.canonical_schema import empty_candidate
from utils.logger import get_logger


class ResumeReader(BaseReader):
    """
    Reads PDF resumes.
    """

    SOURCE_NAME = "resume"

    def __init__(self, file_path: str):

        super().__init__(file_path)

        self.logger = get_logger(__name__)

    # -----------------------------------------------------
    # Read PDF
    # -----------------------------------------------------

    def read(self) -> str:
        """
        Extracts text from every page of the PDF.
        """

        reader = PdfReader(self.file_path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    # -----------------------------------------------------
    # Parse
    # -----------------------------------------------------
    # -----------------------------------------------------

    def parse(
        self,
        raw_text: str
    ) -> Dict:
        """
        Parses the extracted resume text into the
        CandidateOne canonical schema.

        Pipeline:
            PDF Text
                ↓
            Clean Text
                ↓
            Basic Extraction
                ↓
            Section Detection
                ↓
            Structured Extraction
                ↓
            Provenance
                ↓
            Confidence
                ↓
            Metadata
                ↓
            Canonical Candidate
        """

        # Create empty canonical candidate
        candidate = empty_candidate()

        # Clean extracted text
        cleaned = self.clean_text(raw_text)

        # -------------------------------------------------
        # Basic Information
        # -------------------------------------------------

        candidate["full_name"] = self.extract_name(cleaned)

        candidate["emails"] = self.extract_emails(cleaned)

        candidate["phones"] = self.extract_phones(cleaned)

        # -------------------------------------------------
        # Links
        # -------------------------------------------------

        urls = self.extract_urls(cleaned)

        self.populate_links(candidate, urls)

        # -------------------------------------------------
        # Split Resume into Sections
        # -------------------------------------------------

        self.sections = self.extract_sections(cleaned)

        # -------------------------------------------------
        # Populate Candidate
        # -------------------------------------------------

        candidate = self.populate_candidate(candidate)

        # -------------------------------------------------
        # Final Processing
        # -------------------------------------------------

        candidate = self.finalize_candidate(candidate)

        # -------------------------------------------------
        # Logging
        # -------------------------------------------------

        self.logger.info(
            "Resume parsed successfully for candidate: %s",
            candidate.get("full_name", "Unknown")
        )

        return candidate

    # -----------------------------------------------------
    # Text Cleaning
    # -----------------------------------------------------

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans resume text.
        """

        text = text.replace("\r", "\n")

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n+",
            "\n",
            text
        )

        return text.strip()

    # -----------------------------------------------------
    # Name
    # -----------------------------------------------------

    @staticmethod
    def extract_name(text: str):

        """
        Uses first meaningful line as candidate name.
        """

        for line in text.splitlines():

            line = line.strip()

            if len(line) < 3:
                continue

            if "@" in line:
                continue

            if "http" in line.lower():
                continue

            return Parser.text(line)

        return None

    # -----------------------------------------------------
    # Email
    # -----------------------------------------------------

    @staticmethod
    def extract_emails(
        text: str
    ) -> List[str]:

        return Parser.emails(text)

    # -----------------------------------------------------
    # Phone
    # -----------------------------------------------------

    @staticmethod
    def extract_phones(
        text: str
    ) -> List[str]:

        return Parser.phones(text)

    # -----------------------------------------------------
    # URLs
    # -----------------------------------------------------

    @staticmethod
    def extract_urls(
        text: str
    ) -> List[str]:

        return Parser.urls(text)

    # -----------------------------------------------------
    # Populate Links
    # -----------------------------------------------------

    @staticmethod
    def populate_links(
        candidate: Dict,
        urls: List[str]
    ):

        """
        Detects GitHub, LinkedIn and Portfolio URLs.
        """

        for url in urls:

            lower = url.lower()

            if "linkedin" in lower:

                candidate["links"]["linkedin"] = url

            elif "github" in lower:

                candidate["links"]["github"] = url

            else:

                candidate["links"]["other"].append(url)

    # -----------------------------------------------------
    # Section Extraction
    # -----------------------------------------------------

    @staticmethod
    def extract_sections(
        text: str
    ) -> Dict[str, str]:

        """
        Splits resume into logical sections.

        Returned dictionary is used in Part 2.
        """

        headings = [

            "education",

            "experience",

            "skills",

            "projects",

            "certifications",

            "summary",

            "profile"

        ]

        lines = text.splitlines()

        sections = {}

        current = "general"

        sections[current] = []

        for line in lines:

            cleaned = line.strip()

            if not cleaned:
                continue

            lower = cleaned.lower()

            matched = False

            for heading in headings:

                if lower.startswith(heading):

                    current = heading

                    sections.setdefault(
                        current,
                        []
                    )

                    matched = True

                    break

            if matched:
                continue

            sections[current].append(cleaned)

        return {

            key: "\n".join(value)

            for key, value in sections.items()

        }
        # -----------------------------------------------------
    # Skills Extraction
    # -----------------------------------------------------

    def extract_skills(self) -> List[str]:
        """
        Extracts candidate skills from the Skills section.

        Falls back to the entire resume if the section
        is unavailable.
        """

        text = self.sections.get("skills", "")

        if not text:
            text = self.sections.get("general", "")

        return Parser.split_skills(text)

    # -----------------------------------------------------
    # Education Extraction
    # -----------------------------------------------------

    def extract_education(self) -> List[Dict]:
        """
        Extracts education entries from the Education section.

        Since resume formats vary significantly, each
        non-empty line is initially treated as one record.
        """

        text = self.sections.get("education", "")

        if not text:
            return []

        records = []

        for line in text.splitlines():

            line = Parser.text(line)

            if not line:
                continue

            records.append(
                {
                    "institution": line,
                    "degree": None,
                    "start_date": None,
                    "end_date": None
                }
            )

        return records

    # -----------------------------------------------------
    # Experience Extraction
    # -----------------------------------------------------

    def extract_experience(self) -> List[Dict]:
        """
        Extracts experience entries.

        Each non-empty line becomes an initial experience
        record. The merge stage can enrich this later.
        """

        text = self.sections.get("experience", "")

        if not text:
            return []

        records = []

        for line in text.splitlines():

            line = Parser.text(line)

            if not line:
                continue

            records.append(
                {
                    "company": None,
                    "role": line,
                    "start_date": None,
                    "end_date": None
                }
            )

        return records

    # -----------------------------------------------------
    # Headline Generation
    # -----------------------------------------------------

    def extract_headline(self) -> str | None:
        """
        Attempts to generate a professional headline.

        Preference:
        1. Summary section
        2. Profile section
        3. First experience title
        """

        summary = self.sections.get("summary")

        if summary:
            return Parser.text(summary.splitlines()[0])

        profile = self.sections.get("profile")

        if profile:
            return Parser.text(profile.splitlines()[0])

        experience = self.extract_experience()

        if experience:

            return experience[0]["role"]

        return None

    # -----------------------------------------------------
    # Years of Experience
    # -----------------------------------------------------

    def calculate_years_experience(self) -> float | None:
        """
        Very lightweight estimate.

        Currently based on number of experience entries.

        This method can later be upgraded to calculate
        duration from start/end dates.
        """

        experience = self.extract_experience()

        if not experience:
            return None

        return float(len(experience))

    # -----------------------------------------------------
    # Populate Candidate
    # -----------------------------------------------------

    def populate_candidate(
        self,
        candidate: Dict
    ) -> Dict:
        """
        Populates canonical fields extracted from the
        resume sections.
        """

        candidate["headline"] = self.extract_headline()

        candidate["skills"] = self.extract_skills()

        candidate["education"] = self.extract_education()

        candidate["experience"] = self.extract_experience()

        candidate["years_experience"] = (
            self.calculate_years_experience()
        )

        return candidate

    # -----------------------------------------------------
    # Provenance Generation
    # -----------------------------------------------------

    def generate_provenance(
        self,
        candidate: Dict
    ) -> None:
        """
        Generates field-level provenance information.
        """

        provenance = {}

        for field, value in candidate.items():

            if field == "provenance":
                continue

            if value is None:
                continue

            if isinstance(value, str) and not value.strip():
                continue

            if isinstance(value, (list, dict)) and len(value) == 0:
                continue

            provenance[field] = [
                {
                    "source": self.SOURCE_NAME,
                    "method": "resume_pdf"
                }
            ]

        candidate["provenance"] = provenance

    # -----------------------------------------------------
    # Confidence Calculation
    # -----------------------------------------------------

    def calculate_confidence(
        self,
        candidate: Dict
    ) -> float:
        """
        Computes a lightweight confidence score for the
        extracted resume data.

        Resume is considered the highest priority source,
        therefore starts with a strong base score.
        """

        score = 0.50

        weights = {

            "full_name": 0.08,

            "emails": 0.08,

            "phones": 0.08,

            "headline": 0.05,

            "skills": 0.08,

            "experience": 0.06,

            "education": 0.04,

            "links": 0.03
        }

        for field, weight in weights.items():

            value = candidate.get(field)

            if value is None:
                continue

            if isinstance(value, str):

                if value.strip():
                    score += weight

            elif isinstance(value, list):

                if value:
                    score += weight

            elif isinstance(value, dict):

                if any(value.values()):
                    score += weight

        return round(min(score, 1.0), 3)

    # -----------------------------------------------------
    # Resume Metadata
    # -----------------------------------------------------

    def add_metadata(
        self,
        candidate: Dict
    ) -> None:
        """
        Stores resume metadata useful during debugging
        and downstream processing.
        """

        candidate.setdefault("metadata", {})

        candidate["metadata"].update({

            "source_file": self.file_path.name,

            "source_type": "resume_pdf",

            "reader": self.__class__.__name__
        })

    # -----------------------------------------------------
    # Finalization
    # -----------------------------------------------------

    def finalize_candidate(
        self,
        candidate: Dict
    ) -> Dict:
        """
        Applies final processing before returning the
        canonical candidate.
        """

        self.generate_provenance(candidate)

        candidate["overall_confidence"] = (
            self.calculate_confidence(candidate)
        )

        self.add_metadata(candidate)

        return candidate