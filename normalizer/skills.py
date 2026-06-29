"""
Skills Normalizer

Canonicalizes skill names.

"""

from __future__ import annotations

from typing import List


SKILL_ALIASES = {

    "ml": "Machine Learning",

    "machine learning": "Machine Learning",

    "ai": "Artificial Intelligence",

    "artificial intelligence": "Artificial Intelligence",

    "js": "JavaScript",

    "javascript": "JavaScript",

    "py": "Python",

    "python": "Python",

    "sql": "SQL",

    "mysql": "MySQL",

    "postgres": "PostgreSQL",

    "postgresql": "PostgreSQL",

    "c++": "C++",

    "cpp": "C++",

    "node": "Node.js",

    "nodejs": "Node.js",

    "reactjs": "React",

    "react": "React",

    "html": "HTML",

    "css": "CSS",

    "flask": "Flask",

    "django": "Django"
}


class SkillNormalizer:

    @classmethod
    def normalize(
        cls,
        skill: str
    ) -> str:

        if not skill:
            return ""

        skill = skill.strip()

        key = skill.lower()

        return SKILL_ALIASES.get(
            key,
            skill.title()
        )

    @classmethod
    def normalize_list(
        cls,
        skills: List[str]
    ) -> List[str]:

        normalized = []

        seen = set()

        for skill in skills:

            value = cls.normalize(skill)

            if not value:
                continue

            if value in seen:
                continue

            seen.add(value)

            normalized.append(value)

        return normalized

    @classmethod
    def normalize_candidate(
        cls,
        candidate: dict
    ) -> dict:

        candidate["skills"] = cls.normalize_list(
            candidate.get("skills", [])
        )

        return candidate