from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=1000)


class TaskResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )  # from_attributes=True allows Pydantic to read values such as new_task.id from an ORM object instead of expecting a dictionary.
    id: int
    completed: bool
    description: str
    title: str
