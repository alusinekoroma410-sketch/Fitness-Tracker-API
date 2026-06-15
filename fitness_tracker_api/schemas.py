from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- WORKOUT SCHEMAS ---
class WorkoutBase(BaseModel):
    title: str
    activity_type: str
    duration_minutes: int
    calories_burned: Optional[float] = None

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutResponse(WorkoutBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# --- USER SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str