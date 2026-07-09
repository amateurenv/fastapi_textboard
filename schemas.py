from pydantic import BaseModel, Field


# схема для проверки данных при создании доски
class BoardCreate(BaseModel):
    url: str = Field(..., description="Короткая ссылка, например 'b'")
    name: str = Field(..., description="Название доски, например 'Бред'")
