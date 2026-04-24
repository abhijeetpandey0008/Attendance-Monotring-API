from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db

from src.schemas.session import (
    SessionCreate,
    SessionResponse
)

from src.schemas.attendance import SessionAttendanceResponse

from src.services.session_service import (
    create_session,
    get_sessions
)

from src.services.attendance_service import get_session_attendance

from src.api.deps import require_role, get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])


# 🔹 Create Session (Trainer only)
@router.post("/", response_model=SessionResponse)
def create_new_session(
    session: SessionCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("trainer"))
):
    return create_session(
        db,
        session.batch_id,
        user["user_id"],
        session.title,
        session.date,
        session.start_time,
        session.end_time
    )


# 🔹 Get All Sessions
@router.get("/", response_model=list[SessionResponse])
def get_all_sessions(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_sessions(db)


# 🔥 Get Full Attendance List for Session (Trainer)
@router.get("/{session_id}/attendance",
            response_model=list[SessionAttendanceResponse])
def get_session_attendance_api(
    session_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("trainer"))
):
    return get_session_attendance(db, session_id)