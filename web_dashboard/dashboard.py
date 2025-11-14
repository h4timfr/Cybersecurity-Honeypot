from flask import Flask, render_template, jsonify
import json, os
from datetime import datetime
from collections import Counter

app = Flask(__name__)

LOG_FOLDER = "../honeypot_logs"


def load_latest_log():
    if not os.path.exists(LOG_FOLDER):
        return None

    files = [
        f for f in os.listdir(LOG_FOLDER)
        if f.startswith("honeypot_") and f.endswith(".json")
    ]
    if not files:
        return None

    newest = max(files, key=lambda x: os.path.getmtime(os.path.join(LOG_FOLDER, x)))
    return os.path.join(LOG_FOLDER, newest)


def load_logs():
    path = load_latest_log()
    if not path:
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []


# ------------------ ATTACK CATEGORY CLASSIFIER ------------------

def categorize_payload(payload: str):
    p = payload.lower()

    if "user" in p:
        return "Username Attempts"
    if "pass" in p:
        return "Password Attempts"
    if "get" in p or "post" in p:
        return "Web Requests"
    if "ssh" in p:
        return "SSH Probe"
    return "Other"


# ------------------ IP INTELLIGENCE ------------------

def compute_ip_details(ip, logs):
    ip_logs = [l for l in logs if l["remote_ip"] == ip]

    if not ip_logs:
        return {}

    timestamps = [
        datetime.strptime(l["timestamp"], "%Y-%m-%d %H:%M:%S")
        for l in ip_logs
    ]

    first_seen = min(timestamps).strftime("%Y-%m-%d %H:%M:%S")
    last_seen = max(timestamps).strftime("%Y-%m-%d %H:%M:%S")

    ports = list({str(l["port"]) for l in ip_logs})
    payloads = [l["data"][:40] for l in ip_logs][:5]

    score = (
        (len(ip_logs) // 5) +
        len(ports) +
        min(5, len(payloads))
    )
    score = min(score, 10)

    if score >= 7:
        risk = "High Risk"
    elif score >= 4:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return {
        "ip": ip,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "total_hits": len(ip_logs),
        "ports": ports,
        "payloads": payloads,
        "score": score,
        "risk": risk
    }


# ------------------ ROUTES ------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    logs = load_logs()

    total = len(logs)
    unique_ips = len({l["remote_ip"] for l in logs}) if logs else 0

    # Port Distribution
    port_count = Counter(str(l["port"]) for l in logs)

    most_targeted = max(port_count, key=port_count.get) if port_count else "N/A"

    # Attack Categories
    categories = Counter(categorize_payload(l["data"]) for l in logs)

    return jsonify({
        "summary": {
            "total": total,
            "unique_ips": unique_ips,
            "most_targeted": most_targeted
        },
        "logs": logs[-20:],          # last 20 logs
        "graph_categories": dict(categories),
        "graph_port": dict(port_count)
    })


@app.route("/ipinfo/<ip>")
def ipinfo(ip):
    logs = load_logs()
    return jsonify(compute_ip_details(ip, logs))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
