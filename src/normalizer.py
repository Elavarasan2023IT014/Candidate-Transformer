import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError


class Normalizer:

    def __init__(self):

        # Skill normalization dictionary
        self.skill_map = {
            "reactjs": "React",
            "react.js": "React",
            "node js": "Node.js",
            "nodejs": "Node.js",
            "js": "JavaScript",
            "javascript": "JavaScript",
            "py": "Python",
            "ml": "Machine Learning",
            "machine learning": "Machine Learning",
            "sql": "SQL",
            "java": "Java",
            "python": "Python"
        }

    # ---------------------------------------

    def normalize(self, candidate):

        candidate["name"] = self.normalize_name(
            candidate.get("name")
        )

        candidate["email"] = self.normalize_email(
            candidate.get("email")
        )

        candidate["phone"] = self.normalize_phone(
            candidate.get("phone")
        )

        candidate["skills"] = self.normalize_skills(
            candidate.get("skills", [])
        )

        candidate["location"] = self.normalize_location(
            candidate.get("location")
        )

        return candidate

    # ---------------------------------------

    def normalize_name(self, name):

        if not name:
            return None

        name = name.strip()

        return " ".join(
            word.capitalize()
            for word in name.split()
        )

    # ---------------------------------------

    def normalize_email(self, email):

        if not email:
            return None

        email = email.strip().lower()

        try:
            validate_email(email, check_deliverability=False)
            return email

        except EmailNotValidError:
            return None

    # ---------------------------------------

    def normalize_phone(self, phone):

        if not phone:
            return None

        phone = re.sub(r"[^\d+]", "", phone)

        try:

            parsed = phonenumbers.parse(phone, "IN")

            if phonenumbers.is_valid_number(parsed):

                return phonenumbers.format_number(
                    parsed,
                    phonenumbers.PhoneNumberFormat.E164
                )

        except:
            pass

        return phone

    # ---------------------------------------

    def normalize_skills(self, skills):

        normalized = []

        seen = set()

        for skill in skills:

            key = skill.strip().lower()

            if key in self.skill_map:
                value = self.skill_map[key]
            else:
                value = skill.strip().title()

            if value not in seen:

                seen.add(value)

                normalized.append(value)

        return normalized

    # ---------------------------------------

    def normalize_location(self, location):

        if not location:
            return None

        location = re.sub(r"\s+", " ", location)

        return location.strip()