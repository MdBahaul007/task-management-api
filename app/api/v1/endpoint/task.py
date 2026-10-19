from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.tasks import TaskCreate, TaskResponse
from app.database import get_db
from app.models.task import Task
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Literal

router = APIRouter()


# create tasks
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        completed=False,
        title=data.title,
        description=data.description,
    )
    db.add(
        new_task
    )  # Adds the new ORM object to the session. SQLAlchemy tracks it as a new object to be inserted.
    db.commit()  # Commits the transaction. SQLAlchemy flushes pending changes before committing, so the new task is inserted into PostgreSQL.
    db.refresh(
        new_task
    )  # Reloads the object's values from the database. #For example, after the insert, new_task.id will contain the generated ID.
    return new_task


# get all tasks
@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    completed: bool | None = Query(default=None),
    search: str | None = Query(default=None, min_length=1, max_length=30),
    sortby: Literal["id", "title"] = Query(default="id"),
    orderby: Literal["asc", "desc"] = Query(default="asc"),
    # db is your SQLAlchemy session.
):
    # if completed is not None:
    #     statement = select(Task).where(Task.completed == completed).order_by(Task.id)
    # else:
    #     statement = select(Task).order_by(Task.id)
    # same way above commented code can be done as

    # statement = select(Task).order_by(Task.id)  # base query
    statement = select(Task)  # base query

    if completed is not None:
        statement = statement.where(Task.completed == completed)
    if search is not None:
        statement = statement.where(Task.title.ilike(f"%{search}%"))
    if sortby == "title":
        sort_col = Task.title
    else:
        sort_col = Task.id

    if orderby == "desc":
        statement = statement.order_by(sort_col.desc())
    else:
        statement = statement.order_by(sort_col.asc())

    task = db.scalars(
        statement.limit(limit).offset(offset)
    ).all()  # it executes the query
    return task


# Select(Task) = SELECT * FROM tasks; #it only build the query
# scalars() extracts the Task objects from the query results. .all() method always returns a list, even if the query matches only one record.


# get task by id
@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    # filtered_obj = [obj for obj in results if obj["id"] == task_id] -- to return as array
    # to return just obj
    # filtered_obj = next((obj for obj in results if obj["id"] == task_id), None)
    statement = select(Task).where(Task.id == task_id)
    filtered_obj = db.scalars(
        statement
    ).one_or_none()  # one_or_none() - If a matching task exists, it returns the Task object not list else return none.
    if filtered_obj is None:
        raise HTTPException(
            status_code=404, detail=f"No task found with this task id {task_id}"
        )

    return filtered_obj


# update the task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updatedData: TaskCreate, db: Session = Depends(get_db)):
    # filtered_obj = next((obj for obj in results if obj["id"] == task_id), None)
    statement = select(Task).where(Task.id == task_id)
    filtered_obj = db.scalars(statement).one_or_none()
    if filtered_obj is None:
        raise HTTPException(
            status_code=404, detail=f"No task found with this task id {task_id}"
        )
    filtered_obj.title = updatedData.title
    filtered_obj.description = updatedData.description
    db.commit()
    db.refresh(filtered_obj)
    return filtered_obj


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    statement = select(Task).where(Task.id == task_id)
    filtered_obj = db.scalars(statement).one_or_none()
    if filtered_obj is None:
        raise HTTPException(
            status_code=404, detail=f"No task found with this task id {task_id}"
        )
    db.delete(filtered_obj)
    db.commit()
    return {
        "status": 200,
        "message": f"Successfully deleted the task by id {task_id}",
    }
