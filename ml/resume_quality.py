"""
Resume Quality Analyzer

Analyzes the resume itself for ATS-friendly structure
and overall completeness. """

import re
from ml.utilities.resume_quality_config import (
    STRUCTURE_WEIGHTS,
    CONTACT_WEIGHTS,
    CONTENT_WEIGHTS,
    PROFESSIONAL_WEIGHTS,
    ATS_WEIGHTS,
    GRADE_THRESHOLDS,
    GRADE_DESCRIPTIONS,
)
from ml.utilities.resume_recommendation_data import (
    RESUME_RECOMMENDATIONS
)


# INCLUDE SECTIONS

SECTION_PATTERNS = {

    "skills": [
        "skills",
        "technical skills",
        "technologies"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internships"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualifications"
    ]
}


def detect_sections(resume_text: str) -> dict:
    """ Detects whether important resume sections exist. """

    text = resume_text.lower()

    results = {}

    for section, keywords in SECTION_PATTERNS.items():

        results[section] = any(
            keyword in text
            for keyword in keywords
        )

    return results


# CONTACT INFORMATION

EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

PHONE_PATTERN = (
    r"(?:\+?\d{1,3}[- ]?)?"
    r"(?:\(?\d{3}\)?[- ]?)?"
    r"\d{3}[- ]?\d{4,6}"
)

GITHUB_PATTERN = r"(github\.com/[^\s]+)"

LINKEDIN_PATTERN = r"(linkedin\.com/in/[^\s]+)"


def detect_contact_information(resume_text: str) -> dict:
    """ Detects important contact information
    present in the resume. """

    text = resume_text.lower()

    return {

        "email": bool(
            re.search(
                EMAIL_PATTERN,
                text
            )
        ),

        "phone": bool(
            re.search(
                PHONE_PATTERN,
                text
            )
        ),

        "github": bool(
            re.search(
                GITHUB_PATTERN,
                text
            )
        ),

        "linkedin": bool(
            re.search(
                LINKEDIN_PATTERN,
                text
            )
        )
    }


# QUANTIFIED ACHIEVEMENTS

NUMBER_PATTERN = r"\b\d+(\.\d+)?(%|\+|x|k|m|b)?\b"

def detect_quantified_achievements(resume_text: str) -> dict:
    """
    Detects resume bullet points that contain
    measurable achievements.

    Example:
    • Increased API speed by 35%
    • Solved 400+ DSA problems
    """

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    number_pattern = re.compile(r"\b\d+(?:\.\d+)?(?:%|\+|x|k|m|b)?\b", re.IGNORECASE)

    achievement_verbs = {
        "built",
        "developed",
        "designed",
        "implemented",
        "optimized",
        "created",
        "led",
        "improved",
        "automated",
        "deployed",
        "engineered",
        "integrated",
        "managed",
        "reduced",
        "increased",
        "enhanced",
        "analyzed",
        "collaborated",
        "mentored",
        "organized",
        "delivered",
        "achieved",
        "launched",
        "solved",
        "spearheaded",
        "streamlined",
        "innovated",
        "transformed",
    }

    count = 0
    matched_lines = []

    for line in lines:

        lower_line = line.lower()

        has_number = bool(number_pattern.search(lower_line))

        has_action = any(
            verb in lower_line
            for verb in achievement_verbs
        )

        if has_number and has_action:
            count += 1
            matched_lines.append(line)

    return {
        "count": count,
        "present": count > 0,
        "examples": matched_lines,
    }

# ACTION VERBS

ACTION_VERBS = {

    "built",
    "developed",
    "designed",
    "implemented",
    "optimized",
    "created",
    "led",
    "improved",
    "automated",
    "deployed",
    "engineered",
    "integrated",
    "managed",
    "reduced",
    "increased",
    "enhanced",
    "analyzed",
    "collaborated",
}

def detect_action_verbs(resume_text: str) -> dict:
    """
    Detects strong action verbs commonly used
    in impactful resumes.
    """

    text = resume_text.lower()

    found = []

    for verb in ACTION_VERBS:
        if verb in text:
            found.append(verb)

    return {
        "count": len(found),
        "verbs": sorted(found),
        "present": len(found) > 0
    }


# BULLET POINTS

def detect_bullet_points(resume_text: str) -> dict:
    """
    Detects actual bullet point entries in the resume.
    """

    lines = resume_text.splitlines()

    bullet_pattern = re.compile(
        r"^\s*(?:•|\*|-|–|→|»)\s+"
    )

    bullet_lines = []

    for line in lines:

        if bullet_pattern.match(line):
            bullet_lines.append(line.strip())

    return {
        "count": len(bullet_lines),
        "present": len(bullet_lines) > 0,
        "examples": bullet_lines
    }


# RESUME LENGTH

def analyze_resume_length(resume_text: str) -> dict:
    """
    Estimates resume length using word count.
    """

    words = resume_text.split()

    count = len(words)

    if count < 250:
        category = "Short"

    elif count <= 700:
        category = "Good"

    else:
        category = "Long"

    return {
        "word_count": count,
        "category": category
    }


# RESUME QUALITY ANALYSIS

