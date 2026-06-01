from bson import ObjectId
from fastapi import HTTPException, status


def to_object_id(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid record id")
    return ObjectId(value)


def serialize_document(document: dict | None) -> dict | None:
    if not document:
        return None
    document["id"] = str(document.pop("_id"))
    return document


def serialize_documents(documents: list[dict]) -> list[dict]:
    return [serialize_document(document) for document in documents]
