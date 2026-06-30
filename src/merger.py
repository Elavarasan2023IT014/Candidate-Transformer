from copy import deepcopy


class Merger:

    def __init__(self):

        # Higher value = Higher priority
        self.source_priority = {
            "resume": 2,
            "csv": 1
        }

    # ----------------------------------------------------

    def is_same_candidate(self, csv_data, resume_data):
        """
        Match candidates in the following order:
        1. Email
        2. Phone
        3. Name
        """

        # -------------------------
        # Email
        # -------------------------
        csv_email = csv_data.get("email")
        resume_email = resume_data.get("email")

        if csv_email and resume_email:
            if csv_email.strip().lower() == resume_email.strip().lower():
                return True

        # -------------------------
        # Phone
        # -------------------------
        csv_phone = csv_data.get("phone")
        resume_phone = resume_data.get("phone")

        if csv_phone and resume_phone:

            csv_phone = "".join(filter(str.isdigit, csv_phone))
            resume_phone = "".join(filter(str.isdigit, resume_phone))

            if csv_phone == resume_phone:
                return True

        # -------------------------
        # Name
        # -------------------------
        csv_name = csv_data.get("name")
        resume_name = resume_data.get("name")

        if csv_name and resume_name:
            if csv_name.strip().lower() == resume_name.strip().lower():
                return True

        return False

    # ----------------------------------------------------

    def merge(self, csv_data, resume_data):

        # Verify both inputs belong to same candidate
        if not self.is_same_candidate(csv_data, resume_data):
            raise Exception("CSV and Resume belong to different candidates.")

        profile = {

            "candidate_id": "CAND-001",

            "full_name": None,
            "emails": [],
            "phones": [],
            "headline": None,
            "current_company": None,
            "location": None,

            "skills": [],
            "experience": [],
            "education": [],

            "overall_confidence": 0,

            "provenance": []

        }

        confidence_scores = []

        # -------------------------
        # Name
        # -------------------------
        profile["full_name"] = self.choose_value(
            csv_data.get("name"),
            resume_data.get("name"),
            "full_name",
            profile
        )

        confidence_scores.append(95)

        # -------------------------
        # Email
        # -------------------------
        email = self.choose_value(
            csv_data.get("email"),
            resume_data.get("email"),
            "emails",
            profile
        )

        if email:
            profile["emails"] = [email]

        confidence_scores.append(98)

        # -------------------------
        # Phone
        # -------------------------
        phone = self.choose_value(
            csv_data.get("phone"),
            resume_data.get("phone"),
            "phones",
            profile
        )

        if phone:
            profile["phones"] = [phone]

        confidence_scores.append(97)

        # -------------------------
        # Current Company
        # -------------------------
        company = self.choose_value(
            csv_data.get("current_company"),
            resume_data.get("current_company"),
            "current_company",
            profile
        )

        profile["current_company"] = company

        confidence_scores.append(90)

        # -------------------------
        # Headline
        # -------------------------
        headline = self.choose_value(
            csv_data.get("title"),
            resume_data.get("title"),
            "headline",
            profile
        )

        profile["headline"] = headline

        confidence_scores.append(90)

        # -------------------------
        # Location
        # -------------------------
        location = self.choose_value(
            csv_data.get("location"),
            resume_data.get("location"),
            "location",
            profile
        )

        profile["location"] = location

        confidence_scores.append(90)

        # -------------------------
        # Skills
        # -------------------------
        profile["skills"] = self.merge_skills(
            csv_data.get("skills", []),
            resume_data.get("skills", [])
        )

        confidence_scores.append(92)

        # -------------------------
        # Experience
        # -------------------------
        profile["experience"] = deepcopy(
            resume_data.get("experience", [])
        )

        confidence_scores.append(95)

        # -------------------------
        # Education
        # -------------------------
        profile["education"] = deepcopy(
            resume_data.get("education", [])
        )

        confidence_scores.append(95)

        # -------------------------
        # Overall Confidence
        # -------------------------
        profile["overall_confidence"] = round(
            sum(confidence_scores) / len(confidence_scores),
            2
        )

        return profile

    # ----------------------------------------------------

    def choose_value(
        self,
        csv_value,
        resume_value,
        field,
        profile
    ):
        """
        Choose value based on source priority.
        """

        candidates = []

        if csv_value:
            candidates.append(("csv", csv_value))

        if resume_value:
            candidates.append(("resume", resume_value))

        if not candidates:
            return None

        source, value = max(
            candidates,
            key=lambda item: self.source_priority[item[0]]
        )

        profile["provenance"].append({

            "field": field,
            "source": source,
            "confidence": 0.95 if source == "resume" else 0.80

        })

        return value

    # ----------------------------------------------------

    def merge_skills(
        self,
        csv_skills,
        resume_skills
    ):

        merged = []
        seen = set()

        for skill in csv_skills + resume_skills:

            if skill not in seen:

                seen.add(skill)

                sources = []

                if skill in csv_skills:
                    sources.append("csv")

                if skill in resume_skills:
                    sources.append("resume")

                merged.append({

                    "name": skill,
                    "confidence": 0.90,
                    "sources": sources

                })

        return merged