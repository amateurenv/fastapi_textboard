from contextlib import asynccontextmanager

import aiosqlite
from fastapi import FastAPI, Depends

from database import init_db, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Создаем таблицы в базе...")
    await init_db()
    yield
    print("Сервер выключается...")


app = FastAPI(lifespan=lifespan, title="Textboard API")

from routers import boards, threads, posts

app.include_router(boards.router)
app.include_router(threads.router)
app.include_router(posts.router)


@app.get("/")
async def root(db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute("SELECT id, url, name, created_at FROM boards") as cursor:
        rows = await cursor.fetchall()

    boards_list = [dict(row) for row in rows]

    return boards_list
