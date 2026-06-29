"""
CandidateOne Custom Exceptions

Defines all project-specific exceptions used across the CandidateOne
ETL pipeline.

Using custom exceptions improves readability, debugging,
error handling, and logging.

"""

from typing import Optional


# ==========================================================
# Base Exception
# ==========================================================

class CandidateOneError(Exception):
    """
    Base exception for all CandidateOne errors.
    """

    def __init__(self, message: str = "CandidateOne application error"):
        self.message = message
        super().__init__(self.message)


# ==========================================================
# Extraction Errors
# ==========================================================

class ExtractionError(CandidateOneError):
    """
    Raised when a data source cannot be read or parsed.
    """

    def __init__(
        self,
        source: str,
        message: Optional[str] = None
    ):
        if message is None:
            message = f"Failed to extract data from '{source}'."

        self.source = source
        super().__init__(message)


# ==========================================================
# Parsing Errors
# ==========================================================

class ParsingError(CandidateOneError):
    """
    Raised when extracted content cannot be parsed.
    """

    def __init__(self, message="Unable to parse extracted content."):
        super().__init__(message)


# ==========================================================
# Normalization Errors
# ==========================================================

class NormalizationError(CandidateOneError):
    """
    Raised when a field cannot be normalized.
    """

    def __init__(
        self,
        field_name: str,
        value=None,
        message: Optional[str] = None
    ):

        if message is None:
            message = (
                f"Normalization failed for field "
                f"'{field_name}'. Value: {value}"
            )

        self.field_name = field_name
        self.value = value

        super().__init__(message)


# ==========================================================
# Merge Errors
# ==========================================================

class MergeError(CandidateOneError):
    """
    Raised when candidate profiles cannot be merged.
    """

    def __init__(self, message="Candidate merge failed."):
        super().__init__(message)


# ==========================================================
# Conflict Resolution Errors
# ==========================================================

class ConflictResolutionError(CandidateOneError):
    """
    Raised when conflicting field values cannot be resolved.
    """

    def __init__(
        self,
        field_name: str,
        message: Optional[str] = None
    ):

        if message is None:
            message = (
                f"Unable to resolve conflict "
                f"for field '{field_name}'."
            )

        self.field_name = field_name

        super().__init__(message)


# ==========================================================
# Projection Errors
# ==========================================================

class ProjectionError(CandidateOneError):
    """
    Raised when canonical data cannot be projected.
    """

    def __init__(self, message="Projection failed."):
        super().__init__(message)


# ==========================================================
# Validation Errors
# ==========================================================

class ValidationError(CandidateOneError):
    """
    Raised when schema validation fails.
    """

    def __init__(self, message="Schema validation failed."):
        super().__init__(message)


# ==========================================================
# Configuration Errors
# ==========================================================

class ConfigurationError(CandidateOneError):
    """
    Raised when runtime configuration is invalid.
    """

    def __init__(self, message="Invalid configuration."):
        super().__init__(message)


# ==========================================================
# Confidence Calculation Errors
# ==========================================================

class ConfidenceError(CandidateOneError):
    """
    Raised when confidence scores cannot be computed.
    """

    def __init__(self, message="Confidence calculation failed."):
        super().__init__(message)


# ==========================================================
# Provenance Errors
# ==========================================================

class ProvenanceError(CandidateOneError):
    """
    Raised when provenance information cannot be generated.
    """

    def __init__(self, message="Provenance generation failed."):
        super().__init__(message)


# ==========================================================
# File Errors
# ==========================================================

class FileTypeError(CandidateOneError):
    """
    Raised when an unsupported file type is supplied.
    """

    def __init__(
        self,
        file_name: str,
        message: Optional[str] = None
    ):

        if message is None:
            message = (
                f"Unsupported file type: {file_name}"
            )

        self.file_name = file_name

        super().__init__(message)


class FileMissingError(CandidateOneError):
    """
    Raised when an expected file is missing.
    """

    def __init__(
        self,
        file_path: str,
        message: Optional[str] = None
    ):

        if message is None:
            message = (
                f"Required file not found: {file_path}"
            )

        self.file_path = file_path

        super().__init__(message)

        # ==========================================================
# Backward Compatibility Aliases
# ==========================================================

# Older modules may import these names.
SchemaValidationError = ValidationError