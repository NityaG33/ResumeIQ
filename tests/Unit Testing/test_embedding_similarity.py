
import numpy as np
import pytest

from ml.embeddings import embedding_similarity as embedding_module


class FakeModel:

    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.received_texts = None
        self.received_kwargs = None

    def encode(self, texts, **kwargs):
        self.received_texts = texts
        self.received_kwargs = kwargs

        return np.array(self.embeddings)


def setup_fake_model(monkeypatch, embeddings):
    model = FakeModel(embeddings)

    monkeypatch.setattr(
        embedding_module,
        "get_model",
        lambda: model
    )

    return model


def test_identical_embeddings(monkeypatch):
    model = setup_fake_model(
        monkeypatch,
        [[1.0, 0.0], [1.0, 0.0]]
    )

    score = embedding_module.embedding_similarity(
        "Python developer",
        "Python developer"
    )

    assert score == pytest.approx(1.0)


def test_orthogonal_embeddings(monkeypatch):
    setup_fake_model(
        monkeypatch,
        [[1.0, 0.0], [0.0, 1.0]]
    )

    score = embedding_module.embedding_similarity(
        "Python developer",
        "Cooking recipes"
    )

    assert score == pytest.approx(0.0)


def test_opposite_embeddings(monkeypatch):
    setup_fake_model(
        monkeypatch,
        [[1.0, 0.0], [-1.0, 0.0]]
    )

    score = embedding_module.embedding_similarity(
        "Text A",
        "Text B"
    )

    assert score == pytest.approx(-1.0)


def test_model_receives_both_texts(monkeypatch):
    model = setup_fake_model(
        monkeypatch,
        [[1.0, 0.0], [1.0, 0.0]]
    )

    embedding_module.embedding_similarity(
        "Resume text",
        "Job description"
    )

    assert model.received_texts == [
        "Resume text",
        "Job description"
    ]

    assert model.received_kwargs == {
        "convert_to_numpy": True,
        "show_progress_bar": False
    }
