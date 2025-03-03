"""
This module provides an asynchronous employee management system.
"""

import logging
from aiohttp import web
import aiomysql
from pydantic import BaseModel, EmailStr, conint
from datetime import date

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "db": "employee_mgmts"
}

class EmployeeModel(BaseModel):
    """
    Pydantic model for validating employee data.
    """
    employee_id: conint(ge=1)
    name: str
    email: EmailStr
    department: str
    designation: str
    salary: conint(ge=0)
    date_of_joining: date  # Ensures valid date format (YYYY-MM-DD)

def log_request(func):
    """
    Decorator to log HTTP requests.
    """
    async def wrapper(request):
        logging.info("Request received: %s %s", request.method, request.path)
        return await func(request)
    return wrapper

def validate_data(func):
    """
    Decorator to validate JSON request data using Pydantic.
    """
    async def wrapper(request):
        try:
            data = await request.json()
            validated_data = EmployeeModel(**data).dict()  # Validate data
            request["validated_data"] = validated_data  # Store validated data in request
            return await func(request)
        except Exception as e:
            return web.json_response({"error": f"Invalid data: {str(e)}"}, status=400)

    return wrapper

async def create_database():
    """
    Creates the database and table if they do not exist.
    """
    logging.info("Creating DB..")
    conn = await aiomysql.connect(host=DB_CONFIG["host"], password=DB_CONFIG["password"],
                                  user=DB_CONFIG["user"])
    async with conn.cursor() as curr:
        await curr.execute("CREATE DATABASE IF NOT EXISTS employee_mgmts;")
        await curr.execute("USE employee_mgmts;")
        await curr.execute("""
            CREATE TABLE IF NOT EXISTS employees (
            employee_id INT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            department VARCHAR(50),
            designation VARCHAR(50),
            salary INT,
            date_of_joining DATE
            );
        """)
        await conn.commit()
    conn.close()
    logging.info("Database setup complete!")

async def init_db():
    """
    Initializes the database connection.
    """
    await create_database()
    return await aiomysql.create_pool(**DB_CONFIG, minsize=1, maxsize=5)

@log_request
@validate_data
async def add_employee(request):
    """
    Handles HTTP POST requests to add a new employee to the database.
    """
    data = request["validated_data"]  # Use validated data
    async with request.app["db_pool"].acquire() as conn:
        async with conn.cursor() as curr:
            sql = """
            INSERT INTO employees 
            (employee_id, name, email, department, designation, salary, date_of_joining) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            """
            try:
                await curr.execute(sql, (
                    data["employee_id"], data["name"], data["email"],
                    data["department"], data["designation"],
                    data["salary"], data["date_of_joining"]
                ))
                await conn.commit()
                return web.json_response({"message": "Employee added successfully"}, status=201)
            except aiomysql.IntegrityError:
                return web.json_response({"employee_id": data["employee_id"],
                                          "error": "Duplicate employee_id or email"}, status=400)

async def create_app():
    """
    Creates and configures the application.
    """
    app = web.Application()
    app["db_pool"] = await init_db()
    app.router.add_post("/add_employee", add_employee)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)
