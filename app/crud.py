from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Employee, User
from app.schemas import EmployeeCreate, EmployeeUpdate
from typing import Optional

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(Employee).filter(Employee.email == email).first()

def get_employees(
    db: Session, 
    skip: int = 0, 
    limit: int = 10,
    department: Optional[str] = None,
    role: Optional[str] = None
):
    query = db.query(Employee)
    
    if department:
        query = query.filter(func.lower(Employee.department) == func.lower(department))
    if role:
        query = query.filter(func.lower(Employee.role) == func.lower(role))
    
    return query.offset(skip).limit(limit).all()

def get_total_employees(
    db: Session,
    department: Optional[str] = None,
    role: Optional[str] = None
):
    query = db.query(Employee)
    
    if department:
        query = query.filter(func.lower(Employee.department) == func.lower(department))
    if role:
        query = query.filter(func.lower(Employee.role) == func.lower(role))
    
    return query.count()

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = get_employee(db, employee_id)
    if db_employee:
        update_data = employee.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return True
    return False

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()