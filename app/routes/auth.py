from fastapi import APIRouter, HTTPException, status
from app.database import db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.utils.object_id import serialize_document
from app.utils.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    existing_user = await db.users.find_one({"email": payload.email.lower()})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = payload.model_dump(exclude={"password"})
    user["email"] = payload.email.lower()
    user["password_hash"] = hash_password(payload.password)
    result = await db.users.insert_one(user)
    created_user = serialize_document(await db.users.find_one({"_id": result.inserted_id}))
    created_user.pop("password_hash", None)
    return {"access_token": create_access_token(created_user["email"]), "user": created_user}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await db.users.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    user = serialize_document(user)
    user.pop("password_hash", None)
    return {"access_token": create_access_token(user["email"]), "user": user}
