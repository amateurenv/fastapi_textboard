from fastapi import HTTPException
import aiosqlite

def add_display_numbers(rows: list, start: int = 1) -> list:
    items = []
    for index, row in enumerate(rows, start=start):
        item = dict(row)
        item["display_number"] = index
        items.append(item)
    return items

async def check_deleted_or_404(cursor: aiosqlite.Cursor, error_msg: str):
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail=error_msg)