from itertools import zip_longest

import pytest
from pydantic import ValidationError

from models import Task
from schemas import TaskCreate


class TestTaskCrud:

	# CT_001
	def test_create_task(self, test_app):
		task_data = TaskCreate(title="test title 1", description="test description 1")

		response = test_app.post("/tasks/", json=task_data.dict())
		assert response.status_code == 200

		data = response.json()
		assert data["title"] == task_data.title
		assert data["description"] == task_data.description
		assert data["id"] == 1

	# CT_002
	def test_create_task_error(self, test_app):
		response = test_app.post("/tasks/", json={"title": "test title 1"})
		assert response.status_code == 422

		data = response.json()
		assert data["detail"][0]["msg"] == "field required"
		assert data["detail"][0]["type"] == "value_error.missing"

	def test_get_specific_task_success(self, test_app):
		test_app.post("/tasks/", json=TaskCreate(title="test title 1", description="test description 1").dict())
		response = test_app.get(f"/tasks/1")
		assert response.status_code == 200

		data = response.json()
		task_data = Task(title="test title 1", description="test description 1", id=1)
		assert data["title"] == task_data.title
		assert data["description"] == task_data.description
		assert data["id"] == task_data.id

	def test_get_specific_task_not_found(self, test_app):
		response = test_app.get(f"/tasks/{40}")
		assert response.status_code == 404

		data = response.json()
		assert data["detail"] == "Task not found"

	def test_get_tasks(self, test_app):
		test_app.post("/tasks/", json=TaskCreate(title="Test Task 1", description="This is a test task").dict())
		test_app.post("/tasks/", json=TaskCreate(title="Test Task 2", description="This another test task").dict())
		test_app.post("/tasks/", json=TaskCreate(title="Test Task 3", description="This yet another test task").dict())
		response = test_app.get("/tasks/")
		assert response.status_code == 200

		tasks = response.json()
		expected_tasks = [
			{"title": "Test Task 1", "description": "This is a test task", "id": 1},
			{"title": "Test Task 2", "description": "This another test task", "id": 2},
			{"title": "Test Task 3", "description": "This yet another test task", "id": 3}
		]

		assert len(tasks) == 3
		for result, expected in zip_longest(tasks, expected_tasks, fillvalue={}):
			assert result.get("id") == expected.get("id")
			assert result.get("title") == expected.get("title")
			assert result.get("description") == expected.get("description")

	# CT_003
	def test_update_task_success(self, test_app):
		test_app.post("/tasks/", json=TaskCreate(title="test title 1", description="test description 1").dict())

		updated_task_data = {"title": "new title", "description": "new description"}
		response = test_app.put(f"/tasks/1", json=updated_task_data)
		assert response.status_code == 200

		data = response.json()
		assert data["title"] == updated_task_data["title"]
		assert data["description"] == updated_task_data["description"]

	# CT_004
	def test_update_task_error(self, test_app):
		updated_task_data = {"title": "new title"}
		response = test_app.put(f"/tasks/1", json=updated_task_data)
		assert response.status_code == 422

		data = response.json()
		assert data["detail"][0]["msg"] == "field required"
		assert data["detail"][0]["type"] == "value_error.missing"

	# CT_005
	def test_update_task_not_found(self, test_app):
		task_data = TaskCreate(title="new title", description="This is an updated test task")
		response = test_app.put(f"/tasks/1", json=task_data.dict())
		assert response.status_code == 404

		data = response.json()
		assert data["detail"] == "Task not found"
