import csv
import os


class CSVReader:
    """
    Reads recruiter CSV files and converts them into
    a standardized internal candidate format.
    """

    REQUIRED_COLUMNS = [
        "name",
        "email",
        "phone",
        "current_company",
        "title"
    ]

    def __init__(self):
        self.source_name = "Recruiter CSV"

    def extract(self, file_path):
        """
        Reads the recruiter CSV file.

        Parameters
        ----------
        file_path : str

        Returns
        -------
        list
            List of standardized candidate dictionaries.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        candidates = []

        with open(file_path, "r", encoding="utf-8-sig") as file:

            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError("CSV file is empty.")

            missing_columns = [
                column
                for column in self.REQUIRED_COLUMNS
                if column not in reader.fieldnames
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {', '.join(missing_columns)}"
                )

            for row in reader:

                candidate = {
                    "candidate_id": None,

                    "full_name": self.clean(row.get("name")),

                    "emails": self.list_value(
                        self.clean(row.get("email"))
                    ),

                    "phones": self.list_value(
                        self.clean(row.get("phone"))
                    ),

                    "current_company": self.clean(
                        row.get("current_company")
                    ),

                    "title": self.clean(
                        row.get("title")
                    ),

                    "location": None,

                    "headline": None,

                    "years_experience": None,

                    "skills": [],

                    "experience": [],

                    "education": [],

                    "links": {},

                    "provenance": {},

                    "source": self.source_name
                }

                candidates.append(candidate)

        return candidates

    @staticmethod
    def clean(value):
        """
        Removes unnecessary spaces.
        Converts empty strings into None.
        """

        if value is None:
            return None

        value = value.strip()

        if value == "":
            return None

        return value

    @staticmethod
    def list_value(value):
        """
        Converts a single value into a list.
        """

        if value is None:
            return []

        return [value]