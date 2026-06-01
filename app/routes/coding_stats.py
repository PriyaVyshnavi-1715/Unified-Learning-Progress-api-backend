from fastapi import APIRouter, Depends
from app.schemas.learning import CodingStatsCreate, CodingStatsUpdate
from app.services.crud import create_record, delete_record, get_record, list_records, update_record
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/coding-stats", tags=["Coding Stats"])
COLLECTION = "coding_stats"


@router.post("")
async def create_stats(payload: CodingStatsCreate, current_user: dict = Depends(get_current_user)):
    return await create_record(COLLECTION, current_user["id"], payload.model_dump())


@router.get("")
async def get_stats(current_user: dict = Depends(get_current_user)):
    return await list_records(COLLECTION, current_user["id"])


@router.get("/{stat_id}")
async def get_stat(stat_id: str, current_user: dict = Depends(get_current_user)):
    return await get_record(COLLECTION, current_user["id"], stat_id)


@router.put("/{stat_id}")
async def update_stats(stat_id: str, payload: CodingStatsUpdate, current_user: dict = Depends(get_current_user)):
    return await update_record(COLLECTION, current_user["id"], stat_id, payload.model_dump())


@router.delete("/{stat_id}")
async def delete_stats(stat_id: str, current_user: dict = Depends(get_current_user)):
    return await delete_record(COLLECTION, current_user["id"], stat_id)
