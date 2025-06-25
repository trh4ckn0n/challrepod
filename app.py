from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/ping", methods=["POST"])
def ping():
    data = request.get_json()
    print(f"[+] Beacon reçu de {request.remote_addr} à {datetime.now()}: {data}")
    return {"status": "received"}, 200

@app.route("/", methods=["GET"])
def reveal_flag():
    return "FLAG{dns_trafic_detected_correctly}"
