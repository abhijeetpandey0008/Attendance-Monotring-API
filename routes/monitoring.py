from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.api.deps import get_current_user
from src.models.attendance import Attendance

router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)


# 🔥 Monitoring Officer Read-only Attendance
@router.get("/attendance")
def monitoring_attendance(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    # Must be monitoring officer
    if user["role"] != "monitoring_officer":
        raise HTTPException(
            status_code=403,
            detail="Access forbidden"
        )

    records = db.query(Attendance).all()

    return records