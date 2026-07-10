import aiosqlite
from fastapi import HTTPException
from schemas import ThreadCreate
from services.utils import add_display_numbers, check_deleted_or_404


async def get_by_board(db: aiosqlite.Connection, board_url: str):
    query = """
            SELECT threads.* \
            FROM threads \
                     JOIN boards ON threads.board_id = boards.id
            WHERE boards.url = ? \
            """
    async with db.execute(query, (board_url,)) as cursor:
        rows = await cursor.fetchall()

    return add_display_numbers(rows, start=1)


async def create(db: aiosqlite.Connection, board_url: str, thread: ThreadCreate):
    cursor = await db.execute("SELECT id FROM boards WHERE url = ?", (board_url,))
    board_record = await cursor.fetchone()

    if not board_record:
        raise HTTPException(status_code=404, detail="Доска не найдена")

    await db.execute("INSERT INTO threads (board_id, title) VALUES (?, ?)", (board_record["id"], thread.title))
    await db.commit()
    return {"message": "Тред успешно создан"}


async def delete(db: aiosqlite.Connection, thread_id: int):
    cursor = await db.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
    await db.commit()
    await check_deleted_or_404(cursor, "Тред не найден")
    return {"message": "Тред удален"}