from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.database import db
from app.utils.object_id import serialize_document, serialize_documents, to_object_id


async def create_record(collection_name: str, user_id: str, payload: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    payload.update({"user_id": user_id, "created_at": now, "updated_at": now})
    result = await db[collection_name].insert_one(payload)
    document = await db[collection_name].find_one({"_id": result.inserted_id})
    return serialize_document(document)


async def list_records(collection_name: str, user_id: str) -> list[dict]:
    cursor = db[collection_name].find({"user_id": user_id}).sort("created_at", -1)
    return serialize_documents(await cursor.to_list(length=200))


async def get_record(collection_name: str, user_id: str, record_id: str) -> dict:
    document = await db[collection_name].find_one({"_id": to_object_id(record_id), "user_id": user_id})
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return serialize_document(document)


async def update_record(collection_name: str, user_id: str, record_id: str, payload: dict) -> dict:
    updates = {key: value for key, value in payload.items() if value is not None}
    if not updates:
        return await get_record(collection_name, user_id, record_id)
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db[collection_name].update_one(
        {"_id": to_object_id(record_id), "user_id": user_id},
        {"$set": updates},
    )
    return await get_record(collection_name, user_id, record_id)


async def delete_record(collection_name: str, user_id: str, record_id: str) -> dict:
    result = await db[collection_name].delete_one({"_id": to_object_id(record_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return {"message": "Record deleted successfully"}
