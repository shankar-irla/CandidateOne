"""
Base Reader

Defines the abstract interface that every data extractor
must implement.

All source readers (CSV, ATS, Resume, GitHub, LinkedIn)
inherit from this class.

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from utils.logger import get_logger
from utils.exceptions import (
    ExtractionError,
    FileMissingError,
    FileTypeError,
)
from utils.constants import SUPPORTED_EXTENSIONS


class BaseReader(ABC):
    """
    Abstract base class for all input readers.

    Responsibilities
    ----------------
    1. Validate input file
    2. Read source
    3. Parse source
    4. Return standardized dictionary
    """

    def __init__(self, file_path: str | Path):

        self.file_path = Path(file_path)

        self.logger = get_logger(self.__class__.__name__)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_file(self) -> None:
        """
        Validates that the input file exists and has a supported
        extension.
        """

        if not self.file_path.exists():
            raise FileMissingError(str(self.file_path))

        extension = self.file_path.suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            raise FileTypeError(str(self.file_path))

    # ---------------------------------------------------------
    # Pipeline Entry
    # ---------------------------------------------------------

    def extract(self) -> Dict[str, Any]:
        """
        Standard extraction pipeline.

        Every reader follows:

            Validate
                ↓
            Read
                ↓
            Parse
                ↓
            Return Dictionary
        """

        self.validate_file()

        self.logger.info(
            "Reading source: %s",
            self.file_path.name
        )

        try:

            raw_data = self.read()

            parsed = self.parse(raw_data)

            self.logger.info(
                "Successfully extracted %s",
                self.file_path.name
            )

            return parsed

        except Exception as exc:

            self.logger.exception(
                "Extraction failed for %s",
                self.file_path.name
            )

            raise ExtractionError(
                source=self.file_path.name,
                message=str(exc)
            ) from exc

    # ---------------------------------------------------------
    # Abstract Methods
    # ---------------------------------------------------------

    @abstractmethod
    def read(self) -> Any:
        """
        Reads raw content from the source.

        Returns
        -------
        Any
            Raw source content.
        """
        raise NotImplementedError

    @abstractmethod
    def parse(self, raw_data: Any) -> Dict[str, Any]:
        """
        Converts raw content into the internal candidate
        dictionary.

        Parameters
        ----------
        raw_data : Any

        Returns
        -------
        dict
        """
        raise NotImplementedError