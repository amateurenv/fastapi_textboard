import aiosqlite
from fastapi import APIRouter, Depends

from auth import verify_admin
from database import get_db

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.get("/")
async def get_boards(db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute("SELECT * FROM boards") as cursor:
        return [dict(row) for row in await cursor.fetchall()]


@router.post("/")
async def create_board(name: str, url: str, db: aiosqlite.Connection = Depends(get_db),
                       admin: str = Depends(verify_admin)):
    await db.execute("INSERT INTO boards (url, name) VALUES (?, ?)", (url, name))
    await db.commit()
    return {"message": "Доска создана"}


@router.delete("/{url}")
async def delete_board(url: str, db: aiosqlite.Connection = Depends(get_db), admin: str = Depends(verify_admin)):
    await db.execute("DELETE FROM boards WHERE url = ?", (url,))
    await db.commit()
    return {"message": "Доска удалена"}
