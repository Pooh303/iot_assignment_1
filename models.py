from sqlalchemy import Boolean, Column, Integer, String, Date
from database import Base

class Student(Base):
    __tablename__ = 'students'

    first_name = Column(String, index=True)  # ชื่อ
    last_name = Column(String, index=True)  # นามสกุล
    student_id = Column(String, unique=True, primary_key=True, index=True)  # รหัสประจำตัวนักศึกษา
    birth_date = Column(Date, index=True)  # วันเกิด
    gender = Column(String, index=True)  # เพศ

