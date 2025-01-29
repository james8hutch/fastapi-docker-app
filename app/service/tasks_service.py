from sqlalchemy.orm import Session
from app.dao.tasks_dao import TaskDAO
from app.models.task import Task
from typing import Optional

class TaskService:
    @staticmethod
    def fetch_all_tasks(db: Session) -> list[Task]:
        """Fetch all tasks."""
        return TaskDAO.get_all_tasks(db)

    @staticmethod
    def fetch_task_by_id(db: Session, task_id: int) -> Optional[Task]:
        """Fetch a task by ID."""
        return TaskDAO.get_task_by_id(db, task_id)

    @staticmethod
    def add_task(db: Session, name: str) -> Task:
        """Add a new task."""
        return TaskDAO.create_task(db, name)

    @staticmethod
    def remove_task(db: Session, task_id: int) -> bool:
        """Remove a task by ID."""
        return TaskDAO.delete_task(db, task_id)
