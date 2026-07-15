"""
Master Skill Taxonomy

This file contains all canonical skills recognised by the Resume-JD Matcher.
Skills are grouped by domain to improve maintainability and readability.
"""


# Programming Languages

PROGRAMMING_LANGUAGES = {
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
}


# Frontend

FRONTEND_SKILLS = {
    "html",
    "css",
    "react",
    "nextjs",
    "redux",
    "tailwind",
}


# Backend

BACKEND_SKILLS = {
    "backend",
    "fastapi",
    "flask",
    "django",
    "nodejs",
    "express",
    "rest api",
    "graphql",
}


# Databases

DATABASE_SKILLS = {
    "sql",
    "mongodb",
    "mysql",
    "postgresql",
    "sqlite",
    "redis",
}


# DevOps

DEVOPS_SKILLS = {
    "docker",
    "kubernetes",
    "git",
    "github",
    "ci/cd",
}


# Cloud

CLOUD_SKILLS = {
    "aws",
    "azure",
    "gcp",
    "cloud",
}


# Core Computer Science

CORE_CS_SKILLS = {
    "data structures",
    "algorithms",
    "oop",
    "dbms",
    "operating systems",
    "computer networks",
    "system design",
}


# Machine Learning

ML_SKILLS = {
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
}


# Master Skill Set

SKILL_CATEGORIES = {
    "programming_languages": PROGRAMMING_LANGUAGES,
    "frontend": FRONTEND_SKILLS,
    "backend": BACKEND_SKILLS,
    "database": DATABASE_SKILLS,
    "devops": DEVOPS_SKILLS,
    "cloud": CLOUD_SKILLS,
    "core_cs": CORE_CS_SKILLS,
    "ml": ML_SKILLS,
}

SKILLS = set().union(*SKILL_CATEGORIES.values())