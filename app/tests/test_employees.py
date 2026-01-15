# C:\Users\saksh\Desktop\interrview\employee-management-api\app\tests\test_employees.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.auth import get_password_hash
from app.models import User


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Setup test user
def setup_test_user():
    db = TestingSessionLocal()
    existing_user = db.query(User).filter(User.username == "testuser").first()
    if not existing_user:
        test_user = User(
            username="testuser",
            hashed_password=get_password_hash("testpass123")
        )
        db.add(test_user)
        db.commit()
    db.close()

def get_auth_token():
    response = client.post("/token", params={"username": "testuser", "password": "testpass123"})
    return response.json()["access_token"]

setup_test_user()
token = get_auth_token()
headers = {"Authorization": f"Bearer {token}"}

def test_create_employee():
    response = client.post(
        "/api/employees/",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "department": "Engineering",
            "role": "Developer"
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

def test_create_duplicate_email():
    client.post(
        "/api/employees/",
        json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "department": "HR",
            "role": "Manager"
        },
        headers=headers
    )
    response = client.post(
        "/api/employees/",
        json={
            "name": "Jane Smith",
            "email": "jane@example.com",
            "department": "Sales",
            "role": "Analyst"
        },
        headers=headers
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_list_employees():
    response = client.get("/api/employees/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "employees" in data
    assert "page" in data
    assert "total" in data

def test_get_employee():
    create_response = client.post(
        "/api/employees/",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "department": "IT",
            "role": "Analyst"
        },
        headers=headers
    )
    employee_id = create_response.json()["id"]
    
    response = client.get(f"/api/employees/{employee_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_get_nonexistent_employee():
    response = client.get("/api/employees/99999", headers=headers)
    assert response.status_code == 404

def test_update_employee():
    create_response = client.post(
        "/api/employees/",
        json={
            "name": "Update Test",
            "email": "update@example.com",
            "department": "Sales",
            "role": "Manager"
        },
        headers=headers
    )
    employee_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/employees/{employee_id}",
        json={"department": "Marketing"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["department"] == "Marketing"

def test_delete_employee():
    create_response = client.post(
        "/api/employees/",
        json={
            "name": "Delete Test",
            "email": "delete@example.com",
            "department": "HR",
            "role": "Recruiter"
        },
        headers=headers
    )
    employee_id = create_response.json()["id"]
    
    response = client.delete(f"/api/employees/{employee_id}", headers=headers)
    assert response.status_code == 204

def test_filter_by_department():
    response = client.get("/api/employees/?department=Engineering", headers=headers)
    assert response.status_code == 200

def test_pagination():
    response = client.get("/api/employees/?page=1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["per_page"] == 10