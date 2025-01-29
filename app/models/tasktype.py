from sqlalchemy import Column, Integer, String
from app.db import Base

class TaskType(Base):
    __tablename__ = "task_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
