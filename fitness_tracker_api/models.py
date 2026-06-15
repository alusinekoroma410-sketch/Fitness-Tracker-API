from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Links user to their workouts
    workouts = relationship("Workout", back_populates="owner")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    activity_type = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Key linking back to the User table
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="workouts")