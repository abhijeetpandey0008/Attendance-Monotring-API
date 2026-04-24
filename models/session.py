from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from src.database.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)

    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)