from copy import deepcopy


class Merger:

    def __init__(self):

        # Source priority
        # Higher value = More trusted
        self.source_priority = {
            "resume": 2,
            "csv": 1
        }

    # ----------------------------------------------------

    def merge(self, csv_data, resume_data):

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
        # Company
        # -------------------------

        company = self.choose_value(
            csv_data.get("current_company"),
            None,
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
            None,
            "headline",
            profile
        )

        profile["headline"] = headline

        confidence_scores.append(90)

        # -------------------------
        # Location
        # -------------------------

        location = self.choose_value(
            None,
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

        if resume_value:

            profile["provenance"].append({

                "field": field,
                "source": "resume",
                "confidence": 0.95

            })

            return resume_value

        if csv_value:

            profile["provenance"].append({

                "field": field,
                "source": "csv",
                "confidence": 0.80

            })

            return csv_value

        return None

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

                merged.append({

                    "name": skill,

                    "confidence": 0.90,

                    "sources": ["resume"]
                    if skill in resume_skills
                    else ["csv"]

                })

        return merged