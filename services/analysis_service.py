from datetime import datetime, timezone
from bson import ObjectId
from database.connection import (
    analyses_collection,
    resumes_collection,
)


def create_analysis(
    user_id: str,
    analysis_type: str,
    input_type: str,
    result: dict,
    resume_id: str | None = None
):
    analysis = {
        "user_id": user_id,
        "resume_id": resume_id,
        "analysis_type": analysis_type,
        "input_type": input_type,
        "result": result,
        "created_at": datetime.now(timezone.utc),
        "model_version": "1.0"
    }

    db_result = analyses_collection.insert_one(analysis)

    analysis["_id"] = db_result.inserted_id

    return analysis


def get_user_analyses(user_id: str):
    analyses = list(
        analyses_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1)
    )

    for analysis in analyses:
        analysis["resume_filename"] = None

        if analysis.get("resume_id"):
            resume = resumes_collection.find_one({
                "_id": ObjectId(analysis["resume_id"]),
                "user_id": user_id,
            })

            if resume:
                analysis["resume_filename"] = resume.get("filename")

    return analyses


def get_user_analysis(user_id: str, analysis_id: str):
    try:
        object_id = ObjectId(analysis_id)
    except Exception:
        return None

    analysis = analyses_collection.find_one({
        "_id": object_id,
        "user_id": user_id,
    })

    if not analysis:
        return None

    analysis["resume_filename"] = None

    if analysis.get("resume_id"):
        resume = resumes_collection.find_one({
            "_id": ObjectId(analysis["resume_id"]),
            "user_id": user_id,
        })

        if resume:
            analysis["resume_filename"] = resume.get("filename")

    return analysis


def delete_user_analysis(
    user_id: str,
    analysis_id: str
):
    from bson import ObjectId

    try:
        object_id = ObjectId(analysis_id)
    except Exception:
        return False

    result = analyses_collection.delete_one({
        "_id": object_id,
        "user_id": user_id,
    })

    return result.deleted_count == 1