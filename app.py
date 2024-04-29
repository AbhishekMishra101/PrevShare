#!/usr/bin/env python

from flask import render_template, Flask, render_template, redirect, url_for, request, jsonify, send_file
import tkinter as tk
from tkinter import filedialog
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import csv
import threading
import requests
import io
import base64

# Initialize Flask app
app = Flask(__name__)
server_files = []

# Define AES encryption and decryption functions
def encrypt_file(file, key):
    data = file.read()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, cipher.nonce

def decrypt_file(encrypted_data, key, nonce):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt(encrypted_data)
    return data
    
@app.route("/")
def index():
    return render_template("index.html", files=server_files)
    
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files['file']
    if file:
        print(type(file))
        if file not in server_files:
            # Generate a random key
            key = get_random_bytes(16)
            # Encrypt the file
            encrypted_data, nonce = encrypt_file(file, key)
            # Convert bytes to base64 string for JSON serialization
            encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
            key_b64 = base64.b64encode(key).decode('utf-8')
            nonce_b64 = base64.b64encode(nonce).decode('utf-8')
            file_info = {"file_name": file.filename, "encrypted_data": encrypted_data_b64, "key": key_b64, "nonce": nonce_b64}
            server_files.append(file_info)
            return jsonify({"message": "File uploaded successfully"})
        else:
            return jsonify({"error": "File already exists"}), 400
    else:
        return jsonify({"error": "File already exists"}), 400

@app.route("/files", methods=["GET"])
def get_files():
    return jsonify(server_files)

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    for file_info in server_files:
        if file_info["file_name"] == filename:
            # Decode base64 strings to bytes
            encrypted_data = base64.b64decode(file_info["encrypted_data"])
            key = base64.b64decode(file_info["key"])
            nonce = base64.b64decode(file_info["nonce"])
            # Decrypt the file
            decrypted_data = decrypt_file(encrypted_data, key, nonce)
            # Return the decrypted file as attachment
            return send_file(io.BytesIO(decrypted_data), as_attachment=True, download_name=filename)
    return jsonify({"error": "File not found"}), 404

# Initialize the GUI application
class DataSharingApp:
    def __init__(self, master):
        self.master = master
        master.title("Secure Data Sharing App")

        self.label = tk.Label(master, text="Welcome to Secure Data Sharing App")
        self.label.pack()

        self.upload_button = tk.Button(master, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.file_listbox = tk.Listbox(master)
        self.file_listbox.pack()

        self.download_button = tk.Button(master, text="Download File", command=self.download_file)
        self.download_button.pack()

        self.refresh_button = tk.Button(master, text="Refresh", command=self.refresh_files)
        self.refresh_button.pack()

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            file_name = file_path.split("/")[-1]
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = io.StringIO()
                writer = csv.writer(data)
                writer.writerows(reader)
                files = {'file': data.getvalue().encode()}
                response = requests.post("http://127.0.0.1:5000/upload", files=files)
                if response.status_code == 200:
                    print("File uploaded successfully")
                else:
                    print("Failed to upload file")

    def download_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            response = requests.get(f"http://127.0.0.1:5000/download/{selected_file}")
            if response.status_code == 200:
                with open(selected_file, 'wb') as file:
                    file.write(response.content)
                print("File downloaded successfully")
            else:
                print("Failed to download file")

    def refresh_files(self):
        response = requests.get("http://127.0.0.1:5000/files")
        if response.status_code == 200:
            server_files = response.json()
            self.file_listbox.delete(0, tk.END)
            for file_info in server_files:
                self.file_listbox.insert(tk.END, file_info["file_name"])

# Start Flask server
if __name__ == "__main__":
    # Start Flask server in the main thread
    threading.Thread(target=app.run, kwargs={'debug': True, 'threaded': True, 'use_reloader': False}).start()
    # Create the GUI application window
    root = tk.Tk()
    app = DataSharingApp(root)
    root.mainloop()