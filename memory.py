import json

FILE = "memory.json"

def save_memory(q, a):
    try:
        data = load_memory()
        data[q] = a

        with open(FILE, "w") as f:
            json.dump(data, f)
    except:
        pass


def load_memory():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def recall_memory(query):
    data = load_memory()
    for k in data:
        if query in k:
            return data[k]
    return None