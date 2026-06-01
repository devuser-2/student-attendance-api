from pydantic import BaseModel, Field
from datetime import date

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1)
    class_name: str = Field(..., min_length=1)
    mobile: str = Field(..., min_length=1)

class AttendanceCreate(BaseModel):
    student_id: int
    attendance_date: date
    status: str

class Login(BaseModel):
    username: str
    password: str