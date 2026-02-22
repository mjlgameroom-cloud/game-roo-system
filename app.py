import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Game Room System API is running ✅"

@app.route("/init-db")
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    return "Database initialized ✅"

@app.route("/create-admin")
def create_admin():
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            ("admin", "1234", "admin")
        )
        conn.commit()
    except:
        pass
    cur.close()
    conn.close()
    return "Admin ready ✅"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, role FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "user_id": user[0],
            "role": user[1]
        })
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
