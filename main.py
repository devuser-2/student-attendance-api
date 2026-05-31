from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from datetime import date
import csv
import os
from database import SessionLocal, engine
from models import Base, Student, Attendance
from schemas import StudentCreate, AttendanceCreate, Login
from security import verify_token

from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app = FastAPI()
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/students")
def get_students(
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
    ):
    return db.query(Student).all()

@app.post("/attendance")
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):

    existing = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.attendance_date == attendance.attendance_date
    ).first()

    if existing:
        return {"message": "Attendance already marked"}

    new = Attendance(**attendance.dict())

    db.add(new)
    db.commit()
    db.refresh(new)

    return new

@app.get("/attendance")
def get_attendance(db: Session = Depends(get_db)):
    records = db.query(Attendance).all()

    result = []
    for r in records:
        student = db.query(Student).filter(Student.id == r.student_id).first()

        result.append({
            "student_name": student.name if student else "Unknown",
            "date": r.attendance_date,
            "status": r.status
        })

    return result

@app.get("/report/student/{student_id}")
def student_report(
    student_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):

    records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    total = len(records)
    present = len([r for r in records if r.status.lower() == "present"])
    absent = len([r for r in records if r.status.lower() == "absent"])

    student = db.query(Student).filter(Student.id == student_id).first()

    return {
        "student_name": student.name if student else "Unknown",
        "total_days": total,
        "present": present,
        "absent": absent,
        "percentage": round((present/total)*100, 2) if total else 0
    }
@app.get("/report/monthly")
def monthly_report(month: str, db: Session = Depends(get_db)):

    records = db.query(Attendance).filter(
        Attendance.attendance_date.like(f"{month}%")
    ).all()

    return {
        "month": month,
        "total_records": len(records)
    }
@app.get("/ui/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/ui/attendance")
def attendance_page(request: Request):
    return templates.TemplateResponse("attendance.html", {"request": request})

@app.get("/export/students")
def export_students(db: Session = Depends(get_db)):

    students = db.query(Student).all()

    file = "students.csv"

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Class", "Mobile"])

        for s in students:
            writer.writerow([s.id, s.name, s.class_name, s.mobile])

    return FileResponse(file, media_type="text/csv")