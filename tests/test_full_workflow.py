
import uuid
import pytest
from fastapi.testclient import TestClient

from api import app
from database.connection import users_collection, analyses_collection


@pytest.fixture
def workflow_client():
    email = f"workflow_{uuid.uuid4().hex}@example.com"

    with TestClient(app) as client:
        yield client, email

    # Clean up test data
    user = users_collection.find_one({"email": email})

    if user:
        user_id = str(user["_id"])

        analyses_collection.delete_many({"user_id": user_id})
        users_collection.delete_one({"_id": user["_id"]})


# 1. Complete registration, login, analysis and retrieval workflow
def test_complete_user_analysis_workflow(
    workflow_client,
    monkeypatch
):
    client, email = workflow_client

    # Register a real user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    # Log in using real password verification and JWT creation
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "password123"
        }
    )

    assert login_response.status_code == 200
    assert client.cookies.get("access_token") is not None

    # Verify authenticated user
    me_response = client.get("/api/v1/auth/me")

    assert me_response.status_code == 200
    assert me_response.json()["email"] == email

    # Mock only the ML matching pipeline
    mock_result = {
        "jd_match": {
            "score": 85.0,
            "confidence": "Strong Match",
            "component_scores": {
                "skill_coverage": 90.0,
                "embedding_similarity": 80.0,
                "tfidf_similarity": 75.0,
                "role_alignment": 85.0
            },
            "skill_coverage": {
                "matched_skills": ["python", "fastapi"],
                "missing_skills": ["docker"],
                "coverage": 80.0
            },
            "role_alignment": {
                "score": 85.0,
                "matched_skills": ["python", "fastapi"]
            }
        },
        "resume_report": {
            "overall_score": 80.0,
            "grade": "A",
            "summary": "Good resume quality",
            "score_breakdown": {},
            "ats_diagnostics": {},
            "strengths": ["Good technical skills"],
            "recommendations": ["Add quantified achievements"],
            "priority_improvements": ["Improve project descriptions"]
        },
        "recommendations": {
            "resume": ["Add quantified achievements"],
            "job_match": ["Learn Docker"]
        },
        "explanation": ["Strong technical skill alignment"]
    }

    monkeypatch.setattr(
        "routes.analysis_routes.run_match",
        lambda resume_text, jd_text, role: mock_result
    )

    # Submit matching request
    match_response = client.post(
        "/api/v1/match",
        json={
            "role": "backend",
            "resume_text": "Python FastAPI MongoDB developer",
            "jd_text": "Looking for a Python backend developer"
        }
    )

    assert match_response.status_code == 200
    assert match_response.json()["jd_match"]["score"] == 85.0

    # Retrieve actual saved analysis from MongoDB through API
    history_response = client.get("/api/v1/analyses")

    assert history_response.status_code == 200
    assert len(history_response.json()) == 1

    analysis = history_response.json()[0]

    assert analysis["analysis_type"] == "jd_match"
    assert analysis["input_type"] == "text"
    assert analysis["result"]["jd_match"]["score"] == 85.0

    # Retrieve the individual analysis
    detail_response = client.get(
        f"/api/v1/analyses/{analysis['id']}"
    )

    assert detail_response.status_code == 200
    assert detail_response.json()["id"] == analysis["id"]

    # Log out
    logout_response = client.post("/api/v1/auth/logout")

    assert logout_response.status_code == 200

    # Protected route should reject the logged-out client
    protected_response = client.get("/api/v1/auth/me")

    assert protected_response.status_code == 401
    

