"""
Resume Quality Scoring Configuration

Defines weights used by the Resume Report Engine.
Total Score = 100
"""


# Structure Score (25)

STRUCTURE_WEIGHTS = {
    "skills": 6,
    "projects": 7,
    "experience": 7,
    "education": 5,
}


# Contact Score (15)

CONTACT_WEIGHTS = {
    "email": 4,
    "phone": 4,
    "github": 3,
    "linkedin": 4,
}


# Content Score (35)

CONTENT_WEIGHTS = {
    "quantified": 12,
    "action_verbs": 10,
    "bullet_points": 5,
    "resume_length": 8,
}


# Professional Presence (10)

PROFESSIONAL_WEIGHTS = {
    "github": 5,
    "linkedin": 5,
}


# ATS Friendliness (15)

ATS_WEIGHTS = {
    "standard_sections": 4,
    "skills_section": 3,
    "contact_information": 3,
    "resume_length": 3,
    "bullet_points": 2,
}


# GRADE THRESHOLDS

GRADE_THRESHOLDS = {

    "A+": 90,

    "A": 80,

    "B": 70,

    "C": 60,

    "Needs Improvement": 0
}


# GRADE DESCRIPTIONS

GRADE_DESCRIPTIONS = {

    "A+": "Outstanding resume. Highly ATS-friendly with excellent technical presentation.",

    "A": "Strong resume with only minor improvements recommended.",

    "B": "Good resume but several areas can be strengthened.",

    "C": "Average resume. Significant improvements are recommended.",

    "Needs Improvement": "Resume requires major improvements before applying."
}