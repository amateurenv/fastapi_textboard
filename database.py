import aiosqlite

DB_NAME = "textboard.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # поддержка внешних связей
        await db.execute("PRAGMA foreign_keys = ON;")

        # таблица досок
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS boards
                         (
                             id   INTEGER PRIMARY KEY AUTOINCREMENT,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             url TEXT UNIQUE NOT NULL,
                             name TEXT        NOT NULL
                         )
                         """)

        # таблица тредов
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS threads
                         (
                             id       INTEGER PRIMARY KEY AUTOINCREMENT,
                             board_id INTEGER NOT NULL,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             title    TEXT NOT NULL,
                             FOREIGN KEY (board_id) REFERENCES boards (id) ON DELETE CASCADE
                         )
                         """)

        # таблица постов
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS posts
                         (
                             id        INTEGER PRIMARY KEY AUTOINCREMENT,
                             thread_id INTEGER NOT NULL,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             content   TEXT    NOT NULL,
                             FOREIGN KEY (thread_id) REFERENCES threads (id) ON DELETE CASCADE
                         )
                         """)

        await db.commit()


async def get_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        db.row_factory = aiosqlite.Row
        yield db
