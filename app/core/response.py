from typing import Any
from app.schemas.common import APIResponse


def success_response(message: str, data: Any = None) -> dict:
    return APIResponse(
        success=True,
        message=message,
        data=data,
    ).model_dump(mode="json")
