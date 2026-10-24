from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.exceptions import (
    http_exception_handler,
    verification_exception_handler,
    global_exception_handler,
)
from starlette.exceptions import HTTPException as StartleeteHTTPException
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="Task management api",
    description="APi for managing tasks",
    version="1.0.0",
)
app.add_exception_handler(StartleeteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, verification_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Task management api running"}
