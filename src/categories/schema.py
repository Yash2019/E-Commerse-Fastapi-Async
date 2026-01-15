from pydantic import BaseModel

class ReadCategory(BaseModel):
    name : str
    parent_id : int = None | None

class UpdateCategory(BaseModel):
    name: str = None | None 
    parent_id: int | None = None 
