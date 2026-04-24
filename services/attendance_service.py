from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from src.models.attendance import Attendance
from src.models.session import Session as SessionModel
from src.models.batch_student import BatchStudent


# 🔹 Mark Attendance (Student)
def mark_attendance(db: Session, session_id: int, student_id: int, status: str):

    # Check session exists
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Check student belongs to batch
    enrolled = db.query(BatchStudent).filter(
        BatchStudent.batch_id == session.batch_id,
        BatchStudent.student_id == student_id
    ).first()

    if not enrolled:
        raise HTTPException(
            status_code=403,
            detail="You are not enrolled in this batch"
        )

    # Prevent duplicate attendance
    existing = db.query(Attendance).filter(
        Attendance.session_id == session_id,
        Attendance.student_id == student_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked"
        )

    # Time validation
    now = datetime.now()

    session_start = datetime.combine(
        session.date,
        session.start_time
    )

    session_end = datetime.combine(
        session.date,
        session.end_time
    )

    if now < session_start:
        raise HTTPException(
            status_code=400,
            detail="Session has not started yet"
        )

    if now > session_end:
        raise HTTPException(
            status_code=400,
            detail="Session has already ended"
        )

    # Save attendance
    attendance = Attendance(
        session_id=session_id,
        student_id=student_id,
        status=status
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance


# 🔹 Get All Attendance
def get_attendance(db: Session):
    return db.query(Attendance).all()


# 🔥 Session Summary
def get_session_attendance_summary(db: Session, session_id: int):

    session = db.query(SessionModel).filter(
        SessionModel.id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    total_students = db.query(BatchStudent).filter(
        BatchStudent.batch_id == session.batch_id
    ).count()

    present = db.query(Attendance).filter(
        Attendance.session_id == session_id,
        Attendance.status == "present"
    ).count()

    absent = db.query(Attendance).filter(
        Attendance.session_id == session_id,
        Attendance.status == "absent"
    ).count()

    late = db.query(Attendance).filter(
        Attendance.session_id == session_id,
        Attendance.status == "late"
    ).count()

    percentage = (
        (present / total_students) * 100
        if total_students > 0 else 0
    )

    return {
        "total_students": total_students,
        "present": present,
        "absent": absent,
        "late": late,
        "attendance_percentage": round(percentage, 2)
    }


# 🔥 Full Attendance List for Session
def get_session_attendance(db: Session, session_id: int):

    session = db.query(SessionModel).filter(
        SessionModel.id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    records = db.query(Attendance).filter(
        Attendance.session_id == session_id
    ).all()

    return records