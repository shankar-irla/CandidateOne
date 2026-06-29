import os
import re
import pdfplumber
from docx import Document


class ResumeReader:
    """
    Reads PDF/DOCX resumes and extracts candidate information
    into CandidateOne's canonical internal schema.
    """

    def __init__(self):
        self.source_name = "Resume"

    def extract(self, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume not found: {file_path}")

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            text = self.read_pdf(file_path)

        elif extension == ".docx":
            text = self.read_docx(file_path)

        else:
            raise ValueError("Only PDF and DOCX resumes are supported.")

        return {
            "candidate_id": None,

            "full_name": self.extract_name(text),

            "emails": self.extract_emails(text),

            "phones": self.extract_phones(text),

            "current_company": None,

            "title": None,

            "location": None,

            "headline": None,

            "years_experience": None,

            "skills": self.extract_skills(text),

            "experience": [],

            "education": [],

            "links": self.extract_links(text),

            "provenance": {},

            "source": self.source_name
        }

    def read_pdf(self, file_path):

        text = ""

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    def read_docx(self, file_path):

        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    def extract_name(self, text):

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        if len(lines) == 0:
            return None

        return lines[0]

    def extract_emails(self, text):

        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        return list(set(re.findall(pattern, text)))

    def extract_phones(self, text):

        pattern = r"(?:\+91[- ]?)?[6-9]\d{9}"

        return list(set(re.findall(pattern, text)))

    def extract_links(self, text):

        links = {}

        linkedin = re.search(
            r"https?://(www\.)?linkedin\.com/\S+",
            text,
            re.IGNORECASE
        )

        github = re.search(
            r"https?://(www\.)?github\.com/\S+",
            text,
            re.IGNORECASE
        )

        if linkedin:
            links["linkedin"] = linkedin.group()

        if github:
            links["github"] = github.group()

        return links

    def extract_skills(self, text):

        skill_dictionary = [

            "Python",
            "Java",
            "C++",
            "SQL",
            "AWS",
            "Docker",
            "Kubernetes",
            "Flask",
            "Django",
            "TensorFlow",
            "PyTorch",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "Data Science",
            "Git",
            "REST API",
            "HTML",
            "CSS",
            "JavaScript"

        ]

        found = []

        lower_text = text.lower()

        for skill in skill_dictionary:

            if skill.lower() in lower_text:
                found.append(skill)

        return found