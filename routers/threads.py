import aiosqlite
from fastapi import APIRouter, Depends

from auth import verify_admin
from database import get_db
from schemas import ThreadCreate
from services import threads as thread_service

router = APIRouter(prefix="/threads", tags=["Threads"])

@router.get("/{board_url}")
async def get_threads(board_url: str, db: aiosqlite.Connection = Depends(get_db)):
    return await thread_service.get_by_board(db, board_url)

@router.post("/{board_url}")
async def create_thread(board_url: str, thread: ThreadCreate, db: aiosqlite.Connection = Depends(get_db)):
    return await thread_service.create(db, board_url, thread)

@router.delete("/{thread_id}")
async def delete_thread(thread_id: int, db: aiosqlite.Connection = Depends(get_db), admin: str = Depends(verify_admin)):
    return await thread_service.delete(db, thread_id)