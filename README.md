🛡️ Honeypot Project
====================

This Python project creates a honeypot that emulates multiple services like FTP, SSH, and HTTP to capture and log suspicious activity. It also includes a simulator to generate attacks and a log analyzer to extract insights from the activity.

✨ Features
----------

*   Listens on common ports (21, 22, 80, 443) to emulate services
    
*   Logs all incoming connections, payloads, timestamps, and remote IPs in JSON format
    
*   Attack simulator to test the honeypot with port scans and brute force attacks
    
*   Advanced log analysis providing:
    
    *   Most active IPs 🌐
        
    *   Port targeting statistics 🔢
        
    *   Hourly attack patterns ⏰
        
    *   Payload patterns and attacker sophistication 🕵️
        

⚙️ Setup
--------

1.  Make sure Python 3.x is installed
    
2.  Place all three scripts (main.py, honeypot\_simulator.py, analyze\_logs.py) in the same folder
    
3.  No extra libraries needed, all are standard Python modules
    

🚀 How to Run
-------------

1️⃣ Start the honeypot server:

`   python main.py   `

The honeypot will start listening on the configured ports and log all activity in a JSON file like honeypot\_YYYYMMDD.json in the same folder

2️⃣ Run the attack simulator:

`   python honeypot_simulator.py --target 127.0.0.1 --intensity medium --duration 300   `

*   \--target : IP of the honeypot (default 127.0.0.1)
    
*   \--intensity : Attack intensity (low, medium, high)
    
*   \--duration : Duration of simulation in seconds
    

3️⃣ Analyze the logs:

`   python analyze_logs.py honeypot_YYYYMMDD.json   `

Replace YYYYMMDD with the date of your log file. The analysis will show:

*   Top attacker IPs 🌐
    
*   Port targeting and unique payloads 🔢
    
*   Hourly attack distribution ⏰
    
*   Attacker sophistication 🕵️
    
*   Most common payload patterns 💻
    

📝 Notes
--------

*   The honeypot is safe to run locally
    
*   Always start main.py first before running the simulator
    
*   Logs are saved in JSON format in the same folder for easy analysis
    