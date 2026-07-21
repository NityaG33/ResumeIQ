from ml.skill_extraction import extract_skills

jd = """
Backend Developer

Requirements:
Python
FastAPI
Docker
Git
PostgreSQL
REST APIs
Experience building scalable backend applications.
"""

print(extract_skills(jd))