import os
import subprocess
import sys
import time
import threading

from atlaz.headquarter.client import AtlazClient

def start_app_server():
    subprocess.run(["python", "-m", "atlaz.codeGen.backend.flask_server"])

def start_frontend_client():
    client = AtlazClient()
    client.start_frontend()

def start_full_chain():
    start_frontend_client()

def main():
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd) 
    start_full_chain()

if __name__ == "__main__":
    main()