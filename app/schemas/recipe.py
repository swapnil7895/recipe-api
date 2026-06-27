from pydantic import BaseModel, Field
from typing import Optional

class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    cooking_time_minutes : int = Field(..., gt=0)
    instructions: str = Field(...,min_length=10)    


class RecipeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    cooking_time_minutes: int
    instructions: str

    class Config:
        from_attributes = True


