from fastapi import APIRouter, HTTPException, Depends
from app.schemas.tasks import TaskCreate, TaskResponse
from app.database import get_db
from app.models.task import Task
from sqlalchemy.orm import Session

router = APIRouter()
results = []

initial_value: int = 1


def counter():
    global initial_value
    current_id = initial_value
    initial_value += 1

    return current_id


# create tasks
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        completed=False,
        title=data.title,
        description=data.description,
    )
    db.add(new_task) #Adds the new ORM object to the session. SQLAlchemy tracks it as a new object to be inserted.
    db.commit() #Commits the transaction. SQLAlchemy flushes pending changes before committing, so the new task is inserted into PostgreSQL.
    db.refresh(new_task) #Reloads the object's values from the database. #For example, after the insert, new_task.id will contain the generated ID.
    return new_task


# get all tasks
@router.get("/", response_model=list[TaskCreate])
def get_all_tasks():
    return results


# get task by id
@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int):
    # filtered_obj = [obj for obj in results if obj["id"] == task_id] -- to return as array
    # to return just obj
    filtered_obj = next((obj for obj in results if obj["id"] == task_id), None)
    if not filtered_obj:
        raise HTTPException(
            status_code=404, detail=f"No task found with this task id {task_id}"
        )
    return filtered_obj


# update the task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updatedData: TaskCreate):
    filtered_obj = next((obj for obj in results if obj["id"] == task_id), None)
    if not filtered_obj:
        raise HTTPException(
            status_code=404, detail=f"No task found with this task id {task_id}"
        )
    filtered_obj["title"] = updatedData.title
    filtered_obj["description"] = updatedData.description
    return filtered_obj


@router.delete("/{task_id}")
def delete_task(task_id: int):
    filtered_obj = next((obj for obj in results if obj["id"] == task_id), None)
    if not filtered_obj:
        raise HTTPException(
            status_code=404, detail=f"No task found with this task id {task_id}"
        )
    results.remove(filtered_obj)
    return {
        "status": 200,
        "message": f"Successfully deleted the task by id {task_id}",
    }
