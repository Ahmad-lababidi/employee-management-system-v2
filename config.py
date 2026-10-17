import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.getenv("DB_NAME", os.path.join(PROJECT_DIR,"db","employee.db"))

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
