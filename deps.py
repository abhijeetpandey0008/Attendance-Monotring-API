from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from src.core.config import SECRET_KEY, ALGORITHM

security = HTTPBearer()


# 🔐 Standard JWT User
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return {
            "user_id": user_id,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# 🔒 Role Based Access Control
def require_role(*allowed_roles: str):

    def role_checker(user=Depends(get_current_user)):

        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Access forbidden"
            )

        return user

    return role_checker


# 🔥 Monitoring Scoped Token Only
def get_monitoring_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")
        role = payload.get("role")
        scope = payload.get("scope")

        if (
            user_id is None
            or role != "monitoring_officer"
            or scope != "monitoring"
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid monitoring token"
            )

        return {
            "user_id": user_id,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired monitoring token"
        )