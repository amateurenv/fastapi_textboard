import aiosqlite
from fastapi import HTTPException
from schemas import BoardCreate
from services.utils import check_deleted_or_404

async def get_all(db: aiosqlite.Connection):
    async with db.execute("SELECT * FROM boards") as cursor:
        return [dict(row) for row in await cursor.fetchall()]

async def create(db: aiosqlite.Connection, board: BoardCreate):
    try:
        await db.execute("INSERT INTO boards (url, name) VALUES (?, ?)", (board.url, board.name))
        await db.commit()
        return {"message": f"Доска /{board.url}/ успешно создана"}
    except aiosqlite.IntegrityError:
        raise HTTPException(status_code=400, detail="Доска с таким URL уже существует")

async def delete(db: aiosqlite.Connection, url: str):
    cursor = await db.execute("DELETE FROM boards WHERE url = ?", (url,))
    await db.commit()
    await check_deleted_or_404(cursor, "Доска не найдена")
    return {"message": "Доска удалена"}