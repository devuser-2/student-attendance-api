from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    class_name = Column(String)
    mobile = Column(String)

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    attendance_date = Column(Date)
    status = Column(String)