from pydantic import BaseModel
from typing import Literal


# Allowed values for attendance
AttendanceStatus = Literal["present", "absent", "late"]


# 🔹 Mark Attendance Request
class AttendanceCreate(BaseModel):
    session_id: int
    status: AttendanceStatus


# 🔹 Attendance Response
class AttendanceResponse(BaseModel):
    id: int
    session_id: int
    student_id: int
    status: AttendanceStatus

    class Config:
        from_attributes = True


# 🔥 Attendance Summary Response
class AttendanceSummaryResponse(BaseModel):
    total_students: int
    present: int
    absent: int
    late: int
    attendance_percentage: float


# 🔥 Session Attendance List Response (NEW)
class SessionAttendanceResponse(BaseModel):
    student_id: int
    status: AttendanceStatus

    class Config:
        from_attributes = True