import json
import os


class ATSReader:
    """
    Reads ATS JSON data and converts it into the
    standardized CandidateOne candidate format.
    """

    def __init__(self):
        self.source_name = "ATS JSON"

    def extract(self, file_path):
        """
        Reads ATS JSON file.

        Parameters
        ----------
        file_path : str

        Returns
        -------
        list
            List of normalized candidate dictionaries.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"ATS file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            data = [data]

        candidates = []

        for record in data:

            candidate = {
                "candidate_id": self.clean(
                    record.get("candidateId")
                ),

                "full_name": self.clean(
                    record.get("candidateName")
                ),

                "emails": self.list_value(
                    self.clean(record.get("emailAddress"))
                ),

                "phones": self.list_value(
                    self.clean(record.get("mobile"))
                ),

                "current_company": self.clean(
                    record.get("organization")
                ),

                "title": self.clean(
                    record.get("designation")
                ),

                "location": self.clean(
                    record.get("location")
                ),

                "headline": self.clean(
                    record.get("headline")
                ),

                "years_experience": record.get("experience"),

                "skills": record.get("skills", []),

                "experience": record.get("workHistory", []),

                "education": record.get("education", []),

                "links": {},

                "provenance": {},

                "source": self.source_name
            }

            candidates.append(candidate)

        return candidates

    @staticmethod
    def clean(value):

        if value is None:
            return None

        value = str(value).strip()

        if value == "":
            return None

        return value

    @staticmethod
    def list_value(value):

        if value is None:
            return []

        return [value]