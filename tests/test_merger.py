import sys
import os
import pytest

# Add src folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from merger import Merger


def test_merge_candidate():

    csv_data = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "phone": "+919876543210",
        "current_company": "Google",
        "title": "Software Engineer",
        "skills": ["Python"]
    }

    resume_data = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "phone": "+919876543210",
        "location": "Chennai",
        "skills": [
            "Python",
            "React",
            "SQL"
        ],
        "experience": [
            {
                "company": "Google",
                "title": "Software Engineer",
                "duration": "Jan 2022 - Present",
                "summary": "Backend Development"
            }
        ],
        "education": [
            {
                "degree": "B.Tech",
                "institution": "ABC Engineering College",
                "year": "2022"
            }
        ]
    }

    merger = Merger()

    profile = merger.merge(csv_data, resume_data)

    assert profile["full_name"] == "John Doe"

    assert profile["emails"][0] == "john.doe@gmail.com"

    assert profile["phones"][0] == "+919876543210"

    assert profile["headline"] == "Software Engineer"

    assert profile["current_company"] == "Google"

    assert profile["location"] == "Chennai"

    assert len(profile["skills"]) == 3

    assert len(profile["experience"]) == 1

    assert len(profile["education"]) == 1

    assert profile["overall_confidence"] > 90

    assert len(profile["provenance"]) > 0


def test_resume_priority():

    csv_data = {
        "name": "John Doe",
        "email": "john@gmail.com"
    }

    resume_data = {
        "name": "Johnathan Doe",
        "email": "john@gmail.com"
    }

    merger = Merger()

    profile = merger.merge(csv_data, resume_data)

    # Resume should win
    assert profile["full_name"] == "Johnathan Doe"


def test_missing_resume_values():

    csv_data = {
        "name": "John Doe",
        "email": "john@gmail.com",
        "phone": "+919876543210",
        "current_company": "Google",
        "title": "Software Engineer"
    }

    # Resume has only identity information
    resume_data = {
        "email": "john@gmail.com"
    }

    merger = Merger()

    profile = merger.merge(csv_data, resume_data)

    assert profile["full_name"] == "John Doe"

    assert profile["emails"][0] == "john@gmail.com"

    assert profile["current_company"] == "Google"


def test_skill_merge():

    csv_data = {
        "name": "John Doe",
        "email": "john@gmail.com",
        "skills": [
            "Python"
        ]
    }

    resume_data = {
        "name": "John Doe",
        "email": "john@gmail.com",
        "skills": [
            "Python",
            "React",
            "SQL"
        ]
    }

    merger = Merger()

    profile = merger.merge(csv_data, resume_data)

    skill_names = [skill["name"] for skill in profile["skills"]]

    assert "Python" in skill_names

    assert "React" in skill_names

    assert "SQL" in skill_names

    assert len(skill_names) == 3


def test_different_candidate():

    csv_data = {
        "name": "John Doe",
        "email": "john@gmail.com"
    }

    resume_data = {
        "name": "Alice Smith",
        "email": "alice@gmail.com"
    }

    merger = Merger()

    with pytest.raises(Exception) as exc:

        merger.merge(csv_data, resume_data)

    assert "different candidates" in str(exc.value).lower()