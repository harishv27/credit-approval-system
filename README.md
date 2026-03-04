# Credit Approval System

## Overview

The **Credit Approval System** is a backend service built using Django and Django REST Framework to evaluate customer loan eligibility and manage loan records.
It provides APIs to register customers, check loan eligibility, create loans, and view loan details.

The system runs fully containerized using Docker and uses PostgreSQL as the database and Celery with Redis for background tasks.

---

## Tech Stack

* Python 3.11
* Django 4.2
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker & Docker Compose

---

## System Architecture

Client → Django REST API → PostgreSQL Database
↘
Celery Worker → Redis Queue

---

## Features

* Customer Registration
* Loan Eligibility Check
* Loan Creation
* View Customer Loans
* View Loan Details
* EMI Calculation
* Credit Limit Calculation
* Background Data Loading using Celery

---

## Project Structure

```
credit_approval_system/
│
├── config/                 # Django project configuration
│
├── core/                   # Celery tasks and utility functions
│
├── customers/              # Customer model and APIs
│
├── loans/                  # Loan model and APIs
│
├── data/                   # CSV files for initial dataset
│
├── docker-compose.yml      # Docker services configuration
├── Dockerfile              # Docker build configuration
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
└── README.md               # Project documentation
```

---

## Setup Instructions

### 1. Clone the repository

```
git clone <repository_url>
cd credit_approval_system
```

### 2. Build Docker containers

```
docker compose up --build
```

### 3. Run migrations

Open another terminal and run:

```
docker compose exec web python manage.py migrate
```

### 4. Access the API

Server will run at:

```
http://localhost:8000
```

---

## API Endpoints

### 1. Register Customer

POST `/api/register/`

Request:

```
{
  "first_name": "Aaron",
  "last_name": "Garcia",
  "age": 63,
  "monthly_income": 50000,
  "phone_number": "9629317944"
}
```

Response:

```
{
  "customer_id": 1,
  "first_name": "Aaron",
  "last_name": "Garcia",
  "age": 63,
  "phone_number": "9629317944",
  "monthly_salary": 50000,
  "approved_limit": 1800000
}
```

---

### 2. Check Loan Eligibility

POST `/api/check-eligibility/`

Request:

```
{
  "customer_id": 1,
  "loan_amount": 500000,
  "interest_rate": 10,
  "tenure": 12
}
```

Response:

```
{
  "customer_id": 1,
  "approval": false,
  "interest_rate": 10.0,
  "corrected_interest_rate": 12,
  "tenure": 12,
  "monthly_installment": 44424.39
}
```

---

### 3. Create Loan

POST `/api/create-loan/`

Request:

```
{
  "customer_id": 1,
  "loan_amount": 500000,
  "interest_rate": 12,
  "tenure": 12
}
```

Response:

```
{
  "loan_id": 1,
  "customer_id": 1,
  "loan_approved": true,
  "monthly_installment": 44424.39
}
```

---

### 4. View Customer Loans

GET `/api/view-loans/{customer_id}`

Example:

```
GET /api/view-loans/1
```

Response:

```
[
  {
    "loan_id": 1,
    "loan_amount": 500000,
    "interest_rate": 12,
    "monthly_installment": 44424.39,
    "repayments_left": 12
  }
]
```

---

### 5. View Loan Details

GET `/api/view-loan/{loan_id}`

Example:

```
GET /api/view-loan/1
```

---

## Business Logic

### Approved Credit Limit

```
Approved Limit = 36 × Monthly Salary
```

### EMI Calculation

```
EMI = [P × r × (1+r)^n] / [(1+r)^n − 1]
```

Where:

* P = Loan Amount
* r = Monthly Interest Rate
* n = Number of Months

---

## Docker Services

| Service | Description          |
| ------- | -------------------- |
| web     | Django application   |
| db      | PostgreSQL database  |
| redis   | Redis message broker |
| celery  | Celery worker        |

---

## Running Containers

Start system:

```
docker compose up --build
```

Stop system:

```
docker compose down
```

Run migrations:

```
docker compose exec web python manage.py migrate
```

---

## Author

Harish V
M.Sc AI & ML
Vellore Institute of Technology
