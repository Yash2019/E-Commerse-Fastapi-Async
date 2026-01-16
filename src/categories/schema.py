from pydantic import BaseModel

class CreateCategorySchema(BaseModel):
    name : str
    parent_id : int | None = None

class ReadCategory(BaseModel):
    id: int
    name : str
    parent_id : int | None = None

class UpdateCategory(BaseModel):
    name: str | None  = None
    parent_id: int | None = None 
