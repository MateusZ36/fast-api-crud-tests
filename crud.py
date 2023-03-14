from sqlalchemy.orm import Session
import models
import schemas


def create_task(db: Session, task: schemas.TaskCreate):
	db_task = models.Task(title=task.title, description=task.description)
	db.add(db_task)
	db.commit()
	db.refresh(db_task)
	return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
	return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, db_task: models.Task, task: schemas.TaskUpdate):
	db_task.title = task.title
	db_task.description = task.description
	db.commit()
	db.refresh(db_task)
	return db_task


def delete_task(db: Session, db_task: models.Task):
	db.delete(db_task)
	db.commit()
	return db_task
