import pdfplumber
import re


class ResumeExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        """
        Extract text from PDF.
        """

        text = ""

        try:
            with pdfplumber.open(self.pdf_path) as pdf:

                for page in pdf.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

        except FileNotFoundError:
            raise Exception(f"Resume not found: {self.pdf_path}")

        except Exception as e:
            raise Exception(f"Unable to read PDF: {e}")

        return text

    def extract(self):

        text = self.extract_text()

        candidate = {}

        # -----------------------------
        # Name (First line)
        # -----------------------------
        lines = text.split("\n")

        candidate["name"] = lines[0].strip() if lines else None

        # -----------------------------
        # Email
        # -----------------------------
        email = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        candidate["email"] = email.group(0) if email else None

        # -----------------------------
        # Phone
        # -----------------------------
        phone = re.search(
            r"(\+?\d[\d\s-]{9,15})",
            text
        )

        candidate["phone"] = phone.group(0).strip() if phone else None

        # -----------------------------
        # Location
        # -----------------------------
        location = re.search(
            r"Location:\s*(.*)",
            text
        )

        candidate["location"] = (
            location.group(1).strip()
            if location else None
        )

        # -----------------------------
        # Skills
        # -----------------------------
        candidate["skills"] = self.extract_skills(text)

        # -----------------------------
        # Experience
        # -----------------------------
        candidate["experience"] = self.extract_experience(text)

        # -----------------------------
        # Education
        # -----------------------------
        candidate["education"] = self.extract_education(text)

        return candidate

    # ------------------------------------------------------

    def extract_skills(self, text):

        skills = []

        match = re.search(
            r"Skills(.*?)Experience",
            text,
            re.DOTALL | re.IGNORECASE
        )

        if match:

            section = match.group(1)

            for line in section.split("\n"):

                line = line.strip()

                if line:
                    skills.append(line)

        return skills

    # ------------------------------------------------------

    def extract_experience(self, text):

        experience = []

        match = re.search(
            r"Experience(.*?)Education",
            text,
            re.DOTALL | re.IGNORECASE
        )

        if match:

            lines = [
                x.strip()
                for x in match.group(1).split("\n")
                if x.strip()
            ]

            if len(lines) >= 4:

                experience.append({

                    "company": lines[0],

                    "title": lines[1],

                    "duration": lines[2],

                    "summary": lines[3]

                })

        return experience

    # ------------------------------------------------------

    def extract_education(self, text):

        education = []

        match = re.search(
            r"Education(.*)",
            text,
            re.DOTALL | re.IGNORECASE
        )

        if match:

            lines = [
                x.strip()
                for x in match.group(1).split("\n")
                if x.strip()
            ]

            if len(lines) >= 3:

                education.append({

                    "degree": lines[0],

                    "institution": lines[1],

                    "year": lines[2]

                })

        return education