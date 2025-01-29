from fastapi import APIRouter, HTTPException
from app.schemas.tasktypes_schema import TaskTypeSchema
from app.service.tasktypes_service import TaskTypeService
from sqlalchemy.orm import Session
from app.db import get_db  # Assuming get_db is a dependency that provides the DB session
from fastapi import Depends

router = APIRouter()

@router.get("/task_types", response_model=list[TaskTypeSchema])
def get_task_types(db: Session = Depends(get_db)):
    """API endpoint to fetch task types."""
    # FastAPI does an automatic conversion here from TaskType to TaskTypeSchema as from_attributes is true
    task_types = TaskTypeService.fetch_task_types(db)
    if not task_types:
        raise HTTPException(status_code=404, detail="Task types not found")
    return task_types