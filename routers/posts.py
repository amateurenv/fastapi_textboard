import aiosqlite
from fastapi import APIRouter, Depends

from auth import verify_admin
from database import get_db
from schemas import PostCreate
from services import posts as post_service

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/{thread_id}")
async def get_posts(thread_id: int, db: aiosqlite.Connection = Depends(get_db)):
    return await post_service.get_by_thread(db, thread_id)

@router.post("/{thread_id}")
async def create_post(thread_id: int, post: PostCreate, db: aiosqlite.Connection = Depends(get_db)):
    return await post_service.create(db, thread_id, post)

@router.delete("/{post_id}")
async def delete_post(post_id: int, db: aiosqlite.Connection = Depends(get_db), admin: str = Depends(verify_admin)):
    return await post_service.delete(db, post_id)