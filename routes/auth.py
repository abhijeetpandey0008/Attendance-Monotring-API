from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models.user import User

from src.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse
)

from src.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from src.api.deps import get_current_user
from src.core.config import MONITORING_API_KEY

router = APIRouter(prefix="/auth", tags=["Auth"])


# 🔹 SIGNUP
@router.post("/signup", response_model=TokenResponse)
def signup(user_data: SignupRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({
        "user_id": new_user.id,
        "role": new_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 🔹 LOGIN
@router.post("/login", response_model=TokenResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not user or not verify_password(
        user_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 🔥 Monitoring Officer Scoped Token
@router.post("/monitoring-token")
def monitoring_token(
    body: dict,
    user=Depends(get_current_user)
):

    if user["role"] != "monitoring_officer":
        raise HTTPException(
            status_code=403,
            detail="Only monitoring officer allowed"
        )

    key = body.get("key")

    if key != MONITORING_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    token = create_access_token(
        {
            "user_id": user["user_id"],
            "role": "monitoring_officer",
            "scope": "monitoring"
        },
        expires_minutes=60
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }