from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.schemas.batch import (
    BatchCreate,
    BatchResponse,
    JoinBatchRequest,
    InviteResponse,
    JoinWithTokenRequest
)

from src.services.batch_service import (
    create_batch,
    get_batches,
    join_batch,
    create_invite,
    join_batch_with_token,
    get_batch_summary
)

from src.api.deps import require_role, get_current_user
from src.models.batch import Batch

router = APIRouter(prefix="/batches", tags=["Batches"])


# 🔹 Create Batch (Trainer / Institution)
@router.post("/", response_model=BatchResponse)
def create_new_batch(
    batch: BatchCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("trainer", "institution"))
):
    return create_batch(db, batch.name, batch.description)


# 🔹 Get All Batches
@router.get("/", response_model=list[BatchResponse])
def get_all_batches(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_batches(db)


# 🔹 Get Single Batch
@router.get("/{batch_id}", response_model=BatchResponse)
def get_single_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()

    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    return batch


# 🔹 Join Batch Directly (Student)
@router.post("/join")
def join_batch_api(
    request: JoinBatchRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role("student"))
):
    return join_batch(
        db,
        request.batch_id,
        user["user_id"]
    )


# 🔹 Create Invite Token (Trainer)
@router.post("/{batch_id}/invite", response_model=InviteResponse)
def create_invite_api(
    batch_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("trainer"))
):
    invite = create_invite(db, batch_id, user["user_id"])
    return {"token": invite.token}


# 🔹 Join via Invite Token (Student)
@router.post("/join-with-token")
def join_with_token_api(
    request: JoinWithTokenRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role("student"))
):
    return join_batch_with_token(
        db,
        request.token,
        user["user_id"]
    )


# 🔥 Batch Summary (Institution only)
@router.get("/{batch_id}/summary")
def batch_summary_api(
    batch_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("institution"))
):
    return get_batch_summary(db, batch_id)