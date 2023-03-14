from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
	try:
		db = TestingSessionLocal()
		yield db
	finally:
		db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestTaskCrud:
	def test_create_task(self):
		task_data = {"title": "Test Task", "description": "This is a test task"}
		response = client.post("/tasks/", json=task_data)
		assert response.status_code == 200
		data = response.json()
		assert data["title"] == task_data["title"]
		assert data["description"] == task_data["description"]
		assert "id" in data
		task_id = data["id"]

		response = client.get(f"/tasks/{task_id}")
		assert response.status_code == 200
		data = response.json()
		assert data["title"] == task_data["title"]
		assert data["description"] == task_data["description"]
		assert data["id"] == task_id

	def test_read_tasks(self):
		response = client.get("/tasks/")
		assert response.status_code == 200
		tasks = response.json()
		assert len(tasks) > 0
		for task in tasks:
			assert "id" in task
			assert "title" in task
			assert "description" in task

	def test_update_task(self):
		task_data = {"title": "Test Task", "description": "This is a test task"}
		response = client.post("/tasks/", json=task_data)
		assert response.status_code == 200
		data = response.json()
		assert data["title"] == task_data["title"]
		assert data["description"] == task_data["description"]
		assert "id" in data
		task_id = data["id"]

		updated_task_data = {"title": "Updated Test Task", "description": "This is an updated test task"}
		response = client.put(f"/tasks/{task_id}", json=updated_task_data)
		assert response.status_code == 200
		data = response.json()
		assert data["title"] == updated_task_data["title"]
		assert data["description"] == updated_task_data["description"]
		assert data["id"] == task_id

	def test_delete_task(self):
		task_data = {"title": "Test Task", "description": "This is a test task"}
		response = client.post("/tasks/", json=task_data)
		assert response.status_code == 200
		data = response.json()
		assert data["title"] == task_data["title"]
		assert data["description"] == task_data["description"]
		assert "id" in data
		task_id = data["id"]

		response = client.delete(f"/tasks/{task_id}")
		assert response.status_code == 200

		response = client.get(f"/tasks/{task_id}")
		assert response.status_code == 404
