from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import logging
from config import DB_NAME

logging.basicConfig(level=logging.INFO)

app = FastAPI()

class Employee(BaseModel):
    name: str
    department: str
    salary: float
    hire_date: str

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    from db.database import init_db
    init_db()

@app.get("/")
def read_root():
    return {"message": "Employee API is running. Navigate to /docs to view the interface."}


@app.get("/employees")
def get_employees():
    try:
        conn = get_db_connection()
        employees = conn.execute("SELECT * FROM employees").fetchall()
        conn.close()
        return [dict(ix) for ix in employees]
    except Exception as e:
        logging.error(f"Error fetching employees: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    try:
        conn = get_db_connection()
        emp = conn.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,)).fetchone()
        conn.close()
        if emp is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return dict(emp)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching employee: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/employees")
def add_employee(emp: Employee):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
            (emp.name, emp.department, emp.salary, emp.hire_date)
        )
        conn.commit()
        conn.close()
        return {"message": "Employee added successfully"}
    except Exception as e:
        logging.error(f"Error adding employee: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, emp: Employee):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employees SET name=?, department=?, salary=?, hire_date=? WHERE employee_id=?",
            (emp.name, emp.department, emp.salary, emp.hire_date, employee_id)
        )
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Employee not found")
        conn.commit()
        conn.close()
        return {"message": "Employee updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating employee: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Employee not found")
        conn.commit()
        conn.close()
        return {"message": "Employee deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting employee: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
