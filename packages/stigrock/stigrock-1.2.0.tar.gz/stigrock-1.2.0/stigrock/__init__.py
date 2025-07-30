#!/usr/bin/env python3

import os
import sys
import time
import socket
import subprocess
from pyngrok import ngrok
from threading import Thread
from pathlib import Path
from dotenv import load_dotenv

# === CONFIG ===
PROJECT_DIR = Path("stiprog")
PORT = 8080

# === LOAD .env IF EXISTS ===
load_dotenv()
NGROK_TOKEN = os.getenv("NGROK_AUTHTOKEN")

# === PRINT BANNER ===
def print_ascii_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(r"""
███████╗████████╗██╗ ██████╗ ██████╗  ██████╗  ██████╗  ██████╗  ██████╗██╗  ██╗
██╔════╝╚══██╔══╝██║██╔═══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██║ ██╔╝
███████╗   ██║   ██║██║   ██║██████╔╝██║   ██║██║  ███╗██║  ███╗██║     █████╔╝ 
╚════██║   ██║   ██║██║   ██║██╔═══╝ ██║   ██║██║   ██║██║   ██║██║     ██╔═██╗ 
███████║   ██║   ██║╚██████╔╝██║     ╚██████╔╝╚██████╔╝╚██████╔╝╚██████╗██║  ██╗
╚══════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝      ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝
""")

# === PORT CHECK ===
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# === START SERVER ===
def start_http_server():
    try:
        os.chdir(PROJECT_DIR)
        subprocess.run(["python3" if os.name != "nt" else "python", "-m", "http.server", str(PORT)])
    except Exception as e:
        print(f"Errore nell’avvio del server: {e}")

# === START NGROK ===
def start_ngrok_tunnel():
    public_url = ngrok.connect(PORT, bind_tls=True)
    print("\n✅ Stigrock è online!")
    print(f"🌍 URL pubblico: {public_url}")
    print("📁 Servendo contenuti da: stiprog/")
    print("📡 Porta locale:", PORT)
    print("➡ Apri il link per vedere il sito!\n")
    return public_url

# === MAIN FUNCTION ===
def main():
    print_ascii_banner()

    if not PROJECT_DIR.exists():
        print(f"❌ Errore: cartella '{PROJECT_DIR}' non trovata.")
        sys.exit(1)

    # --- Edit options ---
    print("Vuoi modificare i file prima dell’avvio?")
    print("1 - Modifica index.html")
    print("2 - Modifica style.css")
    print("3 - Modifica entrambi")
    print("4 - Continua senza modifiche")
    choice = input("Scelta: ")

    def edit_file(filepath):
        editor = os.getenv("EDITOR") or ("notepad" if os.name == "nt" else "nano")
        subprocess.run([editor, str(PROJECT_DIR / filepath)])

    if choice == "1":
        edit_file("index.html")
    elif choice == "2":
        edit_file("style.css")
    elif choice == "3":
        edit_file("index.html")
        edit_file("style.css")
    else:
        print("✅ Nessuna modifica eseguita.\n")

    # --- Ngrok token ---
    global NGROK_TOKEN
    if not NGROK_TOKEN:
        NGROK_TOKEN = input("Inserisci la tua chiave Ngrok: ")
    ngrok.set_auth_token(NGROK_TOKEN)

    # --- Porta già occupata? ---
    if is_port_in_use(PORT):
        print(f"❌ ERRORE: La porta {PORT} è già in uso. Chiudi il processo e riprova.")
        sys.exit(1)

    # --- Avvio server ---
    print("Avvio server HTTP...")
    server_thread = Thread(target=start_http_server, daemon=True)
    server_thread.start()
    time.sleep(2)

    print("Avvio tunnel Ngrok...\n")
    try:
        start_ngrok_tunnel()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔴 Interruzione manuale. Chiusura...")
        ngrok.kill()

# === ENTRY POINT ===
if __name__ == "__main__":
    main()
