import os

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

load_dotenv()

security = HTTPBasic()


def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("ADMIN_USERNAME")
    correct_password = os.getenv("ADMIN_PASSWORD")

    if not correct_username or not correct_password:
        raise ValueError("ОШИБКА: ADMIN_USERNAME или ADMIN_PASSWORD не заданы в .env файле!")
    return credentials.username
