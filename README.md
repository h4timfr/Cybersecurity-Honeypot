🛡 Cybersecurity Honeypot System

A lightweight, extensible Python-based honeypot for educational and research use.
This system captures attacker activity, simulates threat behavior, analyzes logs, and visualizes attacks using a modern SOC-style web dashboard.

🚀 Project Overview

This project implements a complete, modular honeypot platform consisting of:

✅ 1. Multi-Port Honeypot Listener (main.py)

Emulates commonly targeted network services and logs all attacker interactions.

✅ 2. Attack Simulator (honeypot_simulator.py)

Generates realistic cyberattacks for testing the honeypot safely.

✅ 3. Log Analyzer (analyze_logs.py)

Extracts intelligence such as attacker behavior, port usage, payload frequency, and sophistication scores.

✅ 4. Real-Time SOC Dashboard (web_dashboard/)

Flask + Chart.js web interface that displays live attack stats, recent logs, port distribution, and behavioral charts.

This system is built for learning, demonstration, research, and academic presentations.

✨ Features
🔥 Honeypot Listener

Emulates ports: 2121 (FTP), 2222 (SSH), 8080 (HTTP), 8443 (HTTPS)

Logs every connection with:

Timestamp

Remote IP

Port targeted

Payload/command

Stores logs as JSON in honeypot_logs/

⚔️ Attack Simulator

Simulates realistic attacks including:

Port scanning

Brute-force attempts

FTP/SSH command injections

HTTP payloads

Multiple threads & velocity based on intensity level

Run safely — no external attackers needed.

📊 Advanced Log Analyzer

Outputs:

Top attacker IPs

Most targeted ports

Hourly attack distribution

Payload frequencies

Sophistication analysis

Timeline of attack attempts

🖥 SOC Web Dashboard

Built using Flask + Bootstrap + Chart.js

Displays:

Total attacks

Unique IP addresses

Most targeted ports

Recent attack logs

Line chart: attacks over time

Pie chart: port distribution

Auto-refresh every 3 seconds.

Directory:

web_dashboard/
 ├── dashboard.py
 └── templates/
      └── index.html

📁 Project Structure
Cybersecurity-Honeypot/
│
├── main.py                       # Honeypot server listener
├── honeypot_simulator.py         # Attack generator
├── analyze_logs.py               # Log analyzer
│
├── honeypot_logs/                # Stored JSON logs
│
├── web_dashboard/
│     ├── dashboard.py            # Flask backend
│     └── templates/
│            └── index.html       # SOC Dashboard UI
│
├── README.md
└── requirements.txt (optional)

⚙️ Setup
1️⃣ Install Python

Python 3.10+ recommended.

2️⃣ Install dependencies

Only Flask + chart rendering requires installs:

pip install flask


Everything else uses Python built-ins.

🧪 How to Run the Project
1. Start the Honeypot Listener
python main.py


It will start simulated services on:

Service	Port
FTP	2121
SSH	2222
HTTP	8080
HTTPS	8443

Logs will appear in:

honeypot_logs/honeypot_YYYYMMDD.json

2. Run the Attack Simulator
python honeypot_simulator.py --target 127.0.0.1 --intensity medium --duration 60

Flags:
Flag	Meaning
--target	IP of honeypot
--intensity	low / medium / high
--duration	seconds
3. Run the Log Analyzer
python analyze_logs.py honeypot_logs/honeypot_YYYYMMDD.json


Outputs structured terminal report.

4. Start the SOC Web Dashboard

Navigate into folder:

cd web_dashboard
python dashboard.py


Visit:

http://127.0.0.1:5000


You will see:

Attack charts

Live updates

Port distribution

Recent logs list

🔍 Use Cases

Academic project

Cybersecurity demonstrations

SOC training

Log analysis research

Detecting attacker behavior patterns

🔒 Safety Notes

This honeypot is local-only by design

No risk of exposing system to real hackers

Attack simulator replaces real threat actors

Safe for student and classroom use
