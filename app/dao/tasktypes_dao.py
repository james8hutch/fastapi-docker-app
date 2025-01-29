from sqlalchemy.orm import Session
from app.models.tasktype import TaskType


class TaskTypeDAO:
    @staticmethod
    def get_all_task_types(db: Session) -> list[TaskType]:
        """Fetch all task types from the database."""
        return db.query(TaskType).all()
