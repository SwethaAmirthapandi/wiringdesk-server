from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT,
    license TEXT,
    hwid TEXT,
    line TEXT,
    status TEXT,
    time TEXT
)
""")
conn.commit()

@app.route("/")
def home():
    return "Server Running"

@app.route("/update", methods=["POST"])
def update():
    data = request.json

    cur.execute("INSERT INTO logs (barcode, license, hwid, line, status, time) VALUES (?, ?, ?, ?, ?, ?)",
                (data["barcode"], data["license"], data["hwid"], data["line"], data["status"], str(datetime.now())))
    
    conn.commit()

    return jsonify({"status": "saved"})

@app.route("/history/<barcode>")
def history(barcode):
    cur.execute("SELECT * FROM logs WHERE barcode=? ORDER BY time DESC", (barcode,))
    rows = cur.fetchall()
    return jsonify({"data": rows})

app.run(host="0.0.0.0", port=5000)