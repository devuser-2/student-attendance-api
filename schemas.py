from pydantic import BaseModel
class StudentCreate(BaseModel):
    name: str
    class_name: str
    mobile: str

class AttendanceCreate(BaseModel):
    student_id: int
    attendance_date: str
    status: str
class Login(BaseModel):
    username: str
    password: str
