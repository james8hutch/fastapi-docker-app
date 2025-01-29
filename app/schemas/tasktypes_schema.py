from pydantic import BaseModel

class TaskTypeSchema(BaseModel):
    id: int
    name: str  # Add all required fields

    class Config:
        from_attributes = True
