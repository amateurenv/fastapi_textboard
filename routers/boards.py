import aiosqlite
from fastapi import APIRouter, Depends

from auth import verify_admin
from database import get_db
from schemas import BoardCreate, BoardResponse
from services import boards as board_service

router = APIRouter(prefix="/boards", tags=["Boards"])

@router.get("/", response_model=list[BoardResponse])
async def get_boards(db: aiosqlite.Connection = Depends(get_db)):
    return await board_service.get_all(db)

@router.post("/")
async def create_board(board: BoardCreate, db: aiosqlite.Connection = Depends(get_db), admin: str = Depends(verify_admin)):
    return await board_service.create(db, board)

@router.delete("/{url}")
async def delete_board(url: str, db: aiosqlite.Connection = Depends(get_db), admin: str = Depends(verify_admin)):
    return await board_service.delete(db, url)