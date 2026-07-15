from ml.utilities.recommendation_data import ROLE_RECOMMENDATIONS


"""
Recommendation Engine

Generates role-specific recommendations
based on missing skills.
"""


def generate_recommendations(
    skill_analysis: dict,
    role: str,
) -> list:

    recommendations = set()

    role_data = ROLE_RECOMMENDATIONS.get(
        role.lower(),
        {}
    )

    # Missing Skills

    for skill in skill_analysis["missing"]:

        if skill in role_data:

            recommendations.add(
                role_data[skill]
            )

        else:

            recommendations.add(
                f"Consider adding '{skill}' through projects, internships, certifications or practical experience."
            )

    # General Resume Advice

    recommendations.update({

        "Quantify achievements using measurable metrics (e.g., reduced response time by 30%).",

        "Tailor your Skills section according to the target job role.",

        "Include GitHub and LinkedIn links showcasing your best technical work.",

        "Write project descriptions focusing on impact, technologies used and measurable outcomes."
    })

    return sorted(recommendations)