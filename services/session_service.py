from sqlalchemy.orm import Session
from src.models.session import Session as SessionModel


# 🔹 Create Session (TRAINER)
def create_session(
    db: Session,
    batch_id: int,
    trainer_id: int,
    title: str,
    date,
    start_time,
    end_time
):
    session = SessionModel(
        batch_id=batch_id,
        trainer_id=trainer_id,
        title=title,
        date=date,
        start_time=start_time,
        end_time=end_time
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


# 🔹 Get all sessions
def get_sessions(db: Session):
    return db.query(SessionModel).all()