from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceSummaryResponse
)
from src.services.attendance_service import (
    mark_attendance,
    get_attendance,
    get_session_attendance_summary
)
from src.api.deps import require_role, get_current_user

router = APIRouter(prefix="/attendance", tags=["Attendance"])


# 🔹 Mark Attendance (STUDENT ONLY)
@router.post("/mark", response_model=AttendanceResponse)
def mark_attendance_api(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("student"))
):
    return mark_attendance(
        db,
        attendance.session_id,
        user["user_id"],   # from JWT
        attendance.status
    )


# 🔹 Get All Attendance (any logged-in user)
@router.get("/", response_model=list[AttendanceResponse])
def get_all_attendance(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_attendance(db)


# 🔥 NEW: Session Attendance Summary
@router.get("/summary/{session_id}", response_model=AttendanceSummaryResponse)
def get_attendance_summary(
    session_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_session_attendance_summary(db, session_id)