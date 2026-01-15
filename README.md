# 🏢 Employee Management API (HabotConnect Task)

A modern **RESTful API** built to manage company employees efficiently.  
This project emphasizes **clean architecture**, **secure authentication**, and **optimized data retrieval**, as required for the HabotConnect hiring task.

---

## 🚀 Key Features

### 🔐 Authentication
- Token-based **JWT authentication**
- Secures all employee-related endpoints
- Login once, access protected APIs securely

### 🧩 CRUD Operations
- Create, Read, Update, and Delete employee records
- Fully REST-compliant API design

### ✅ Data Validation
- Strong input validation using **Pydantic**
- Email format validation
- Name and role constraints enforced

### 🔍 Optimized Search & Pagination
- Filter employees by:
  - Department
  - Role
- Pagination support for large datasets

---

## 🛠️ Tech Stack

| Layer        | Technology |
|--------------|-----------|
| Framework    | FastAPI (High-performance async API) |
| ORM          | SQLAlchemy |
| Security     | Passlib (Bcrypt) + JOSE (JWT Tokens) |
| Database     | SQLite (Zero config for demo) |
| Validation   | Pydantic |

---

## 📂 Project Structure

<details>
<summary><b>Click to expand Project Structure</b></summary>

```plaintext
employee-management-api/
├── app/
│   ├── routers/        # API route definitions (employees.py)
│   ├── auth.py         # JWT & security logic
│   ├── crud.py         # Database operations (CRUD)
│   ├── database.py     # DB session & connection
│   ├── models.py       # SQLAlchemy models
│   ├── schemas.py      # Pydantic validation schemas
│   └── main.py         # Application entry point
├── .env                # Environment variables (secret keys)
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
