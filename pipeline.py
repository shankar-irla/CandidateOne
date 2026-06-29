"""
CandidateOne ETL Pipeline

End-to-End Candidate Canonicalization Pipeline.

Author:
    Shankar Irla
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

# =========================================================
# Extractors
# =========================================================

from extractors.resume_reader import ResumeReader
from extractors.ats_reader import ATSReader
from extractors.csv_reader import CSVReader
from extractors.github_reader import GitHubReader
from extractors.linkedin_reader import LinkedInReader

# =========================================================
# Normalizers
# =========================================================

from normalizer.text import TextNormalizer
from normalizer.email import EmailNormalizer
from normalizer.phone import PhoneNormalizer
from normalizer.dates import DateNormalizer
from normalizer.skills import SkillNormalizer
from normalizer.location import LocationNormalizer

# =========================================================
# Merge
# =========================================================

from merger.merge_engine import MergeEngine

# =========================================================
# Projection
# =========================================================

from projection.config_loader import ConfigLoader
from projection.output_mapper import OutputMapper

# =========================================================
# Validators
# =========================================================

from validator.config_validator import ConfigValidator
from validator.schema_validator import SchemaValidator

# =========================================================
# Models
# =========================================================

from models.canonical_schema import empty_candidate

# =========================================================
# Utilities
# =========================================================

from utils.logger import get_logger


class CandidatePipeline:
    """
    Complete CandidateOne ETL Pipeline.
    """

    def __init__(
        self,
        input_directory: str = "sample_input",
        output_directory: str = "output",
        config_file: str = "config/default_config.json"
    ):

        self.logger = get_logger(__name__)

        self.input_directory = Path(input_directory)

        self.output_directory = Path(output_directory)

        self.output_directory.mkdir(
            exist_ok=True
        )

        # ---------------------------------------------
        # Configuration
        # ---------------------------------------------

        self.config_loader = ConfigLoader(
            config_file
        )

        self.config = self.config_loader.load()

        ConfigValidator.validate_all(
            self.config
        )

        # ---------------------------------------------
        # Projection
        # ---------------------------------------------

        self.output_mapper = OutputMapper(
            self.config_loader
        )

        # ---------------------------------------------
        # Merge Engine
        # ---------------------------------------------

        self.merge_engine = MergeEngine()

        # ---------------------------------------------
        # Validators
        # ---------------------------------------------

        self.schema_validator = SchemaValidator()

        # ---------------------------------------------
        # Readers
        # ---------------------------------------------

        self.readers = [

            ResumeReader(
                self.input_directory / "resume.pdf"
            ),

            ATSReader(
                self.input_directory / "ats.json"
            ),

            LinkedInReader(
                self.input_directory / "linkedin.json"
            ),

            GitHubReader(
                self.input_directory / "github.json"
            ),

            CSVReader(
                self.input_directory / "recruiter.csv"
            )

        ]

        # ---------------------------------------------
        # Normalizers
        # ---------------------------------------------

        self.normalizers = [

            TextNormalizer,

            EmailNormalizer,

            PhoneNormalizer,

            DateNormalizer,

            SkillNormalizer,

            LocationNormalizer

        ]

        self.logger.info(
            "Candidate Pipeline initialized."
        )

    # =====================================================
    # Read One Source
    # =====================================================

    def read_source(
        self,
        reader
    ):
        """
        Reads a single source.

        Supports:

        extract()

        read()+parse()

        read()
        """

        try:

            if hasattr(reader, "extract"):

                return reader.extract()

            if hasattr(reader, "read") and hasattr(reader, "parse"):

                raw = reader.read()

                return reader.parse(raw)

            if hasattr(reader, "read"):

                return reader.read()

            raise RuntimeError(
                f"Unsupported reader: {reader.__class__.__name__}"
            )

        except Exception:

            self.logger.exception(
                "Failed reading %s",
                reader.__class__.__name__
            )

            return None

    # =====================================================
    # Extraction
    # =====================================================

    def extract_candidates(
        self
    ) -> List[Dict]:
        """
        Executes all extractors.
        """

        self.logger.info(
            "Extraction started."
        )

        candidates = []

        for reader in self.readers:

            result = self.read_source(
                reader
            )

            if result is None:
                continue

            if isinstance(result, list):

                candidates.extend(result)

            else:

                candidates.append(result)

        self.logger.info(
            "%d candidate profile(s) extracted.",
            len(candidates)
        )

        return candidates

    # =====================================================
    # Normalize One Candidate
    # =====================================================

    def normalize_candidate(
        self,
        candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes every normalizer on a candidate profile.
        """

        normalized = candidate

        for normalizer in self.normalizers:

            try:

                normalized = normalizer.normalize_candidate(
                    normalized
                )

            except Exception:

                self.logger.exception(

                    "%s failed.",

                    normalizer.__name__

                )

        return normalized

    # =====================================================
    # Normalize All Candidates
    # =====================================================

    def normalize_candidates(
        self,
        candidates: List[Dict]
    ) -> List[Dict]:
        """
        Executes normalization pipeline.
        """

        self.logger.info(
            "Normalization started."
        )

        normalized_profiles = []

        for candidate in candidates:

            normalized_profiles.append(

                self.normalize_candidate(
                    candidate
                )

            )

        self.logger.info(

            "%d profile(s) normalized.",

            len(normalized_profiles)

        )

        return normalized_profiles

    # =====================================================
    # Merge Candidates
    # =====================================================

    def merge_candidates(
        self,
        candidates: List[Dict]
    ) -> Dict[str, Any]:
        """
        Merge every normalized candidate into one
        canonical profile.
        """

        self.logger.info(
            "Merge phase started."
        )

        if not candidates:

            return empty_candidate()

        merged = self.merge_engine.merge(
            candidates
        )

        self.logger.info(
            "Merge completed."
        )

        return merged

    # =====================================================
    # Validate Canonical Profile
    # =====================================================

    def validate_canonical(
        self,
        candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validates canonical schema.
        """

        self.schema_validator.validate_candidate(
            candidate
        )

        self.logger.info(
            "Canonical schema validated."
        )

        return candidate

    # =====================================================
    # Projection
    # =====================================================

    def project_candidate(
        self,
        candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Projects canonical profile into the configured
        output schema.
        """

        self.logger.info(
            "Projection started."
        )

        projected = self.output_mapper.map_candidate(
            candidate
        )

        self.logger.info(
            "Projection completed."
        )

        return projected

    # =====================================================
    # Validate Projected Profile
    # =====================================================

    def validate_projected(
        self,
        projected: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validates projected output.
        """

        self.schema_validator.validate_projected(

            projected,

            self.config

        )

        self.logger.info(
            "Projected schema validated."
        )

        return projected

    # =====================================================
    # Write JSON
    # =====================================================

    def write_json(
        self,
        data: Dict[str, Any],
        filename: str
    ) -> Path:
        """
        Writes JSON into output directory.
        """

        output_file = self.output_directory / filename

        output_settings = self.config.get(

            "output",

            {}

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                data,

                file,

                indent=output_settings.get(
                    "indent",
                    4
                ),

                sort_keys=output_settings.get(
                    "sort_keys",
                    False
                ),

                ensure_ascii=False

            )

        self.logger.info(

            "Generated %s",

            output_file.name

        )

        return output_file

    # =====================================================
    # Save Pipeline Outputs
    # =====================================================

    def save_outputs(
        self,
        canonical: Dict[str, Any],
        projected: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Saves both canonical and projected profiles.
        """

        canonical_file = self.write_json(
            canonical,
            "canonical_profile.json"
        )

        projected_file = self.write_json(
            projected,
            "projected_profile.json"
        )

        return {

            "canonical": str(canonical_file),

            "projected": str(projected_file)

        }

    # =====================================================
    # Pipeline Statistics
    # =====================================================

    @staticmethod
    def pipeline_statistics(
        extracted: List[Dict],
        merged: Dict[str, Any],
        projected: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Returns execution statistics.
        """

        return {

            "profiles_extracted": len(extracted),

            "skills": len(
                merged.get("skills", [])
            ),

            "emails": len(
                merged.get("emails", [])
            ),

            "phones": len(
                merged.get("phones", [])
            ),

            "experience": len(
                merged.get("experience", [])
            ),

            "education": len(
                merged.get("education", [])
            ),

            "confidence": merged.get(
                "overall_confidence"
            ),

            "projected_fields": len(projected)

        }

    # =====================================================
    # Execute ETL
    # =====================================================

    def execute(self) -> Dict[str, Any]:
        """
        Executes the complete ETL pipeline.
        """

        self.logger.info("=" * 70)
        self.logger.info("CandidateOne ETL Pipeline Started")
        self.logger.info("=" * 70)

        # ------------------------------------------
        # Extraction
        # ------------------------------------------

        extracted = self.extract_candidates()

        if not extracted:

            raise RuntimeError(
                "No candidate data extracted."
            )

        # ------------------------------------------
        # Normalization
        # ------------------------------------------

        normalized = self.normalize_candidates(
            extracted
        )

        # ------------------------------------------
        # Merge
        # ------------------------------------------

        canonical = self.merge_candidates(
            normalized
        )

        # ------------------------------------------
        # Validate Canonical
        # ------------------------------------------

        self.validate_canonical(
            canonical
        )

        # ------------------------------------------
        # Projection
        # ------------------------------------------

        projected = self.project_candidate(
            canonical
        )

        # ------------------------------------------
        # Validate Projected
        # ------------------------------------------

        self.validate_projected(
            projected
        )

        # ------------------------------------------
        # Save Files
        # ------------------------------------------

        files = self.save_outputs(
            canonical,
            projected
        )

        statistics = self.pipeline_statistics(

            extracted,

            canonical,

            projected

        )

        self.logger.info("=" * 70)
        self.logger.info("Pipeline Completed Successfully")
        self.logger.info("=" * 70)

        return {

            "canonical": canonical,

            "projected": projected,

            "statistics": statistics,

            "files": files

        }

    # =====================================================
    # Public API
    # =====================================================

    def run(self) -> Dict[str, Any]:
        """
        Executes the pipeline.

        Public entry point.
        """

        try:

            return self.execute()

        except Exception:

            self.logger.exception(
                "Pipeline execution failed."
            )

            raise

    # =====================================================
    # Health
    # =====================================================

    def health(self) -> Dict[str, str]:
        """
        Returns pipeline health.
        """

        return {

            "pipeline": "CandidateOne",

            "status": "Ready",

            "configuration": str(
                self.config_loader.config_path
            ),

            "input_directory": str(
                self.input_directory
            ),

            "output_directory": str(
                self.output_directory
            )

        }

    # =====================================================
    # Available Sources
    # =====================================================

    def available_sources(self) -> List[str]:
        """
        Returns configured readers.
        """

        return [

            reader.__class__.__name__

            for reader in self.readers

        ]

    # =====================================================
    # Output Files
    # =====================================================

    def output_files(self) -> Dict[str, str]:
        """
        Returns expected output file locations.
        """

        return {

            "canonical":

                str(

                    self.output_directory /

                    "canonical_profile.json"

                ),

            "projected":

                str(

                    self.output_directory /

                    "projected_profile.json"

                )

        }

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(readers={len(self.readers)}, "

            f"normalizers={len(self.normalizers)})"

        )


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    pipeline = CandidatePipeline()

    result = pipeline.run()

    print("\nCandidateOne Pipeline Completed Successfully\n")

    print(

        json.dumps(

            result["statistics"],

            indent=4

        )

    )