from models import Task
from schemas import TaskCreate


class TestTaskCrud:
	def test_create_task(self, test_app):
		task_data = TaskCreate(title="Test Task", description="This is a test task")

		response = test_app.post("/tasks/", json=task_data.dict())
		assert response.status_code == 200

		data = response.json()
		assert data["title"] == task_data.title
		assert data["description"] == task_data.description
		assert "id" in data

	def test_get_specific_task_success(self, test_app, ):
		test_app.post("/tasks/", json=TaskCreate(title="Test Task", description="This is a test task").dict())
		response = test_app.get(f"/tasks/1")
		assert response.status_code == 200
		data = response.json()

		task_data = Task(title="Test Task", description="This is a test task", id=1)
		assert data["title"] == task_data.title
		assert data["description"] == task_data.description
		assert data["id"] == task_data.id


	def test_get_specific_task_not_found(self, test_app, ):
		response = test_app.get(f"/tasks/{40}")
		assert response.status_code == 404
		data = response.json()

		assert data["detail"] == "Task not found"

	def test_read_tasks(self, test_app):
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
		for result, expected in zip(tasks, expected_tasks):
			assert result["id"] == expected["id"]
			assert result["title"] == expected["title"]
			assert result["description"] == expected["description"]

	def test_update_task_success(self, test_app, ):
		test_app.post("/tasks/", json=TaskCreate(title="Test Task", description="This is a test task").dict())
		updated_task_data = {"title": "Updated Test Task", "description": "This is an updated test task"}

		response = test_app.put(f"/tasks/1", json=updated_task_data)
		assert response.status_code == 200
		data = response.json()
		assert data["title"] == updated_task_data["title"]
		assert data["description"] == updated_task_data["description"]

	def test_update_task_not_found(self, test_app, ):
		updated_task_data = {"title": "Updated Test Task", "description": "This is an updated test task"}
		response = test_app.put(f"/tasks/90", json=updated_task_data)

		assert response.status_code == 404
		data = response.json()
		assert data["detail"] == "Task not found"

	def test_delete_task_success(self, test_app, ):
		test_app.post("/tasks/", json=TaskCreate(title="Test Task", description="This is a test task").dict())
		response = test_app.delete(f"/tasks/1")
		assert response.status_code == 200

	def test_delete_task_not_found(self, test_app, ):
		response = test_app.delete(f"/tasks/1")
		assert response.status_code == 404
		data = response.json()
		assert data["detail"] == "Task not found"
