from fastapi import APIRouter, Depends
from app.database import db
from app.schemas.learning import StudentUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("/me")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@router.put("/me")
async def update_profile(payload: StudentUpdate, current_user: dict = Depends(get_current_user)):
    updates = {key: value for key, value in payload.model_dump().items() if value is not None}
    if updates:
        await db.users.update_one({"email": current_user["email"]}, {"$set": updates})
        current_user.update(updates)
    return current_user
