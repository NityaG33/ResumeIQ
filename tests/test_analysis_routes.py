
import pytest
from fastapi.testclient import TestClient

from api import app
from auth.dependencies import get_current_user
from datetime import datetime, timezone


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def authenticated_client():
    def mock_current_user():
        return {
            "_id": "test-user-123",
            "email": "test@example.com"
        }

    app.dependency_overrides[get_current_user] = mock_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Sample response matching your actual MatchResponse schema
def get_mock_match_result():
    return {
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
            "recommendations": ["Add more quantified achievements"],
            "priority_improvements": ["Improve project descriptions"]
        },
        "recommendations": {
            "resume": ["Add more quantified achievements"],
            "job_match": ["Learn Docker"]
        },
        "explanation": ["Strong technical skill alignment"]
    }


# 1. Successful resume matching
def test_match_success(authenticated_client, monkeypatch):
    mock_result = get_mock_match_result()
    saved_data = {}

    monkeypatch.setattr(
        "routes.analysis_routes.run_match",
        lambda resume_text, jd_text, role: mock_result
    )

    def mock_create_analysis(**kwargs):
        saved_data.update(kwargs)

    monkeypatch.setattr(
        "routes.analysis_routes.create_analysis",
        mock_create_analysis
    )

    response = authenticated_client.post(
        "/api/v1/match",
        json={
            "role": "backend",
            "resume_text": "Python FastAPI MongoDB developer",
            "jd_text": "Looking for a Python backend developer"
        }
    )

    assert response.status_code == 200
    assert response.json()["jd_match"]["score"] == 85.0
    assert response.json()["resume_report"]["grade"] == "A"

    assert saved_data["user_id"] == "test-user-123"
    assert saved_data["analysis_type"] == "jd_match"
    assert saved_data["input_type"] == "text"


# 2. Unsupported role
def test_match_invalid_role(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/match",
        json={
            "role": "designer",
            "resume_text": "Python developer",
            "jd_text": "Python backend developer required"
        }
    )

    assert response.status_code == 400
    assert "Unsupported role" in response.json()["detail"]


