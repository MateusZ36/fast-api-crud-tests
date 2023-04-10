from models import Task
from schemas import TaskCreate


def mocked_data(*args, **kwargs):
	return Task(title="Test Task", description="This is a test task", id=1)


def mocked_data_none(*args, **kwargs):
	return None


class TestTaskMockedCrud:
	def test_create_task(self, test_app, monkeypatch):
		monkeypatch.setattr("crud.create_task", mocked_data)

		task_data = TaskCreate(title="Test Task", description="This is a test task")

		response = test_app.post("/tasks/", json=task_data.dict())
		assert response.status_code == 200

		data = response.json()
		assert data["title"] == task_data.title
		assert data["description"] == task_data.description
		assert "id" in data

	def test_get_specific_task_success(self, test_app, monkeypatch):
		monkeypatch.setattr("crud.get_task", mocked_data)

		response = test_app.get(f"/tasks/1")
		assert response.status_code == 200
		data = response.json()

		task_data = Task(title="Test Task", description="This is a test task", id=1)
		assert data["title"] == task_data.title
		assert data["description"] == task_data.description
		assert data["id"] == task_data.id


	def test_get_specific_task_not_found(self, test_app, monkeypatch):
		monkeypatch.setattr("crud.get_task", mocked_data_none)

		response = test_app.get(f"/tasks/{40}")
		assert response.status_code == 404
		data = response.json()

		assert data["detail"] == "Task not found"


	def test_get_tasks(self, test_app, monkeypatch):
		def mocked_data(*args, **kwargs):
			return [
				Task(title="Test Task 1", description="This is a test task", id=1),
				Task(title="Test Task 2", description="This another test task", id=2),
				Task(title="Test Task 3", description="This yet another test task", id=3)
			]

		monkeypatch.setattr("crud.get_tasks", mocked_data)

		response = test_app.get("/tasks/")
		assert response.status_code == 200
		tasks = response.json()
		expected_tasks = [
			{"title": "Test Task 1", "description": "This is a test task", "id": 1},
			{"title": "Test Task 2", "description": "This another test task", "id": 2},
			{"title": "Test Task 3", "description": "This yet another test task", "id": 3}
		]

		assert len(tasks) == 3
		for result, expected in zip(tasks, expected_tasks):
			assert result["id"] == expected["id"]
			assert result["title"] == expected["title"]
			assert result["description"] == expected["description"]

	def test_update_task_success(self, test_app, monkeypatch):
		def mocked_data_update(*args, **kwargs):
			return Task(title="Updated Test Task", description="This is an updated test task", id=1)

		monkeypatch.setattr("crud.get_task", mocked_data)
		monkeypatch.setattr("crud.update_task", mocked_data_update)

		updated_task_data = {"title": "Updated Test Task", "description": "This is an updated test task"}
		response = test_app.put(f"/tasks/1", json=updated_task_data)
		assert response.status_code == 200
		data = response.json()
		assert data["title"] == updated_task_data["title"]
		assert data["description"] == updated_task_data["description"]

	def test_update_task_not_found(self, test_app, monkeypatch):
		monkeypatch.setattr("crud.get_task", mocked_data_none)

		updated_task_data = {"title": "Updated Test Task", "description": "This is an updated test task"}
		response = test_app.put(f"/tasks/1", json=updated_task_data)

		assert response.status_code == 404
		data = response.json()
		assert data["detail"] == "Task not found"

	def test_delete_task_success(self, test_app, monkeypatch):
		monkeypatch.setattr("crud.get_task", mocked_data)
		monkeypatch.setattr("crud.delete_task", mocked_data)

		response = test_app.delete(f"/tasks/1")
		assert response.status_code == 200

	def test_delete_task_not_found(self, test_app, monkeypatch):
		monkeypatch.setattr("crud.get_task", mocked_data_none)

		response = test_app.delete(f"/tasks/1")
		assert response.status_code == 404
		data = response.json()
		assert data["detail"] == "Task not found"
