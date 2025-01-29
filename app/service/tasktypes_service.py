from sqlalchemy.orm import Session
from app.dao.tasktypes_dao import TaskTypeDAO
from app.models.tasktype import TaskType


class TaskTypeService:
    @staticmethod
    def fetch_task_types(db: Session) -> list[TaskType]:
        """Fetch all task types."""
        return TaskTypeDAO.get_all_task_types(db)
