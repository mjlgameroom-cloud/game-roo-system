from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return "Game Room System API is running ✅"

@app.get("/health")
def health():
    return jsonify(status="ok")
