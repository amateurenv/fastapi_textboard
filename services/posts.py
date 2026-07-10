import aiosqlite
from fastapi import HTTPException
from schemas import PostCreate
from services.utils import add_display_numbers, check_deleted_or_404


async def get_by_thread(db: aiosqlite.Connection, thread_id: int):
    async with db.execute("SELECT * FROM posts WHERE thread_id = ?", (thread_id,)) as cursor:
        rows = await cursor.fetchall()

    return add_display_numbers(rows, start=2)


async def create(db: aiosqlite.Connection, thread_id: int, post: PostCreate):
    cursor = await db.execute("SELECT id FROM threads WHERE id = ?", (thread_id,))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Тред не найден")

    await db.execute("INSERT INTO posts (thread_id, content) VALUES (?, ?)", (thread_id, post.content))
    await db.commit()
    return {"message": "Ответ добавлен"}


async def delete(db: aiosqlite.Connection, post_id: int):
    cursor = await db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    await db.commit()
    await check_deleted_or_404(cursor, "Пост не найден")
    return {"message": "Пост удален"}