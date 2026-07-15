"""
Skill Alias Mapping

Maps different spellings and variations of the same
technology to one canonical representation.
"""

SKILL_ALIASES = {

    # ------------------------------
    # Programming Languages
    # ------------------------------

    "python": [
        "python"
    ],

    "java": [
        "java"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "javascript": [
        "javascript",
        "js"
    ],

    "typescript": [
        "typescript",
        "ts"
    ],

    # ------------------------------
    # Frontend
    # ------------------------------

    "react": [
        "react",
        "reactjs",
        "react.js"
    ],

    "nextjs": [
        "nextjs",
        "next.js"
    ],

    "tailwind": [
        "tailwind",
        "tailwindcss",
        "tailwind css"
    ],

    # ------------------------------
    # Backend
    # ------------------------------

    "nodejs": [
        "nodejs",
        "node.js",
        "node js"
    ],

    "express": [
        "express",
        "expressjs",
        "express.js"
    ],

    "fastapi": [
        "fastapi",
        "fast api"
    ],

    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest service",
        "rest services"
    ],

    # ------------------------------
    # Databases
    # ------------------------------

    "sql": [
        "sql"
    ],

    "postgresql": [
        "postgresql",
        "postgres"
    ],

    "mysql": [
        "mysql"
    ],

    "sqlite": [
        "sqlite"
    ],

    "mongodb": [
        "mongodb",
        "mongo db"
    ],

    # ------------------------------
    # DevOps
    # ------------------------------

    "docker": [
        "docker",
        "dockerized",
        "containerized"
    ],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "git": [
        "git"
    ],

    "github": [
        "github"
    ],

    "ci/cd": [
        "ci/cd",
        "ci cd",
        "continuous integration",
        "continuous deployment"
    ],

    # ------------------------------
    # Cloud
    # ------------------------------

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure"
    ],

    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform"
    ],

    # ------------------------------
    # Core CS
    # ------------------------------

    "data structures": [
        "data structures",
        "dsa"
    ],

    "algorithms": [
        "algorithms",
        "algorithm"
    ],

    "oop": [
        "oop",
        "oops",
        "object oriented programming",
        "object-oriented programming"
    ],

    "dbms": [
        "dbms",
        "database management system"
    ],

    "operating systems": [
        "operating systems",
        "operating system",
        "os"
    ],

    "computer networks": [
        "computer networks",
        "computer networking"
    ],

    # ------------------------------
    # Machine Learning
    # ------------------------------

    "machine learning": [
        "machine learning",
        "ml",
        "ai",
        "ai/ml"
    ],

    "scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    "tensorflow": [
        "tensorflow",
        "tensor flow"
    ],

    "pytorch": [
        "pytorch",
        "py torch"
    ],

    "huggingface": [
        "huggingface",
        "hugging face"
    ]
}

CANONICAL_SKILLS = set(SKILL_ALIASES.keys())