"""Tăng Mạnh Khang - Đề 11"""

from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from routers import (
    create_room,
    delete_room,
    get_all_room,
    get_room_by_id,
    search_status,
    update_room,
)
from schemas import CreateRoom, UpdateRoom

app = FastAPI(title="Kiểm tra hackathon đề 11")

Base.metadata.create_all(bind=engine)


@app.get("/")
def get_root():
    """Kiểm tra"""
    return "Kết nối thành công"


@app.get("/meeting-rooms", tags=["Rooms"])
def get_all(request: Request, db: Session = Depends(get_db)):
    """Lấy hết ds phòng"""
    return get_all_room(db, str(request.url.path))


@app.get("/meeting-rooms/search", tags=["Rooms"])
def search_status_value(
    request: Request, status_search: str, db: Session = Depends(get_db)
):
    """Tìm kiếm status"""
    return search_status(db, str(request.url.path), status_search)


@app.get("/meeting-rooms/{room_id}", tags=["Rooms"])
def get_room_id(request: Request, room_id: int, db: Session = Depends(get_db)):
    """Lấy theo id"""
    return get_room_by_id(db, str(request.url.path), room_id)


@app.post("/meeting-rooms", tags=["Rooms"])
def create_room_new(
    request: Request, data_create: CreateRoom, db: Session = Depends(get_db)
):
    """Tạo mới phòng"""
    return create_room(db, str(request.url.path), data_create)


@app.put("/meeting-rooms/{room_id}", tags=["Rooms"])
def update_by_id(
    request: Request,
    room_id: int,
    data_update: UpdateRoom,
    db: Session = Depends(get_db),
):
    """Cập nhật"""
    return update_room(db, str(request.url.path), room_id, data_update)


@app.delete("/meeting-rooms/{room_id}", tags=["Rooms"])
def delete_by_id(
    request: Request,
    room_id: int,
    db: Session = Depends(get_db),
):
    """Xóa theo id"""
    return delete_room(db, str(request.url.path), room_id)
