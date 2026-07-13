"""Lớp xử lý logic"""

from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import Room
from schemas import CreateRoom, ResponseRoom, UpdateRoom, make_response


def get_all_room(db: Session, path: str):
    """Lấy tất cả phòng"""
    rooms = db.query(Room).all()

    if not rooms:
        return make_response(
            status_code=status.HTTP_404_NOT_FOUND,
            path=path,
            message="Danh sách phòng đang trống",
            error="Not Found",
        )

    data = [ResponseRoom.model_validate(r).model_dump() for r in rooms]

    return make_response(
        status_code=status.HTTP_200_OK,
        path=path,
        message="Đã lấy thành công danh sách",
        data=data,
    )


def get_room_by_id(db: Session, path: str, room_id: int):
    """Lấy phòng theo id"""
    room = db.query(Room).filter_by(id=room_id).first()

    if not room:
        return make_response(
            status_code=status.HTTP_404_NOT_FOUND,
            path=path,
            message=f"Không tìm thấy phòng có id là {room_id}",
            error="Not Found",
        )

    data = ResponseRoom.model_validate(room).model_dump()

    return make_response(
        status_code=status.HTTP_200_OK,
        path=path,
        message=f"Đã lấy thành công phòng có id là {room_id}",
        data=data,
    )


def create_room(db: Session, path: str, data_create: CreateRoom):
    """Thêm phòng"""

    new_room = Room(**data_create.model_dump())

    try:
        db.add(new_room)
        db.commit()
        db.refresh(new_room)

        data = ResponseRoom.model_validate(new_room).model_dump()

        return make_response(
            status_code=status.HTTP_201_CREATED,
            path=path,
            message="Đã tạo thành công",
            data=data,
        )
    except SQLAlchemyError as sql:
        db.rollback()

        return make_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            path=path,
            message="Lỗi trong quá trình tạo phòng",
            error=str(sql),
        )


def update_room(db: Session, path: str, room_id: int, data_upadate: UpdateRoom):
    """Cập nhật phòng"""
    room = db.query(Room).filter_by(id=room_id).first()

    if not room:
        return make_response(
            status_code=status.HTTP_404_NOT_FOUND,
            path=path,
            message=f"Không tìm thấy phòng có id là {room_id} để cập nhật",
            error="Not Found",
        )

    for key, value in data_upadate.model_dump().items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)

    data = ResponseRoom.model_validate(room).model_dump()

    return make_response(
        status_code=status.HTTP_200_OK,
        path=path,
        message=f"Đã cập nhật thành công phòng có id là {room_id}",
        data=data,
    )


def delete_room(db: Session, path: str, room_id: int):
    """Xóa phòng theo id"""
    room = db.query(Room).filter_by(id=room_id).first()

    if not room:
        return make_response(
            status_code=status.HTTP_404_NOT_FOUND,
            path=path,
            message=f"Không tìm thấy phòng có id là {room_id} để cập nhật",
            error="Not Found",
        )

    db.delete(room)
    db.commit()

    data = ResponseRoom.model_validate(room).model_dump()

    return make_response(
        status_code=status.HTTP_200_OK,
        path=path,
        message=f"Đã xóa thành công phòng có id là {room_id}",
        data=data,
    )


def search_status(db: Session, path: str, status_search: str):
    """Tìm phòng theo status"""
    query = db.query(Room)

    rooms = query.filter(Room.status.ilike(f"%{status_search}%"))

    if not rooms:
        return make_response(
            status_code=status.HTTP_404_NOT_FOUND,
            path=path,
            message=f"Không tìm thấy phòng có status là {status_search} để cập nhật",
            error="Not Found",
        )

    data = [ResponseRoom.model_validate(r).model_dump() for r in rooms]

    return make_response(
        status_code=status.HTTP_200_OK,
        path=path,
        message=f"Đã lấy thành công danh sách có status là {status_search}",
        data=data,
    )
