"""Kết nối database"""

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

PASSWORD = "12345678"

SQLACHEMA_DATABASE_URL = f"mysql+pymysql://root:{PASSWORD}@localhost:3306/room_db"

temp_conn = pymysql.connect(host="localhost", user="root", password=PASSWORD)

try:
    with temp_conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS room_db")
finally:
    temp_conn.close()

engine = create_engine(SQLACHEMA_DATABASE_URL, pool_pre_ping=True)

SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Lấy"""
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()
