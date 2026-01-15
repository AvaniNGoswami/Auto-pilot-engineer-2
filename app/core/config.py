from datetime import timedelta
import secrets
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:admin123@localhost:5432/autopilot_engineer")


SECRET_KEY = secrets.token_hex(32)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 300
ACCESS_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)