# 3. Empty resume text
def test_match_empty_resume(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/match",
        json={
            "role": "backend",
            "resume_text": "   ",
            "jd_text": "Python backend developer required"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Resume text cannot be empty."


# 4. Empty job description
def test_match_empty_jd(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/match",
        json={
            "role": "backend",
            "resume_text": "Python backend developer",
            "jd_text": "   "
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Job description cannot be empty."


# 5. Unauthenticated matching request
def test_match_unauthenticated(client):
    response = client.post(
        "/api/v1/match",
        json={
            "role": "backend",
            "resume_text": "Python developer",
            "jd_text": "Python backend developer required"
        }
    )

    assert response.status_code == 401



# 6. Successful PDF resume matching
def test_match_pdf_success(authenticated_client, monkeypatch):
    mock_result = get_mock_match_result()
    saved_resume = {}
    saved_analysis = {}

    monkeypatch.setattr(
        "routes.analysis_routes.extract_resume_text_from_upload",
        lambda file: "Python FastAPI MongoDB developer"
    )

    monkeypatch.setattr(
        "routes.analysis_routes.run_match",
        lambda resume_text, jd_text, role: mock_result
    )

    def mock_create_resume(**kwargs):
        saved_resume.update(kwargs)
        return {"_id": "resume-123"}

    def mock_create_analysis(**kwargs):
        saved_analysis.update(kwargs)

    monkeypatch.setattr(
        "routes.analysis_routes.create_resume",
        mock_create_resume
    )

    monkeypatch.setattr(
        "routes.analysis_routes.create_analysis",
        mock_create_analysis
    )

    response = authenticated_client.post(
        "/api/v1/match-pdf",
        files={
            "resume_file": (
                "resume.pdf",
                b"%PDF-1.4 fake pdf content",
                "application/pdf"
            )
        },
        data={
            "role": "backend",
            "jd_text": "Python backend developer required"
        }
    )

    assert response.status_code == 200
    assert response.json()["jd_match"]["score"] == 85.0

    assert saved_resume["user_id"] == "test-user-123"
    assert saved_resume["filename"] == "resume.pdf"

    assert saved_analysis["analysis_type"] == "jd_match"
    assert saved_analysis["input_type"] == "pdf"
    assert saved_analysis["resume_id"] == "resume-123"


# 7. Reject non-PDF file
def test_match_pdf_invalid_file(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/match-pdf",
        files={
            "resume_file": (
                "resume.txt",
                b"Some text content",
                "text/plain"
            )
        },
        data={
            "role": "backend",
            "jd_text": "Python backend developer required"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF resumes are supported."


# 8. Reject empty job description
def test_match_pdf_empty_jd(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/match-pdf",
        files={
            "resume_file": (
                "resume.pdf",
                b"%PDF-1.4 fake pdf content",
                "application/pdf"
            )
        },
        data={
            "role": "backend",
            "jd_text": "   "
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Job description cannot be empty."


# 9. Reject unauthenticated PDF request
def test_match_pdf_unauthenticated(client):
    response = client.post(
        "/api/v1/match-pdf",
        files={
            "resume_file": (
                "resume.pdf",
                b"%PDF-1.4 fake pdf content",
                "application/pdf"
            )
        },
        data={
            "role": "backend",
            "jd_text": "Python backend developer required"
        }
    )

    assert response.status_code == 401




# 10. Successful resume quality analysis
def test_resume_quality_success(authenticated_client, monkeypatch):
    mock_report = {
        "overall_score": 85.0,
        "grade": "A",
        "summary": "Good resume quality",
        "score_breakdown": {},
        "ats_diagnostics": {},
        "strengths": ["Good technical skills"],
        "recommendations": ["Add quantified achievements"],
        "priority_improvements": ["Improve project descriptions"]
    }

    saved_data = {}

    monkeypatch.setattr(
        "routes.analysis_routes.build_resume_report",
        lambda resume_text: mock_report
    )

    def mock_create_analysis(**kwargs):
        saved_data.update(kwargs)

    monkeypatch.setattr(
        "routes.analysis_routes.create_analysis",
        mock_create_analysis
    )

    response = authenticated_client.post(
        "/api/v1/resume-quality",
        json={
            "resume_text": "Python developer with 3 years of experience"
        }
    )

    assert response.status_code == 200
    assert response.json()["resume_report"]["overall_score"] == 85.0
    assert response.json()["resume_report"]["grade"] == "A"

    assert saved_data["user_id"] == "test-user-123"
    assert saved_data["analysis_type"] == "resume_quality"
    assert saved_data["input_type"] == "text"


# 11. Reject empty resume text
def test_resume_quality_empty_text(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/resume-quality",
        json={
            "resume_text": "   "
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Resume text cannot be empty."


# 12. Reject resume text exceeding maximum length
def test_resume_quality_text_too_long(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/resume-quality",
        json={
            "resume_text": "A" * 50001
        }
    )

    assert response.status_code == 413
    assert response.json()["detail"] == (
        "Resume text must be 50,000 characters or fewer."
    )


# 13. Reject unauthenticated request
def test_resume_quality_unauthenticated(client):
    response = client.post(
        "/api/v1/resume-quality",
        json={
            "resume_text": "Python developer with 3 years of experience"
        }
    )

    assert response.status_code == 401




# 14. Successful PDF resume quality analysis
def test_resume_quality_pdf_success(authenticated_client, monkeypatch):
    mock_report = {
        "overall_score": 85.0,
        "grade": "A",
        "summary": "Good resume quality",
        "score_breakdown": {},
        "ats_diagnostics": {},
        "strengths": ["Good technical skills"],
        "recommendations": ["Add quantified achievements"],
        "priority_improvements": ["Improve project descriptions"]
    }

    saved_resume = {}
    saved_analysis = {}

    monkeypatch.setattr(
        "routes.analysis_routes.extract_resume_text_from_upload",
        lambda file: "Python developer with 3 years of experience"
    )

    monkeypatch.setattr(
        "routes.analysis_routes.build_resume_report",
        lambda resume_text: mock_report
    )

    def mock_create_resume(**kwargs):
        saved_resume.update(kwargs)
        return {"_id": "resume-123"}

    def mock_create_analysis(**kwargs):
        saved_analysis.update(kwargs)

    monkeypatch.setattr(
        "routes.analysis_routes.create_resume",
        mock_create_resume
    )

    monkeypatch.setattr(
        "routes.analysis_routes.create_analysis",
        mock_create_analysis
    )

    response = authenticated_client.post(
        "/api/v1/resume-quality-pdf",
        files={
            "resume_file": (
                "resume.pdf",
                b"%PDF-1.4 fake pdf content",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["resume_report"]["overall_score"] == 85.0

    assert saved_resume["user_id"] == "test-user-123"
    assert saved_resume["filename"] == "resume.pdf"

    assert saved_analysis["analysis_type"] == "resume_quality"
    assert saved_analysis["input_type"] == "pdf"
    assert saved_analysis["resume_id"] == "resume-123"


# 15. Reject non-PDF file
def test_resume_quality_pdf_invalid_file(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/resume-quality-pdf",
        files={
            "resume_file": (
                "resume.txt",
                b"Some text content",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF resumes are supported."


# 16. Reject unauthenticated request
def test_resume_quality_pdf_unauthenticated(client):
    response = client.post(
        "/api/v1/resume-quality-pdf",
        files={
            "resume_file": (
                "resume.pdf",
                b"%PDF-1.4 fake pdf content",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 401





def get_mock_analysis():
    return {
        "_id": "analysis-123",
        "resume_id": None,
        "resume_filename": None,
        "analysis_type": "jd_match",
        "input_type": "text",
        "result": {
            "jd_match": {
                "score": 85.0,
                "confidence": "Strong Match"
            }
        },
        "created_at": datetime.now(timezone.utc),
        "model_version": "1.0"
    }


# 17. Successfully retrieve all analyses
def test_get_analyses_success(authenticated_client, monkeypatch):
    mock_analysis = get_mock_analysis()
    captured = {}

    def mock_get_user_analyses(user_id):
        captured["user_id"] = user_id
        return [mock_analysis.copy()]

    monkeypatch.setattr(
        "routes.analysis_routes.get_user_analyses",
        mock_get_user_analyses
    )

    response = authenticated_client.get("/api/v1/analyses")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == "analysis-123"
    assert response.json()[0]["analysis_type"] == "jd_match"
    assert captured["user_id"] == "test-user-123"


# 18. Retrieve analyses when history is empty
def test_get_analyses_empty(authenticated_client, monkeypatch):
    monkeypatch.setattr(
        "routes.analysis_routes.get_user_analyses",
        lambda user_id: []
    )

    response = authenticated_client.get("/api/v1/analyses")

    assert response.status_code == 200
    assert response.json() == []


# 19. Successfully retrieve one analysis
def test_get_single_analysis_success(authenticated_client, monkeypatch):
    mock_analysis = get_mock_analysis()
    captured = {}

    def mock_get_user_analysis(user_id, analysis_id):
        captured["user_id"] = user_id
        captured["analysis_id"] = analysis_id
        return mock_analysis.copy()

    monkeypatch.setattr(
        "routes.analysis_routes.get_user_analysis",
        mock_get_user_analysis
    )

    response = authenticated_client.get(
        "/api/v1/analyses/analysis-123"
    )

    assert response.status_code == 200
    assert response.json()["id"] == "analysis-123"
    assert response.json()["result"]["jd_match"]["score"] == 85.0

    assert captured["user_id"] == "test-user-123"
    assert captured["analysis_id"] == "analysis-123"


# 20. Analysis not found
def test_get_single_analysis_not_found(authenticated_client, monkeypatch):
    monkeypatch.setattr(
        "routes.analysis_routes.get_user_analysis",
        lambda user_id, analysis_id: None
    )

    response = authenticated_client.get(
        "/api/v1/analyses/nonexistent-id"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Analysis not found"


# 21. Successfully delete an analysis
def test_delete_analysis_success(authenticated_client, monkeypatch):
    captured = {}

    def mock_delete_user_analysis(user_id, analysis_id):
        captured["user_id"] = user_id
        captured["analysis_id"] = analysis_id
        return True

    monkeypatch.setattr(
        "routes.analysis_routes.delete_user_analysis",
        mock_delete_user_analysis
    )

    response = authenticated_client.delete(
        "/api/v1/analyses/analysis-123"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Analysis deleted successfully"

    assert captured["user_id"] == "test-user-123"
    assert captured["analysis_id"] == "analysis-123"


# 22. Delete an analysis that does not exist
def test_delete_analysis_not_found(authenticated_client, monkeypatch):
    monkeypatch.setattr(
        "routes.analysis_routes.delete_user_analysis",
        lambda user_id, analysis_id: False
    )

    response = authenticated_client.delete(
        "/api/v1/analyses/nonexistent-id"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Analysis not found"


# 23. Reject unauthenticated history request
def test_get_analyses_unauthenticated(client):
    response = client.get("/api/v1/analyses")

    assert response.status_code == 401
