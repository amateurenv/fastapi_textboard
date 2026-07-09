import aiosqlite
from fastapi import APIRouter, Depends

from auth import verify_admin
from database import get_db

router = APIRouter(prefix="/threads", tags=["Threads"])


@router.get("/{board_url}")
async def get_threads(board_url: str, db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute("SELECT * FROM threads WHERE board_url = ?", (board_url,)) as cursor:
        return [dict(row) for row in await cursor.fetchall()]


@router.post("/{board_url}")
async def create_thread(board_url: str, title: str, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("INSERT INTO threads (board_url, title) VALUES (?, ?)", (board_url, title))
    await db.commit()
    return {"message": "Тред создан"}


@router.delete("/{thread_id}")
async def delete_thread(thread_id: int, db: aiosqlite.Connection = Depends(get_db), admin: str = Depends(verify_admin)):
    await db.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
    await db.commit()
    return {"message": "Тред удален"}
