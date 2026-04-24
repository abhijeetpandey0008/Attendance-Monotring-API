from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.batch import Batch
from src.models.batch_student import BatchStudent
from src.models.invite import Invite
from src.models.session import Session as SessionModel
from src.models.attendance import Attendance


# 🔹 Create Batch
def create_batch(db: Session, name: str, description: str):
    batch = Batch(
        name=name,
        description=description
    )

    db.add(batch)
    db.commit()
    db.refresh(batch)

    return batch


# 🔹 Get All Batches
def get_batches(db: Session):
    return db.query(Batch).all()


# 🔹 Join Batch Directly
def join_batch(db: Session, batch_id: int, student_id: int):

    # Check batch exists
    batch = db.query(Batch).filter(Batch.id == batch_id).first()

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found"
        )

    # Prevent duplicate join
    existing = db.query(BatchStudent).filter(
        BatchStudent.batch_id == batch_id,
        BatchStudent.student_id == student_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already joined this batch"
        )

    record = BatchStudent(
        batch_id=batch_id,
        student_id=student_id
    )

    db.add(record)
    db.commit()

    return {"message": "Joined batch successfully"}


# 🔹 Create Invite
def create_invite(db: Session, batch_id: int, creator_id: int):

    # Check batch exists
    batch = db.query(Batch).filter(Batch.id == batch_id).first()

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found"
        )

    invite = Invite(
        batch_id=batch_id,
        created_by=creator_id
    )

    db.add(invite)
    db.commit()
    db.refresh(invite)

    return invite


# 🔹 Join via Invite Token
def join_batch_with_token(db: Session, token: str, student_id: int):

    invite = db.query(Invite).filter(
        Invite.token == token
    ).first()

    if not invite:
        raise HTTPException(
            status_code=404,
            detail="Invalid invite token"
        )

    if invite.is_used:
        raise HTTPException(
            status_code=400,
            detail="Invite already used"
        )

    # Prevent duplicate join
    existing = db.query(BatchStudent).filter(
        BatchStudent.batch_id == invite.batch_id,
        BatchStudent.student_id == student_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already joined this batch"
        )

    record = BatchStudent(
        batch_id=invite.batch_id,
        student_id=student_id
    )

    db.add(record)

    invite.is_used = True

    db.commit()

    return {"message": "Joined batch via invite"}


# 🔥 Batch Summary (NEW)
def get_batch_summary(db: Session, batch_id: int):

    batch = db.query(Batch).filter(Batch.id == batch_id).first()

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found"
        )

    total_students = db.query(BatchStudent).filter(
        BatchStudent.batch_id == batch_id
    ).count()

    total_sessions = db.query(SessionModel).filter(
        SessionModel.batch_id == batch_id
    ).count()

    attendance_records = db.query(Attendance).join(
        SessionModel,
        Attendance.session_id == SessionModel.id
    ).filter(
        SessionModel.batch_id == batch_id
    ).count()

    return {
        "batch_id": batch_id,
        "total_students": total_students,
        "total_sessions": total_sessions,
        "attendance_records": attendance_records
    }