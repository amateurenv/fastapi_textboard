from pydantic import BaseModel, Field
from datetime import datetime

class BoardCreate(BaseModel):
    url: str = Field(..., min_length=1, max_length=10, description="Короткая ссылка (например 'b')")
    name: str = Field(..., min_length=1, max_length=50, description="Название (например 'Бред')")

class ThreadCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Заголовок треда")

class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000, description="Текст ответа")


class BoardResponse(BaseModel):
    id: int
    url: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True 

class ThreadResponse(BaseModel):
    id: int
    board_id: int
    title: str
    created_at: datetime
    display_number: int  
    class Config:
        from_attributes = True