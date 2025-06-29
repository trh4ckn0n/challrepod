from flask import Flask, request, jsonify, render_template, abort
from datetime import datetime
import logging
import base64
import os
import sqlite3
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

DB_PATH = "beacons.db"
FLAG = "FLAG{dns_trafic_detected_correctly}"

# --- INIT DB ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS beacons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- LOGGER ---
logging.basicConfig(
    filename='beacons.log',
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- UTILS ---
def xor_encode(text, key='X'):
    return ''.join(chr(ord(c) ^ ord(key)) for c in text)

def rot13(text):
    return text.translate(str.maketrans(
        'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
        'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm'))

# --- ROUTES ---
@app.route("/")
def index():
    return render_template("index.html")

from flask import request

ADMIN_PASSWORD = "trhackadmin"

@app.route("/admin", methods=["GET"])
def admin():
    if request.args.get("auth") != ADMIN_PASSWORD:
        abort(403)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ip, user, timestamp FROM beacons ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template("admin.html", beacons=rows)

@app.route("/beacons", methods=["GET"])
def view_beacons():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ip, user, timestamp FROM beacons ORDER BY timestamp DESC")
    beacons = cursor.fetchall()
    conn.close()
    return render_template("beacons.html", beacons=beacons)

@app.route("/static/hidden.js")
def trap():
    return app.send_static_file("/static/hidden.js")


@app.route("/trap.js")
def trap():
    return app.send_static_file("trap.js")

@app.route("/redir")
def redir():
    return render_template("redir.html")

@app.route("/ping", methods=["POST"])
def ping():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    data = request.get_json()
    user = data.get("user", "unknown")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO beacons (ip, user, timestamp) VALUES (?, ?, ?)", (ip, user, timestamp))
    conn.commit()
    conn.close()

    log_message = f"[{timestamp}] Beacon reçu de {ip} (user: {user})"
    print(log_message)
    with open("beacons.log", "a") as f:
        f.write(log_message + "\n")

    return jsonify({"status": "ok"})
    
@app.route("/flag", methods=["GET"])
def get_flag():
    encoded_flag = base64.b64encode(rot13(xor_encode(FLAG)).encode()).decode()
    return jsonify({"encoded": encoded_flag, "hint": "base64 -> xor -> rot13"})

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    candidate = data.get("flag", "")
    decoded = xor_encode(rot13(candidate))
    if decoded == FLAG:
        return jsonify({"result": "✅ Correct!"})
    return jsonify({"result": "❌ Incorrect."})

@app.route("/backup.zip", methods=["GET"])
def fake_backup():
    return "This file is encrypted. 🔒", 401

@app.route("/admin_fake", methods=["GET"])
def fake_admin():
    abort(403)

@app.route("/logs")
def view_logs():
    with open("beacons.log", "r") as f:
        content = f.read()
    return f"<pre style='background:black;color:lime;padding:1em;font-family:monospace'>{content}</pre>"



@app.errorhandler(403)
def forbidden(e):
    return "<h1>403 - Access Denied</h1>", 403

@app.errorhandler(404)
def not_found(e):
    return "404 Not Found", 404

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
