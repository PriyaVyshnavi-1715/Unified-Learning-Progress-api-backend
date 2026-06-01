from fastapi import APIRouter, Depends
from app.schemas.learning import SkillCreate, SkillUpdate
from app.services.crud import create_record, delete_record, get_record, list_records, update_record
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/skills", tags=["Skills"])
COLLECTION = "skills"


@router.post("")
async def create_skill(payload: SkillCreate, current_user: dict = Depends(get_current_user)):
    return await create_record(COLLECTION, current_user["id"], payload.model_dump())


@router.get("")
async def get_skills(current_user: dict = Depends(get_current_user)):
    return await list_records(COLLECTION, current_user["id"])


@router.get("/{skill_id}")
async def get_skill(skill_id: str, current_user: dict = Depends(get_current_user)):
    return await get_record(COLLECTION, current_user["id"], skill_id)


@router.put("/{skill_id}")
async def update_skill(skill_id: str, payload: SkillUpdate, current_user: dict = Depends(get_current_user)):
    return await update_record(COLLECTION, current_user["id"], skill_id, payload.model_dump())


@router.delete("/{skill_id}")
async def delete_skill(skill_id: str, current_user: dict = Depends(get_current_user)):
    return await delete_record(COLLECTION, current_user["id"], skill_id)
