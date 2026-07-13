"""Cấu hình"""

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    """Cấu hình cơ bản"""

    room_name: str = Field(..., min_length=1, examples=["Phòng 3E35"])
    floor: str = Field(..., min_length=1, examples=["Tầng 3"])
    capacity: int = Field(..., gt=0, examples=["35"])
    status: str = Field(..., min_length=1, examples=["available"])


class CreateRoom(RoomBase):
    """lớp tạo thêm"""


class UpdateRoom(RoomBase):
    """lớp cập nhật"""


class ResponseRoom(RoomBase):
    """lớp trả về"""
    id: int

    model_config = {"from_attributes": True}


def make_response(
    status_code: int,
    path: str,
    message: str,
    data: Any = None,
    error: Optional[str] = None,
) -> JSONResponse:
    """Chuẩn hóa trả về"""
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "error": error,
            "message": message,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data": data,
            "path": path,
        },
    )
