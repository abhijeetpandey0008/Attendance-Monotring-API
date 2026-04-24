from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.api.deps import require_role

from src.models.user import User
from src.models.batch import Batch
from src.models.session import Session as SessionModel
from src.models.attendance import Attendance

router = APIRouter(
    tags=["Programme"]
)


# 🔥 Institution Summary
@router.get("/institutions/{institution_id}/summary")
def institution_summary(
    institution_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("programme_manager"))
):
    trainers = db.query(User).filter(
        User.role == "trainer",
        User.institution_id == institution_id
    ).count()

    students = db.query(User).filter(
        User.role == "student",
        User.institution_id == institution_id
    ).count()

    sessions = db.query(SessionModel).join(
        User,
        SessionModel.trainer_id == User.id
    ).filter(
        User.institution_id == institution_id
    ).count()

    attendance = db.query(Attendance).join(
        SessionModel,
        Attendance.session_id == SessionModel.id
    ).join(
        User,
        SessionModel.trainer_id == User.id
    ).filter(
        User.institution_id == institution_id
    ).count()

    return {
        "institution_id": institution_id,
        "trainers": trainers,
        "students": students,
        "sessions": sessions,
        "attendance_records": attendance
    }


# 🔥 Programme-wide Summary
@router.get("/programme/summary")
def programme_summary(
    db: Session = Depends(get_db),
    user=Depends(require_role("programme_manager"))
):
    institutions = db.query(User.institution_id).distinct().count()

    trainers = db.query(User).filter(
        User.role == "trainer"
    ).count()

    students = db.query(User).filter(
        User.role == "student"
    ).count()

    batches = db.query(Batch).count()

    sessions = db.query(SessionModel).count()

    attendance = db.query(Attendance).count()

    return {
        "institutions": institutions,
        "trainers": trainers,
        "students": students,
        "batches": batches,
        "sessions": sessions,
        "attendance_records": attendance
    }