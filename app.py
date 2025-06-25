from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import logging
import base64
import os

app = Flask(__name__)

# Logger dans un fichier
logging.basicConfig(
    filename='beacons.log',
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Flag stocké côté serveur (non visible directement)
FLAG = "FLAG{dns_trafic_detected_correctly}"

@app.route("/ping", methods=["POST"])
def ping():
    data = request.get_json()
    ip = request.remote_addr

    # Log en fichier
    logging.info(f"Beacon de {ip} : {data}")

    return jsonify({"status": "received"}), 200


@app.route("/", methods=["GET"])
def index():
    # Page HTML mystérieuse
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Nothing to see here</title>
          <style>
            body {
              background-color: #0a0a0a;
              color: #333;
              font-family: monospace;
              display: flex;
              align-items: center;
              justify-content: center;
              height: 100vh;
              flex-direction: column;
            }
            .hidden {
              color: #0a0a0a;
              user-select: none;
            }
            .glow {
              text-shadow: 0 0 5px #00ffcc;
            }
          </style>
        </head>
        <body>
          <h1 class="glow">403 :: Forbidden</h1>
          <p>This endpoint is restricted.</p>
          <div class="hidden"> <!-- Flag encodé base64 dans le DOM -->
            {{ hidden_flag }}
          </div>
        </body>
        </html>
    """, hidden_flag=base64.b64encode(FLAG.encode()).decode())

@app.route("/flag", methods=["GET"])
def reveal_flag():
    # Expose clairement le flag, mais route inconnue du frontend
    return jsonify({
        "flag": FLAG,
        "hint": "you were not supposed to find this endpoint easily..."
    }), 200


@app.errorhandler(404)
def not_found(e):
    return "404 Not Found", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
