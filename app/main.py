
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import engine, get_db, Base
from app.routers import employees
from app.schemas import Token, UserCreate
from app.auth import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models import User
import app.crud as crud


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="REST API for managing employees with CRUD operations and authentication",
    version="1.0.0"
)


app.include_router(employees.router)

@app.get("/")
def root():
    return {
        "message": "Employee Management API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/token",
            "register": "/register",
            "employees": "/api/employees/"
        }
    }

@app.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "username": new_user.username}

@app.post("/token", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    """Get access token for authentication"""
    user = crud.get_user(db, username=username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}   