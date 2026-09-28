from datetime import datetime, timezone
from database.connection import resumes_collection

def create_resume(
        user_id: str,
        filename: str,
        file_reference: str,
):
    resume = {
        "user_id": user_id,
        "filename": filename,
        "file_reference": file_reference,
        "created_at": datetime.now(timezone.utc),
    }

    result = resumes_collection.insert_one(resume)
    resume["_id"] = result.inserted_id
    return resume


def get_user_resumes(user_id: str):
    return list(
        resumes_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1)
    )


def get_user_resume(
    user_id: str,
    resume_id: str
):
    from bson import ObjectId

    try:
        object_id = ObjectId(resume_id)
    except Exception:
        return None

    return resumes_collection.find_one({
        "_id": object_id,
        "user_id": user_id,
    })


def delete_user_resume(
    user_id: str,
    resume_id: str
):
    from bson import ObjectId

    try:
        object_id = ObjectId(resume_id)
    except Exception:
        return False

    result = resumes_collection.delete_one({
        "_id": object_id,
        "user_id": user_id,
    })

    return result.deleted_count == 1