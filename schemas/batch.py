from pydantic import BaseModel

class BatchCreate(BaseModel):
    name: str
    description: str | None = None


class BatchResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True

# 🔹 Student joins batch (direct join)
class JoinBatchRequest(BaseModel):
    batch_id: int


# 🔹 Invite creation response (trainer gets token)
class InviteResponse(BaseModel):
    token: str


# 🔹 Student joins using invite token
class JoinWithTokenRequest(BaseModel):
    token: str