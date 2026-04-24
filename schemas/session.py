from pydantic import BaseModel
from datetime import date, time


class SessionCreate(BaseModel):
    batch_id: int
    title: str
    date: date
    start_time: time
    end_time: time


class SessionResponse(BaseModel):
    id: int
    batch_id: int
    trainer_id: int
    title: str
    date: date
    start_time: time
    end_time: time

    class Config:
        from_attributes = True