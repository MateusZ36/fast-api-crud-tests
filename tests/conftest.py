import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from database import Base
from main import app, get_db


@pytest.fixture(scope="session")
def test_app():
	app.dependency_overrides[get_db] = override_get_db

	client = TestClient(app)
	yield client
	Base.metadata.drop_all(engine)
	client.close()


engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
	Base.metadata.create_all(bind=engine)
	try:
		db = TestingSessionLocal()
		yield db
	finally:
		db.close()


def reset_db():
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(bind=engine)


def pytest_runtest_setup(item):
	reset_db()
