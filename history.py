import json
import os

FILE = "history.json"

def load_history():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)