from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .text_processing import clean_and_normalize
from .skill_extraction import categorize_skills, extract_skills

def text_similarity(resume_text: str, jd_text: str) -> float:
    documents = [
        clean_and_normalize(resume_text),
        clean_and_normalize(jd_text)
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return score[0][0]


def skill_similarity(resume_text: str, jd_text: str, role: str) -> float:
    skill_analysis = categorize_skills(
        resume_text,
        jd_text,
        role
    )

    matched = skill_analysis["matched"]

    jd_skills = extract_skills(jd_text)

    if not jd_skills:
        return 0.0

    return len(matched) / len(jd_skills)