def analyze_resume_quality(resume_text: str) -> dict:
    """
    Runs all resume quality analyzers and
    returns a complete quality report.
    """

    sections = detect_sections(resume_text)

    contact = detect_contact_information(resume_text)

    quantified = detect_quantified_achievements(resume_text)

    action_verbs = detect_action_verbs(resume_text)

    bullets = detect_bullet_points(resume_text)

    length = analyze_resume_length(resume_text)

    return {
        "sections": sections,
        "contact_information": contact,
        "quantified_achievements": quantified,
        "action_verbs": action_verbs,
        "bullet_points": bullets,
        "resume_length": length
    }


def build_ats_diagnostics(report: dict) -> dict:
    sections_present = sum(report["sections"].values())
    contact_present = sum(report["contact_information"].values())

    section_score = (sections_present / len(report["sections"])) * ATS_WEIGHTS["standard_sections"]
    skills_score = ATS_WEIGHTS["skills_section"] if report["sections"]["skills"] else 0
    contact_score = (contact_present / len(report["contact_information"])) * ATS_WEIGHTS["contact_information"]
    length_score = ATS_WEIGHTS["resume_length"] if report["resume_length"]["category"] == "Good" else 0
    bullet_score = ATS_WEIGHTS["bullet_points"] if report["bullet_points"]["present"] else 0

    ats_score = round(((section_score + skills_score + contact_score + length_score + bullet_score) / 15) * 100, 2)

    return {
        "score": ats_score,
        "sections": report["sections"],
        "contact_information": report["contact_information"],
        "bullet_points": report["bullet_points"],
        "resume_length": report["resume_length"],
    }

def get_resume_grade(score: float) -> tuple:
    """
    Returns the resume grade and description.
    """

    for grade, threshold in GRADE_THRESHOLDS.items():
        if score >= threshold:
            return grade, GRADE_DESCRIPTIONS[grade]

    return "Needs Improvement", GRADE_DESCRIPTIONS["Needs Improvement"]


def generate_resume_summary(
    report: dict,
    overall_score: float,
) -> str:
    """
    Generates a dynamic summary for the resume.
    """

    strengths = []

    improvements = []

    if all(report["sections"].values()):
        strengths.append("well-structured")

    if report["quantified_achievements"]["count"] >= 3:
        strengths.append("impact-oriented")

    if report["action_verbs"]["count"] >= 5:
        strengths.append("strong action verbs")

    if not report["contact_information"]["linkedin"]:
        improvements.append("add LinkedIn")

    if report["quantified_achievements"]["count"] < 3:
        improvements.append("include more measurable achievements")

    if report["action_verbs"]["count"] < 5:
        improvements.append("strengthen project descriptions")

    if overall_score >= 90:
        opening = "Excellent resume"

    elif overall_score >= 80:
        opening = "Strong resume"

    elif overall_score >= 70:
        opening = "Good resume"

    else:
        opening = "Resume needs improvement"

    summary = opening

    if strengths:
        summary += " with " + ", ".join(strengths)

    if improvements:
        summary += ". Recommended next steps: " + ", ".join(improvements)

    return summary + "."


def compute_resume_quality_score(report: dict) -> dict:
    """
    Computes Resume Quality Score from
    the analysis report.
    """


    # Structure Score

    structure_score = 0

    for section, weight in STRUCTURE_WEIGHTS.items():
        if report["sections"][section]:
            structure_score += weight


    # Contact Score

    contact_score = 0

    for field, weight in CONTACT_WEIGHTS.items():
        if report["contact_information"][field]:
            contact_score += weight


    # Content Score

    content_score = 0

    count = report["quantified_achievements"]["count"]

    if count >= 5:
        content_score += CONTENT_WEIGHTS["quantified"]

    elif count >= 3:
        content_score += round(
            CONTENT_WEIGHTS["quantified"] * 0.8
        )

    elif count >= 1:
        content_score += round(
            CONTENT_WEIGHTS["quantified"] * 0.5
        )

    if report["action_verbs"]["count"] >= 5:
        content_score += CONTENT_WEIGHTS["action_verbs"]

    elif report["action_verbs"]["count"] >= 3:
        content_score += round(
            CONTENT_WEIGHTS["action_verbs"] * 0.7
        )

    elif report["action_verbs"]["count"] >= 1:
        content_score += round(
            CONTENT_WEIGHTS["action_verbs"] * 0.4
        )

    bullet_count = report["bullet_points"]["count"]

    if bullet_count >= 6:

        content_score += CONTENT_WEIGHTS["bullet_points"]

    elif bullet_count >= 3:

        content_score += round(
            CONTENT_WEIGHTS["bullet_points"] * 0.7
        )

    elif bullet_count >= 1:

        content_score += round(
            CONTENT_WEIGHTS["bullet_points"] * 0.4
        )

    if report["resume_length"]["category"] == "Good":
        content_score += CONTENT_WEIGHTS["resume_length"]

    elif report["resume_length"]["category"] == "Long":
        content_score += round(
            CONTENT_WEIGHTS["resume_length"] * 0.5
        )


    # Professional Presence

    professional_score = 0

    if report["contact_information"]["github"]:
        professional_score += PROFESSIONAL_WEIGHTS["github"]

    if report["contact_information"]["linkedin"]:
        professional_score += PROFESSIONAL_WEIGHTS["linkedin"]


    # Overall Score

    overall_score = (
        structure_score
        + contact_score
        + content_score
        + professional_score
    )

    overall_score = round(overall_score, 2)

    grade, _ = get_resume_grade(overall_score)

    summary = generate_resume_summary(
        report,
        overall_score,
    )

    score_breakdown = {

    "structure": {
        "score": structure_score,
        "max_score": sum(STRUCTURE_WEIGHTS.values())
    },

    "contact": {
        "score": contact_score,
        "max_score": sum(CONTACT_WEIGHTS.values())
    },

    "content": {
        "score": content_score,
        "max_score": sum(CONTENT_WEIGHTS.values())
    },

    "professional": {
        "score": professional_score,
        "max_score": sum(PROFESSIONAL_WEIGHTS.values())
    }
}

    return {
        "overall_score": overall_score,
        "grade": grade,
        "summary": summary,
        "structure_score": structure_score,
        "contact_score": contact_score,
        "content_score": content_score,
        "professional_score": professional_score,
        "score_breakdown": score_breakdown
    }




