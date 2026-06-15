from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

import models
import schemas
import auth
from database import engine, get_db

# Initialize the FastAPI application
app = FastAPI(
    title="Fitness Tracker API",
    description="An API to track workouts and support SDG 3: Good Health and Well-being",
    version="1.0.0"
)

# Automatically generate database tables on server start
models.Base.metadata.create_all(bind=engine)

# This tells FastAPI where to look for the security token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --- SECURITY DEPENDENCY ---

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Decode the incoming JWT token string using your auth settings
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        
        # 2. Extract the username from the 'sub' (Subject) claim field
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except jwt.PyJWTError:
        # If the token is expired, modified, or corrupted, block them immediately
        raise credentials_exception
        
    # 3. Search the active database for this specific username string
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
        
    # Return the verified user object to the endpoint
    return user

# --- BASIC ENDPOINTS ---

@app.get("/")
async def home():
    return {"message": "Welcome to the Fitness Tracker API! SDG 3 in action."}


# --- USER AUTHENTICATION ENDPOINTS ---

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a brand new account asynchronously with an encrypted password."""
    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username is already taken")

    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is already registered")

    # Uses our updated stable native bcrypt hashing helper
    hashed_pass = auth.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=schemas.Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Log in a user asynchronously and return a secure JWT access token."""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# --- WORKOUT CRUD OPERATIONS ---

@app.post("/workouts/", response_model=schemas.WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(
    workout: schemas.WorkoutCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Log a new workout activity locked to your personal authorized user account."""
    db_workout = models.Workout(
        title=workout.title,
        activity_type=workout.activity_type,
        duration_minutes=workout.duration_minutes,
        calories_burned=workout.calories_burned,
        owner_id=current_user.id
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@app.get("/workouts/", response_model=list[schemas.WorkoutResponse])
async def read_workouts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Fetch a list of all logged items asynchronously."""
    workouts = db.query(models.Workout).offset(skip).limit(limit).all()
    return workouts


@app.get("/workouts/{workout_id}", response_model=schemas.WorkoutResponse)
async def read_workout(workout_id: int, db: Session = Depends(get_db)):
    """Fetch a specific logged item by its ID."""
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@app.put("/workouts/{workout_id}", response_model=schemas.WorkoutResponse)
async def update_workout(workout_id: int, updated_workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    """Modify details of an existing log asynchronously."""
    workout_query = db.query(models.Workout).filter(models.Workout.id == workout_id)
    workout = workout_query.first()
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    workout_query.update(updated_workout.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(workout)
    return workout


@app.delete("/workouts/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    """Permanently delete an item."""
    workout_query = db.query(models.Workout).filter(models.Workout.id == workout_id)
    workout = workout_query.first()
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    workout_query.delete(synchronize_session=False)
    db.commit()
    return None