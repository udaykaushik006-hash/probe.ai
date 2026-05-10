from memory_store import add_memory

def learn(query, answer):

    # store only useful responses
    if len(answer) > 30:
        add_memory({
            "q": query,
            "a": answer
        })