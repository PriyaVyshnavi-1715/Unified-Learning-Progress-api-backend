from fastapi import APIRouter, Depends
from app.schemas.learning import AssignmentCreate, AssignmentUpdate
from app.services.crud import create_record, delete_record, get_record, list_records, update_record
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])
COLLECTION = "assignments"


@router.post("")
async def create_assignment(payload: AssignmentCreate, current_user: dict = Depends(get_current_user)):
    return await create_record(COLLECTION, current_user["id"], payload.model_dump())


@router.get("")
async def get_assignments(current_user: dict = Depends(get_current_user)):
    return await list_records(COLLECTION, current_user["id"])


@router.get("/{assignment_id}")
async def get_assignment(assignment_id: str, current_user: dict = Depends(get_current_user)):
    return await get_record(COLLECTION, current_user["id"], assignment_id)


@router.put("/{assignment_id}")
async def update_assignment(assignment_id: str, payload: AssignmentUpdate, current_user: dict = Depends(get_current_user)):
    return await update_record(COLLECTION, current_user["id"], assignment_id, payload.model_dump())


@router.delete("/{assignment_id}")
async def delete_assignment(assignment_id: str, current_user: dict = Depends(get_current_user)):
    return await delete_record(COLLECTION, current_user["id"], assignment_id)
