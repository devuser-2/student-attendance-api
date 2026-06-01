from pydantic import BaseModel
from datetime import date
class StudentCreate(BaseModel):
    name: str
    class_name: str
    mobile: str

class AttendanceCreate(BaseModel):
    student_id: int
    attendance_date: date
    status: str
class Login(BaseModel):
    username: str
    password: str
