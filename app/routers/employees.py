
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.auth import get_current_user
from app.models import User
import app.crud as crud

router = APIRouter(prefix="/api/employees", tags=["employees"])

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new employee"""
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_employee(db=db, employee=employee)

@router.get("/", response_model=dict)
def list_employees(
    page: int = Query(1, ge=1, description="Page number"),
    department: Optional[str] = Query(None, description="Filter by department"),
    role: Optional[str] = Query(None, description="Filter by role"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all employees with pagination and filtering"""
    limit = 3
    skip = (page - 1) * limit
    
    employees = crud.get_employees(
        db, skip=skip, limit=limit, department=department, role=role
    )


    validated_employees = [EmployeeResponse.model_validate(e) for e in employees]
    
    total = crud.get_total_employees(db, department=department, role=role)
    
    return {
        "employees": validated_employees, 
        "page": page,
        "per_page": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit
    }

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single employee by ID"""
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return db_employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an employee's details"""
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    if employee.email and employee.email != db_employee.email:
        existing = crud.get_employee_by_email(db, email=employee.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    return crud.update_employee(db=db, employee_id=employee_id, employee=employee)

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an employee"""
    success = crud.delete_employee(db, employee_id=employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return None