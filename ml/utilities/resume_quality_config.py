"""
Resume Quality Scoring Configuration

Defines weights used by the Resume Report Engine.
Total Score = 100
"""


# Structure Score (30)

STRUCTURE_WEIGHTS = {
    "skills": 8,
    "projects": 9,
    "experience": 6,
    "education": 7,
}


# Contact Score (15)

CONTACT_WEIGHTS = {
    "email": 4,
    "phone": 4,
    "github": 3,
    "linkedin": 4,
}


# Content Score (40)

CONTENT_WEIGHTS = {
    "quantified": 15,
    "action_verbs": 11,
    "bullet_points": 5,
    "resume_length": 9,
}


# Professional Presence (15)

PROFESSIONAL_WEIGHTS = {
    "github": 9,
    "linkedin": 6,
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