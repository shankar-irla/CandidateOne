"""
CandidateOne Constants

Centralized constants used throughout the CandidateOne ETL pipeline.

Keeping application-wide constants here avoids hardcoded values across
multiple modules and makes maintenance significantly easier.

Author: Shankar Irla
"""

from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = PROJECT_ROOT / "config"
INPUT_DIR = PROJECT_ROOT / "sample_input"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"
DOCS_DIR = PROJECT_ROOT / "docs"

DEFAULT_CONFIG_FILE = CONFIG_DIR / "default_config.json"
CUSTOM_CONFIG_FILE = CONFIG_DIR / "custom_config.json"

CANONICAL_OUTPUT_FILE = OUTPUT_DIR / "canonical_profile.json"
PROJECTED_OUTPUT_FILE = OUTPUT_DIR / "projected_profile.json"

# ==========================================================
# SUPPORTED FILE TYPES
# ==========================================================

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".json",
    ".pdf"
}

SUPPORTED_SOURCES = {
    "resume",
    "linkedin",
    "github",
    "ats",
    "recruiter_csv"
}

# ==========================================================
# SOURCE PRIORITY
# Higher value = more trusted
# Used by conflict_resolver.py
# ==========================================================

SOURCE_PRIORITY = {

    "resume": 100,

    "linkedin": 95,

    "ats": 90,

    "github": 85,

    "recruiter_csv": 80
}

# ==========================================================
# DEFAULT FIELD CONFIDENCE
# Used if no custom confidence is calculated.
# ==========================================================

DEFAULT_FIELD_CONFIDENCE = {

    "candidate_id": 1.00,

    "full_name": 0.98,

    "emails": 0.98,

    "phones": 0.95,

    "location": 0.90,

    "headline": 0.90,

    "years_experience": 0.88,

    "skills": 0.92,

    "experience": 0.95,

    "education": 0.95,

    "links": 0.95
}

# ==========================================================
# PHONE
# ==========================================================

DEFAULT_COUNTRY_CODE = "IN"

# ==========================================================
# DATE FORMAT
# ==========================================================

STANDARD_DATE_FORMAT = "%Y-%m"

# ==========================================================
# EMAIL
# ==========================================================

EMAIL_LOWERCASE = True

# ==========================================================
# LOCATION ALIASES
# Used by location.py
# ==========================================================

COUNTRY_ALIASES = {

    "india": "IN",

    "bharat": "IN",

    "usa": "US",

    "united states": "US",

    "united states of america": "US",

    "uk": "GB",

    "england": "GB",

    "uae": "AE"
}

# ==========================================================
# SKILL NORMALIZATION
# Used by skills.py
# ==========================================================

SKILL_ALIASES = {

    "py": "Python",

    "python3": "Python",

    "python 3": "Python",

    "js": "JavaScript",

    "node": "Node.js",

    "nodejs": "Node.js",

    "reactjs": "React",

    "react.js": "React",

    "ml": "Machine Learning",

    "ai": "Artificial Intelligence",

    "nlp": "Natural Language Processing",

    "sql server": "SQL",

    "postgres": "PostgreSQL",

    "postgresql": "PostgreSQL",

    "mongo": "MongoDB",

    "mongodb": "MongoDB",

    "git hub": "GitHub",

    "c plus plus": "C++"
}

# ==========================================================
# OUTPUT FILE NAMES
# ==========================================================

CANONICAL_JSON_NAME = "canonical_profile.json"

PROJECTED_JSON_NAME = "projected_profile.json"

# ==========================================================
# MERGE SETTINGS
# ==========================================================

ALLOW_EMPTY_VALUES = False

REMOVE_DUPLICATES = True

SKILL_CASE_SENSITIVE = False

# ==========================================================
# EXPERIENCE SETTINGS
# ==========================================================

MAX_EXPERIENCE_YEARS = 60

# ==========================================================
# LOGGING
# ==========================================================

LOGGER_NAME = "CandidateOne"

# ==========================================================
# VALIDATION
# ==========================================================

MIN_CONFIDENCE = 0.0

MAX_CONFIDENCE = 1.0

# ==========================================================
# DEFAULT ENCODING
# ==========================================================

FILE_ENCODING = "utf-8"

# ==========================================================
# APPLICATION
# ==========================================================

APPLICATION_NAME = "CandidateOne"

APPLICATION_VERSION = "1.0.0"

AUTHOR = "Shankar Irla"