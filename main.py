from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start")
    await init_db()
    yield
    print("stooop")

app = FastAPI(lifespan=lifespan, title="Textboard API")

from routers import boards, threads, posts
app.include_router(boards.router)
app.include_router(threads.router)
app.include_router(posts.router)

@app.get("/")
async def root():
    return {
        "message": "hello textboard"
    }