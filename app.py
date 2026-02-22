import os
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Game Room System API is running ✅"

@app.route("/db-test")
def db_test():
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        conn.close()
        return "Database connected successfully ✅"
    except Exception as e:
        return f"Database connection failed: {e}"
