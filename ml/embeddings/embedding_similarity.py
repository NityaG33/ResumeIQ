from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def embedding_similarity(
    resume_text: str,
    jd_text: str
) -> float:

    model = get_model()

    embeddings = model.encode(
        [resume_text, jd_text]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )

    return float(similarity[0][0])