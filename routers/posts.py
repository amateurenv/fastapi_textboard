import aiosqlite
from fastapi import APIRouter, Depends

from auth import verify_admin
from database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/{thread_id}")
async def get_posts(thread_id: int, db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute("SELECT * FROM posts WHERE thread_id = ?", (thread_id,)) as cursor:
        return [dict(row) for row in await cursor.fetchall()]


@router.post("/{thread_id}")
async def create_post(thread_id: int, content: str, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("INSERT INTO posts (thread_id, content) VALUES (?, ?)", (thread_id, content))
    await db.commit()
    return {"message": "Пост создан"}


@router.delete("/{post_id}")
async def delete_post(post_id: int, db: aiosqlite.Connection = Depends(get_db), admin: str = Depends(verify_admin)):
    await db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    await db.commit()
    return {"message": "Пост удален"}
