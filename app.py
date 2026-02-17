"""
NutriPlan – Flask backend
Uruchomienie lokalne:
    pip3 install flask gunicorn
    python3 app.py

Otwórz na laptopie:  http://localhost:5001
Otwórz na telefonie: http://<IP_LAPTOPA>:5001   (ta sama sieć WiFi)
"""

import json
import os
import socket
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Na Railway dane są w /tmp (jedyny katalog z prawem zapisu na read-only FS)
# Lokalnie używamy katalogu projektu
if os.environ.get("RAILWAY_ENVIRONMENT"):
    DATA_FILE = "/tmp/data.json"
else:
    DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# Plik źródłowy z przepisami (tylko do odczytu — zawsze w repo)
SOURCE_DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# ── Domyślna struktura danych ─────────────────────────────
DEFAULT_DATA = {
    "recipes": [],
    "weekPlans": {},
    "trainingDays": {},
    "savedPlans": {}
}


def load_data():
    # Na Railway: jeśli /tmp/data.json nie istnieje, skopiuj z repo
    if os.environ.get("RAILWAY_ENVIRONMENT") and not os.path.exists(DATA_FILE):
        if os.path.exists(SOURCE_DATA_FILE):
            with open(SOURCE_DATA_FILE, "r", encoding="utf-8") as src:
                initial = json.load(src)
            save_data(initial)
            return initial
        return DEFAULT_DATA

    target = DATA_FILE
    if not os.path.exists(target):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    with open(target, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_DATA


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Strona główna ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── API: pobierz wszystkie dane ───────────────────────────
@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(load_data())


# ── API: zapisz wszystkie dane ────────────────────────────
@app.route("/api/data", methods=["POST"])
def post_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Brak danych"}), 400
    for key in ["recipes", "weekPlans", "trainingDays"]:
        if key not in data:
            return jsonify({"error": f"Brak klucza: {key}"}), 400
    save_data(data)
    return jsonify({"ok": True})


# ── Pomocnicza funkcja: znajdź lokalny IP ─────────────────
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    ip = get_local_ip()
    print("\n" + "═" * 52)
    print("  🥗  NutriPlan uruchomiony!")
    print("═" * 52)
    print(f"  💻  Laptop:   http://localhost:{port}")
    print(f"  📱  Telefon:  http://{ip}:{port}")
    print(f"       (telefon musi być w tej samej sieci WiFi)")
    print("═" * 52)
    print("  Aby zatrzymać: Ctrl+C")
    print("═" * 52 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False)
