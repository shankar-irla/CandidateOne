"""
Candidate Data Model

Represents the internal canonical candidate profile used throughout
the CandidateOne ETL pipeline.

"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class Candidate:
    """
    Internal representation of a candidate profile.
    """

    # -----------------------------
    # Basic Information
    # -----------------------------
    candidate_id: Optional[str] = None
    full_name: Optional[str] = None

    emails: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)

    # location = {"city": "...", "region": "...", "country": "..."}
    location: Dict[str, Optional[str]] = field(
        default_factory=lambda: {
            "city": None,
            "region": None,
            "country": None
        }
    )

    # Links
    links: Dict[str, Optional[str]] = field(
        default_factory=lambda: {
            "linkedin": None,
            "github": None,
            "portfolio": None,
            "other": []
        }
    )

    headline: Optional[str] = None
    years_experience: Optional[float] = None

    # Canonical Skills
    skills: List[str] = field(default_factory=list)

    # Experience Records
    experience: List[Dict] = field(default_factory=list)

    # Education Records
    education: List[Dict] = field(default_factory=list)

    # Provenance Information
    provenance: Dict[str, List[Dict]] = field(default_factory=dict)

    # Overall confidence
    overall_confidence: float = 0.0

    # Field level confidence
    field_confidence: Dict[str, float] = field(default_factory=dict)

    # Metadata
    source_count: int = 0

    metadata: Dict = field(default_factory=dict)

    # ----------------------------------------------------
    # Utility Methods
    # ----------------------------------------------------

    def add_email(self, email: str):
        """Adds an email if not already present."""
        if email and email not in self.emails:
            self.emails.append(email)

    def add_phone(self, phone: str):
        """Adds a phone number if not already present."""
        if phone and phone not in self.phones:
            self.phones.append(phone)

    def add_skill(self, skill: str):
        """Adds a normalized skill."""
        if skill and skill not in self.skills:
            self.skills.append(skill)

    def add_experience(self, record: Dict):
        """Adds an experience record."""
        if record:
            self.experience.append(record)

    def add_education(self, record: Dict):
        """Adds an education record."""
        if record:
            self.education.append(record)

    def add_provenance(
        self,
        field_name: str,
        source: str,
        method: str
    ):
        """
        Stores provenance information.

        Example:
        {
            "emails":[
                {
                    "source":"resume.pdf",
                    "method":"regex"
                }
            ]
        }
        """

        self.provenance.setdefault(field_name, [])

        self.provenance[field_name].append(
            {
                "source": source,
                "method": method
            }
        )

    def set_field_confidence(
        self,
        field_name: str,
        score: float
    ):
        """Stores confidence score for a field."""

        self.field_confidence[field_name] = round(
            float(score), 3
        )

    def to_dict(self) -> Dict:
        """Convert Candidate object into dictionary."""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict):
        """Create Candidate object from dictionary."""

        return cls(**data)