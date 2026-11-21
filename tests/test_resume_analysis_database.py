
import uuid
import pytest

from database.connection import (
    resumes_collection,
    analyses_collection
)

from services.resume_service import (
    create_resume,
    get_user_resumes,
    get_user_resume,
    delete_user_resume
)

from services.analysis_service import (
    create_analysis,
    get_user_analyses,
    get_user_analysis,
    delete_user_analysis
)


@pytest.fixture
def test_user_id():
    user_id = f"test-user-{uuid.uuid4().hex}"

    yield user_id

    # Clean up all records created for this test user
    analyses_collection.delete_many({"user_id": user_id})
    resumes_collection.delete_many({"user_id": user_id})


# 1. Create and retrieve a resume
def test_create_and_get_resume(test_user_id):
    resume = create_resume(
        user_id=test_user_id,
        filename="resume.pdf",
        file_reference="resume.pdf"
    )

    assert resume["_id"] is not None
    assert resume["filename"] == "resume.pdf"

    retrieved = get_user_resume(
        test_user_id,
        str(resume["_id"])
    )

    assert retrieved is not None
    assert retrieved["filename"] == "resume.pdf"


# 2. Retrieve only resumes belonging to a user
def test_get_user_resumes(test_user_id):
    create_resume(
        test_user_id,
        "resume1.pdf",
        "resume1.pdf"
    )

    create_resume(
        test_user_id,
        "resume2.pdf",
        "resume2.pdf"
    )

    create_resume(
        "another-user",
        "other.pdf",
        "other.pdf"
    )

    resumes = get_user_resumes(test_user_id)

    assert len(resumes) == 2
    assert {r["filename"] for r in resumes} == {
        "resume1.pdf",
        "resume2.pdf"
    }


# 3. Reject invalid or another user's resume
def test_get_user_resume_access_control(test_user_id):
    resume = create_resume(
        test_user_id,
        "resume.pdf",
        "resume.pdf"
    )

    resume_id = str(resume["_id"])

    assert get_user_resume(
        "another-user",
        resume_id
    ) is None

    assert get_user_resume(
        test_user_id,
        "invalid-id"
    ) is None


# 4. Delete a resume
def test_delete_user_resume(test_user_id):
    resume = create_resume(
        test_user_id,
        "resume.pdf",
        "resume.pdf"
    )

    resume_id = str(resume["_id"])

    assert delete_user_resume(
        test_user_id,
        resume_id
    ) is True

    assert get_user_resume(
        test_user_id,
        resume_id
    ) is None

    assert delete_user_resume(
        test_user_id,
        resume_id
    ) is False


# 5. Create and retrieve an analysis
def test_create_and_get_analysis(test_user_id):
    analysis = create_analysis(
        user_id=test_user_id,
        analysis_type="jd_match",
        input_type="text",
        result={
            "score": 85.0,
            "confidence": "Strong Match"
        }
    )

    assert analysis["_id"] is not None

    retrieved = get_user_analysis(
        test_user_id,
        str(analysis["_id"])
    )

    assert retrieved is not None
    assert retrieved["analysis_type"] == "jd_match"
    assert retrieved["result"]["score"] == 85.0


# 6. Retrieve user analyses and associated resume filename
def test_get_user_analyses(test_user_id):
    resume = create_resume(
        test_user_id,
        "my_resume.pdf",
        "my_resume.pdf"
    )

    create_analysis(
        user_id=test_user_id,
        analysis_type="jd_match",
        input_type="pdf",
        result={"score": 90.0},
        resume_id=str(resume["_id"])
    )

    create_analysis(
        user_id=test_user_id,
        analysis_type="resume_quality",
        input_type="text",
        result={"score": 80.0}
    )

    create_analysis(
        user_id="another-user",
        analysis_type="jd_match",
        input_type="text",
        result={"score": 50.0}
    )

    analyses = get_user_analyses(test_user_id)

    assert len(analyses) == 2

    pdf_analysis = next(
        a for a in analyses
        if a["input_type"] == "pdf"
    )

    assert pdf_analysis["resume_filename"] == "my_resume.pdf"


# 7. Prevent access to another user's analysis
def test_get_user_analysis_access_control(test_user_id):
    analysis = create_analysis(
        user_id=test_user_id,
        analysis_type="jd_match",
        input_type="text",
        result={"score": 85.0}
    )

    analysis_id = str(analysis["_id"])

    assert get_user_analysis(
        "another-user",
        analysis_id
    ) is None

    assert get_user_analysis(
        test_user_id,
        "invalid-id"
    ) is None


# 8. Delete an analysis
def test_delete_user_analysis(test_user_id):
    analysis = create_analysis(
        user_id=test_user_id,
        analysis_type="jd_match",
        input_type="text",
        result={"score": 85.0}
    )

    analysis_id = str(analysis["_id"])

    assert delete_user_analysis(
        test_user_id,
        analysis_id
    ) is True

    assert get_user_analysis(
        test_user_id,
        analysis_id
    ) is None

    assert delete_user_analysis(
        test_user_id,
        analysis_id
    ) is False
