"""
This module reads employee data from a CSV file and asynchronously sends it to a server.
"""

import logging
import asyncio
import aiohttp
import pandas as pd

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Server URL
SERVER_URL = "http://127.0.0.1:8080/add_employee"

def load_csv(filename="employee_data.csv"):
    """
    Loads employee data from a CSV file and converts it into a list of dictionaries.

    :param filename: csv file path.
    :return: employee record.
    """
    df = pd.read_csv(filename)
    df.rename(
        columns={
            "Employee ID": "employee_id",
            "Name": "name",
            "Email": "email",
            "Department": "department",
            "Designation": "designation",
            "Salary": "salary",
            "Date of Joining": "date_of_joining",
        },
        inplace=True,
    )
    return df.to_dict(orient="records")

async def send_employee_data(session, employee):
    """
    Sends a single employee record to the server asynchronously.

    :param session: clientSession.
    :param employee: employee data.
    """
    try:
        async with session.post(SERVER_URL, json=employee) as response:
            resp_data = await response.json()
            if response.status == 201:
                logging.info("Success: %s", resp_data)
            else:
                logging.error("Failed to send: %s", resp_data)
    except Exception as exc:
        logging.error("Request failed: %s", exc)

async def main():
    """
    Reads employee data from CSV and sends each record asynchronously.
    """
    employees = load_csv("../data/employee_data.csv")
    async with aiohttp.ClientSession() as session:
        for emp in employees:
            logging.info("Processing employee: %s", emp)
        tasks = [send_employee_data(session, emp) for emp in employees]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
