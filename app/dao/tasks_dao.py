from sqlalchemy.orm import Session
from app.models.task import Task
from typing import Optional

class TaskDAO:
    @staticmethod
    def get_all_tasks(db: Session) -> list[Task]:
        """Fetch all tasks."""
        return db.query(Task).all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
        """Fetch a task by its ID."""
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def create_task(db: Session, name: str) -> Task:
        """Create a new task."""
        task = Task(name=name)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        """Delete a task by ID."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return True
        return False
