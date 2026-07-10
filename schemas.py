from pydantic import BaseModel, Field

class BoardCreate(BaseModel):
    url: str = Field(..., min_length=1, max_length=10, description="Короткая ссылка (например 'b')")
    name: str = Field(..., min_length=1, max_length=50, description="Название (например 'Бред')")

class ThreadCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Заголовок треда")

class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000, description="Текст ответа")