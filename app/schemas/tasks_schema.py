from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TaskCreateSchema(BaseModel):
    name: str
