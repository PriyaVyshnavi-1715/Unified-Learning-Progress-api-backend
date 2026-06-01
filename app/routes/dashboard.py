from fastapi import APIRouter, Depends
from app.database import db
from app.utils.object_id import serialize_documents
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


async def _records(collection: str, user_id: str) -> list[dict]:
    return serialize_documents(await db[collection].find({"user_id": user_id}).to_list(length=500))


@router.get("/summary")
async def dashboard_summary(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    skills = await _records("skills", user_id)
    assignments = await _records("assignments", user_id)
    coding_stats = await _records("coding_stats", user_id)
    lms_progress = await _records("lms_progress", user_id)

    completed_skills = len([skill for skill in skills if skill.get("status") == "completed"])
    weak_areas = [skill for skill in skills if skill.get("weak_area") or skill.get("proficiency", 0) < 50]
    pending_assignments = len([item for item in assignments if item.get("status") != "submitted"])
    total_problems = sum(item.get("problems_solved", 0) for item in coding_stats)

    skill_completion = round((completed_skills / len(skills)) * 100, 2) if skills else 0
    lms_completion = round(sum(item.get("completion_percentage", 0) for item in lms_progress) / len(lms_progress), 2) if lms_progress else 0
    overall_completion = round((skill_completion + lms_completion) / 2, 2) if skills or lms_progress else 0

    return {
        "total_skills": len(skills),
        "completed_skills": completed_skills,
        "weak_areas": len(weak_areas),
        "pending_assignments": pending_assignments,
        "coding_profiles": len(coding_stats),
        "total_problems_solved": total_problems,
        "skill_completion_percentage": skill_completion,
        "lms_completion_percentage": lms_completion,
        "overall_completion_percentage": overall_completion,
    }


@router.get("/skills")
async def skill_dashboard(current_user: dict = Depends(get_current_user)):
    skills = await _records("skills", current_user["id"])
    return {"skills": skills}


@router.get("/weak-areas")
async def weak_areas(current_user: dict = Depends(get_current_user)):
    skills = await _records("skills", current_user["id"])
    coding_stats = await _records("coding_stats", current_user["id"])
    weak_skills = [skill for skill in skills if skill.get("weak_area") or skill.get("proficiency", 0) < 50]
    weak_topics = [item.get("weakest_topic") for item in coding_stats if item.get("weakest_topic")]
    return {"skills": weak_skills, "coding_topics": weak_topics}


@router.get("/completion")
async def completion(current_user: dict = Depends(get_current_user)):
    summary = await dashboard_summary(current_user)
    return {
        "overall": summary["overall_completion_percentage"],
        "skills": summary["skill_completion_percentage"],
        "lms": summary["lms_completion_percentage"],
    }