def generate_resume_recommendations(
    report: dict,
) -> list:
    """
    Generates personalized recommendations
    based on the Resume Report.
    """

    recommendations = []


    # Structure

    sections = report["sections"]

    if not sections["skills"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_skills_section"]
        )

    if not sections["projects"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_projects"]
        )

    if not sections["experience"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_experience"]
        )

    if not sections["education"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_education"]
        )

    
    # Contact
    
    contact = report["contact_information"]

    if not contact["email"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_email"]
        )

    if not contact["phone"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_phone"]
        )

    if not contact["github"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_github"]
        )

    if not contact["linkedin"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_linkedin"]
        )

    
    # Content
    
    if report["action_verbs"]["count"] < 5:
        recommendations.append(
            RESUME_RECOMMENDATIONS["few_action_verbs"]
        )

    if report["quantified_achievements"]["count"] < 3:
        recommendations.append(
            RESUME_RECOMMENDATIONS["few_quantified_achievements"]
        )

    if not report["bullet_points"]["present"]:
        recommendations.append(
            RESUME_RECOMMENDATIONS["missing_bullets"]
        )

    length = report["resume_length"]["category"]

    if length == "Short":
        recommendations.append(
            RESUME_RECOMMENDATIONS["resume_short"]
        )

    elif length == "Long":
        recommendations.append(
            RESUME_RECOMMENDATIONS["resume_long"]
        )

    return recommendations



def generate_resume_strengths(report: dict) -> list:
    """
    Identifies the strengths of the resume.
    """

    strengths = []

    # Structure

    if all(report["sections"].values()):
        strengths.append(
            "Excellent resume structure with all major sections present."
        )

    # Contact

    if all(report["contact_information"].values()):
        strengths.append(
            "Professional contact information is complete."
        )

    # Content

    if report["action_verbs"]["count"] >= 2:
        strengths.append(
            "Uses strong action verbs throughout the resume."
        )

    if report["sections"]["skills"]:
        strengths.append(
            "Well-defined technical skills section."
        )

    if report["sections"]["experience"]:
        strengths.append(
            "Includes relevant work experience."
        )

    if report["quantified_achievements"]["count"] >= 3:
        strengths.append(
            "Includes measurable achievements that demonstrate impact."
        )

    if report["bullet_points"]["present"]:
        strengths.append(
            "Good use of bullet points for readability."
        )

    if report["resume_length"]["category"] == "Good":
        strengths.append(
            "Resume length is well balanced."
        )

    return strengths




def generate_priority_improvements(report: dict) -> list:
    """
    Returns the three highest priority improvements.
    """

    priorities = []

    if report["quantified_achievements"]["count"] < 3:
        priorities.append(
            "Add measurable achievements to projects and experience."
        )

    if not report["contact_information"]["github"]:
        priorities.append(
            "Include your GitHub profile."
        )

    if not report["contact_information"]["linkedin"]:
        priorities.append(
            "Include your LinkedIn profile."
        )

    if report["action_verbs"]["count"] < 5:
        priorities.append(
            "Improve project descriptions using stronger action verbs."
        )

    if not report["sections"]["projects"]:
        priorities.append(
            "Add 2–3 technical projects."
        )

    return priorities[:3]



def build_resume_report(resume_text: str) -> dict:
    """
    Builds the complete Resume Report.
    """

    analysis = analyze_resume_quality(resume_text)

    scores = compute_resume_quality_score(analysis)

    ats_diagnostics = build_ats_diagnostics(analysis)

    return {
        **scores,
        "resume_quality_score": scores["overall_score"],
        "ats_score": ats_diagnostics["score"],
        "analysis": analysis,
        "ats_diagnostics": ats_diagnostics,
        "strengths": generate_resume_strengths(analysis),
        "recommendations": generate_resume_recommendations(analysis),
        "priority_improvements": generate_priority_improvements(analysis)
    }






