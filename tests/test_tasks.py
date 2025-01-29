import sys
from sqlalchemy import inspect
from conftest import print_tables

def test_check_tables(test_db_session):
    """
    Check the database state and ensure the tables are present.
    """
    from app.models.task import Task
    print_tables(test_db_session)

    # Ensure the `tasks` table is present and empty
    tasks = test_db_session.query(Task).all()
    assert len(tasks) == 0

def test_get_tasks_empty(client, test_db_session):
    """
    Test GET /tasks when there are no tasks in the database.
    """
    response = client.get("/tasks")
    print(f"Response: {response.text}")  # Print the response content
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client, test_db_session):
    """
    Test POST /tasks to create a new task.
    """
    task_data = {"name": "Test Task"}
    response = client.post("/tasks", json=task_data)

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Test Task"
    assert "id" in response_data

    # Verify the task in the database
    from app.models.task import Task  # Import the model within the test
    db_task = test_db_session.query(Task).filter_by(id=response_data["id"]).first()
    assert db_task is not None
    assert db_task.name == "Test Task"


def test_get_task_by_id(client, test_db_session):
    """
    Test GET /tasks/{task_id} to retrieve a specific task by ID.
    """
    # Create a task in the test database
    from app.models.task import Task
    new_task = Task(name="Test Task")
    test_db_session.add(new_task)
    test_db_session.commit()

    # Retrieve the task by ID
    response = client.get(f"/tasks/{new_task.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == new_task.id
    assert response_data["name"] == new_task.name


def test_delete_task(client, test_db_session):
    """
    Test DELETE /tasks/{task_id} to delete a task by ID.
    """
    # Create a task in the test database
    from app.models.task import Task
    new_task = Task(name="Test Task")
    test_db_session.add(new_task)
    test_db_session.commit()

    # Delete the task
    response = client.delete(f"/tasks/{new_task.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

    # Verify the task is no longer in the database
    deleted_task = test_db_session.query(Task).filter_by(id=new_task.id).first()
    assert deleted_task is None


def test_get_task_after_deletion(client, test_db_session):
    """
    Test GET /tasks/{task_id} after the task has been deleted.
    """
    # Create and delete a task
    from app.models.task import Task
    new_task = Task(name="Test Task")
    test_db_session.add(new_task)
    test_db_session.commit()
    test_db_session.delete(new_task)
    test_db_session.commit()

    # Try to retrieve the deleted task
    response = client.get(f"/tasks/{new_task.id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_nonexistent_task(client):
    """
    Test DELETE /tasks/{task_id} when the task does not exist.
    """
    nonexistent_task_id = 9999  # Arbitrary ID that doesn't exist
    response = client.delete(f"/tasks/{nonexistent_task_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
