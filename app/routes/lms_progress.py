from fastapi import APIRouter, Depends
from app.schemas.learning import LMSProgressCreate, LMSProgressUpdate
from app.services.crud import create_record, delete_record, get_record, list_records, update_record
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/lms-progress", tags=["LMS Progress"])
COLLECTION = "lms_progress"


@router.post("")
async def create_progress(payload: LMSProgressCreate, current_user: dict = Depends(get_current_user)):
    data = payload.model_dump()
    data["completion_percentage"] = round((data["completed_modules"] / data["total_modules"]) * 100, 2)
    return await create_record(COLLECTION, current_user["id"], data)


@router.get("")
async def get_progress(current_user: dict = Depends(get_current_user)):
    return await list_records(COLLECTION, current_user["id"])


@router.get("/{progress_id}")
async def get_progress_item(progress_id: str, current_user: dict = Depends(get_current_user)):
    return await get_record(COLLECTION, current_user["id"], progress_id)


@router.put("/{progress_id}")
async def update_progress(progress_id: str, payload: LMSProgressUpdate, current_user: dict = Depends(get_current_user)):
    data = payload.model_dump()
    existing = await get_record(COLLECTION, current_user["id"], progress_id)
    completed = data.get("completed_modules") if data.get("completed_modules") is not None else existing["completed_modules"]
    total = data.get("total_modules") if data.get("total_modules") is not None else existing["total_modules"]
    data["completion_percentage"] = round((completed / total) * 100, 2)
    return await update_record(COLLECTION, current_user["id"], progress_id, data)


@router.delete("/{progress_id}")
async def delete_progress(progress_id: str, current_user: dict = Depends(get_current_user)):
    return await delete_record(COLLECTION, current_user["id"], progress_id)
