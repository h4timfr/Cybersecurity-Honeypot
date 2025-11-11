import socket
import sys
import datetime
import json
import time
import threading
from pathlib import Path

# Configure logging directory
LOG_DIR = Path("honeypot_logs")
LOG_DIR.mkdir(exist_ok=True)

class Honeypot:
    def __init__(self, bind_ip="0.0.0.0", ports=None):
        self.bind_ip = bind_ip
        self.ports = ports or [2121, 2222, 8080, 8443]  # Default ports to monitor
        self.active_connections = {}
        self.log_file = LOG_DIR / f"honeypot_{datetime.datetime.now().strftime('%Y%m%d')}.json"

    def log_activity(self, port, remote_ip, data):
        """Log suspicious activity as a proper JSON array with commas"""
        activity = {
            "timestamp": datetime.datetime.now().isoformat(),
            "remote_ip": remote_ip,
            "port": port,
            "data": data.decode('utf-8', errors='ignore')
        }

        # If file doesn't exist or is empty, start a JSON array
        if not self.log_file.exists() or self.log_file.stat().st_size == 0:
            with open(self.log_file, 'w') as f:
                json.dump([activity], f, indent=4)
        else:
            # Read existing JSON array, append new activity, rewrite file
            with open(self.log_file, 'r+') as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
                logs.append(activity)
                f.seek(0)
                json.dump(logs, f, indent=4)
                f.truncate()

    def handle_connection(self, client_socket, remote_ip, port):
        """Handle individual connections and emulate services"""
        service_banners = {
            21: "220 FTP server ready\r\n",
            22: "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n",
            80: "HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\n\r\n",
            443: "HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\n\r\n"
        }

        try:
            # Send appropriate banner for the service
            if port in service_banners:
                client_socket.send(service_banners[port].encode())

            # Receive data from attacker
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                self.log_activity(port, remote_ip, data)

                # Send fake response
                client_socket.send(b"Command not recognized.\r\n")

        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            client_socket.close()

    def start_listener(self, port):
        """Start a listener on specified port"""
        try:
            #Creates a new TCP socket (IPv4).
            #AF_INET → IPv4
            #SOCK_STREAM → TCP
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.bind_ip, port))
            server.listen(5)

            print(f"[*] Listening on {self.bind_ip}:{port}")

            while True:
                
                client, addr = server.accept()
                #client → a new socket object representing the connection with that remote host
                #addr → a tuple (IP, port) of the remote host
                print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

                # Handle connection in separate thread
                #So the listener can immediately go back to accept() without waiting for the current client to finish.
                client_handler = threading.Thread(
                    target=self.handle_connection,
                    args=(client, addr[0], port)
                )
                client_handler.start() #runs it in the new thread

        except Exception as e:
            print(f"Error starting listener on port {port}: {e}")


def main():
    honeypot = Honeypot()

    # Start listeners for each port in separate threads
    for port in honeypot.ports:
        listener_thread = threading.Thread(
            target=honeypot.start_listener,
            args=(port,)
        )
        listener_thread.daemon = True #if main program exits, these threads will automatically close
        listener_thread.start()

    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down honeypot...")
        sys.exit(0)

if __name__ == "__main__":
    main()
