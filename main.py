from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
from app.utils.response import process_token
from colorama import init
import warnings
from urllib3.exceptions import InsecureRequestWarning
import time
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ignore SSL warnings
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# Initialize Flask app
app = Flask(__name__)

# ===== CACHE with try-except for compatibility =====
try:
    cache = Cache(app, config={"CACHE_TYPE": "simple"})
except Exception as e:
    print(f"⚠️ Cache initialization failed: {e}")
    print("⚠️ Running without cache")
    cache = None
# ===================================================

@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "service": "M. Sarker JWT Token Generator API",
        "release": "OB54",
        "port": "2000",
        "routes": {
            "token": "/token?uid={uid}&password={password}",
            "ui": "/ui",
            "admin": "/admin",
            "health": "/health"
        },
        "developer": "M. Sarker",
        "powered_by": "Sarker"
    }), 200

@app.route("/token", methods=["GET"])
async def get_responses():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if uid and password:
        response = process_token(uid, password)
        status_code = int(response.get("status_code", 500))
        return jsonify(response), status_code
            
    return jsonify({"message": "Bulk retrieval logic has been removed."})

# ===== Routes =====

@app.route("/")
def home():
    """Home UI"""
    return render_template("index.html")

@app.route("/ui")
def ui_dashboard():
    """Responsive to UI Admin"""
    return render_template("index.html")

@app.route("/admin")
def admin_redirect():
    """Redirect UI Dashboard"""
    return render_template("index.html")

if __name__ == "__main__":
    port = 12549
    app.run(host="0.0.0.0", port=port, debug=True)