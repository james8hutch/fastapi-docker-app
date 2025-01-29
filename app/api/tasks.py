from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.db import get_db
from app.service.tasks_service import TaskService
from app.schemas.tasks_schema import TaskSchema, TaskCreateSchema

router = APIRouter()

@router.get("/tasks", response_model=list[TaskSchema])
def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks."""
    return TaskService.fetch_all_tasks(db)


@router.get("/tasks/{task_id}", response_model=TaskSchema)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task by ID."""
    task = TaskService.fetch_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskCreateSchema, db: Session = Depends(get_db)):
    """Create a new task."""
    return TaskService.add_task(db, task.name)


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by ID."""
    success = TaskService.remove_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
