from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once (important)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embedding_similarity(resume_text: str, jd_text: str) -> float:
    embeddings = model.encode([resume_text, jd_text])
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )
    return float(similarity[0][0])
