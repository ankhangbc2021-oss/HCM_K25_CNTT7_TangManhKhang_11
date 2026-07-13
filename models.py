"""Cấu hình table"""

from sqlalchemy import Column, Integer, String

from database import Base


class Room(Base):
    """Cấu hình bảng"""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_name = Column(String(100), nullable=False)
    floor = Column(String(20), nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
