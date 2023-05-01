from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import SessionLocal, engine, Base

app = FastAPI()

origins = [
	"http://localhost",
	"http://localhost:8000",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


def get_db():
	Base.metadata.create_all(bind=engine)
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
	if task.title.strip() == "" or task.description.strip() == "":
		raise HTTPException(status_code=400, detail="Title and description must not be empty")
	db_task = crud.create_task(db, task)
	return db_task


@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	tasks = crud.get_tasks(db, skip=skip, limit=limit)
	return tasks


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
	db_task = crud.get_task(db, task_id=task_id)
	if db_task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return db_task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
	if task.title.strip() == "" or task.description.strip() == "":
		raise HTTPException(status_code=400, detail="Title and description must not be empty")
	db_task = crud.get_task(db, task_id=task_id)
	if db_task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	updated_task = crud.update_task(db, db_task=db_task, task=task)
	return updated_task


@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
	db_task = crud.get_task(db, task_id=task_id)
	if db_task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	crud.delete_task(db, db_task=db_task)
	return db_task
