
from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load the embedding model once, on first use."""
    return SentenceTransformer("all-MiniLM-L6-v2")


def embedding_similarity(
    resume_text: str,
    jd_text: str,
) -> float:
    model = get_model()

    embeddings = model.encode(
        [resume_text, jd_text],
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    similarity = cosine_similarity(
        embeddings[0].reshape(1, -1),
        embeddings[1].reshape(1, -1),
    )

    return float(similarity[0][0])
