from .scoring import decision_aware_final_score
from .explainability import explainability_engine

if __name__ == "__main__":
    resume = """
    Computer Science undergraduate with strong problem-solving skills.

    Technical Skills:
    • Python, ML, Flask, RESTful APIs, backend, data structures
    • Data analysis using Pandas and NumPy

    Experience:
    • Built a resume screening tool using Python and basic NLP techniques.
    • Developed backend APIs using Flask.
    • Worked with databases like MongoDB for CRUD operations.

    Projects:
    • Resume-JD Matcher – implemented TF-IDF based similarity scoring.
    • Machine Learning mini projects including classification models.

    Tools:
    • Git, Docker (basic)

    """

    jd = """
    We are looking for a Backend Software Engineer Intern.

    Required Skills:
    • Strong proficiency in Python
    • Backend development experience
    • REST API design
    • Basic understanding of data structures
    • Experience with SQL or NoSQL databases

    Preferred Skills:
    • Familiarity with Docker
    • Exposure to cloud platforms (AWS)

    Responsibilities:
    • Build and maintain backend services
    • Work closely with frontend engineers
    • Optimize APIs and database queries

    """

    explanation = explainability_engine(resume, jd)
    result = decision_aware_final_score(resume, jd)

    print("\nExplainability Report:")
    for line in explanation["explanation_text"]:
        print("-", line)

    print("\nFinal Decision-Aware Result:")
    print("Score:", result["final_score"], "%")
    print("Confidence:", result["confidence"])

