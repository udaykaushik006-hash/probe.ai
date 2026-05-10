from memory_store import load_memory

def retrieve_context(query):

    memory = load_memory()

    relevant = []

    for item in memory:
        if query.lower() in item["q"].lower():
            relevant.append(item["a"])

    return " ".join(relevant[:3]) if relevant else None