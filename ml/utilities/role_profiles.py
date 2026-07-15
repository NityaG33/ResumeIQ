"""
Role Profiles

Defines the representative skill set for each supported role.
Used for role alignment and recommendations.
"""

ROLE_PROFILES = {

    "backend": {
        "name": "Backend Developer",
        "expected_skills": 8,
        "skills": {
            "python",
            "java",
            "sql",
            "postgresql",
            "mysql",
            "backend",
            "fastapi",
            "django",
            "flask",
            "nodejs",
            "express",
            "rest api",
            "docker",
            "git",
            "github",
            "aws",
            "mongodb",
            "redis",
        }
    },

    "frontend": {
        "name": "Frontend Developer",
        "expected_skills": 8,
        "skills": {
            "html",
            "css",
            "javascript",
            "typescript",
            "react",
            "nextjs",
            "redux",
            "tailwind",
            "git",
            "github",
        }
    },

    "software_engineer": {
        "name": "Software Engineer",
        "expected_skills": 10,
        "skills": {
            "python",
            "java",
            "c++",
            "sql",
            "data structures",
            "algorithms",
            "oop",
            "dbms",
            "operating systems",
            "computer networks",
            "git",
            "github",
            "docker",
            "rest api",
        }
    },

    "ml_engineer": {
        "name": "Machine Learning Engineer",
        "expected_skills": 8,
        "skills": {
            "python",
            "machine learning",
            "numpy",
            "pandas",
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "opencv",
            "huggingface",
            "transformers",
            "matplotlib",
            "docker",
            "git",
            "github",
        }
    }
}


def get_role_profile(role: str):
    """
    Returns the skill profile for the given role.
    Defaults to software_engineer if the role is invalid.
    """
    return ROLE_PROFILES.get(
        role.lower(),
        ROLE_PROFILES["software_engineer"]
    )