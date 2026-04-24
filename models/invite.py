from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from src.database.database import Base
import datetime
import uuid


class Invite(Base):
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)

    token = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))

    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    is_used = Column(Boolean, default=False)