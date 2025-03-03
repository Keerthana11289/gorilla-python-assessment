## Employee Management System

This is a client-server application that processes employee records from a CSV file and stores them in a MySQL database. The client reads the CSV, sends employee data to the server, and the server validates and stores it asynchronously.

### Features
- Asynchronous client-server application
- MySQL database handling with aiomysql
- Input validation using Pydantic
- Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL Server running
- pip upgrade (python -m pip install --upgrade pip)

### Installation
- Extract the project folder to your location
- Open Command Prompt (cmd) and navigate to the project folder
- cd gorilla-python-assessment
- Create a virtual environment
 `python -m venv venv`
`venv\Scripts\activate`
- Install dependencies `pip install -r requirements.txt`

### Running the Application
- Start the Server
`python gorilla-python-assessment\server\server.py`
- Run the Client
`python gorilla-python-assessment\client\client.py`
- Check MySQL DB for records

### Formatting
Run `pylint <file>` 

### Configuration
CSV Employee Data: Place the file in data\employee_data.csv

### Demo
Refer the demo vide to know how the application works gorilla-python-assessment\Demo\