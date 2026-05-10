import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


# ----------------------------------------
# DUCKDUCKGO
# ----------------------------------------
def search_duckduckgo(query):

    try:

        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        data = requests.get(url, timeout=8).json()

        if data.get("Abstract"):
            return data["Abstract"]

        if data.get("RelatedTopics"):

            topics = data["RelatedTopics"]

            if len(topics) > 0 and "Text" in topics[0]:

                return topics[0]["Text"]

    except:
        pass

    return None


# ----------------------------------------
# WIKIPEDIA
# ----------------------------------------
def search_wikipedia(query):

    try:

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(query)}"

        data = requests.get(url, timeout=8).json()

        if data.get("extract"):

            return data["extract"]

    except:
        pass

    return None


# ----------------------------------------
# GEEKSFORGEEKS SEARCH
# ----------------------------------------
def search_geeksforgeeks(query):

    try:

        search_url = f"https://www.geeksforgeeks.org/search/?q={quote(query)}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            search_url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        content = []

        for p in paragraphs:

            text = p.get_text(strip=True)

            if len(text) > 60:

                content.append(text)

            if len(content) >= 5:
                break

        if content:

            return "\n".join(content)

    except:
        pass

    return None


# ----------------------------------------
# EDUCATION SEARCH
# ----------------------------------------
def search_education(query):

    subjects = [

        "python",
        "java",
        "c++",
        "dsa",
        "data structure",
        "algorithm",
        "dbms",
        "os",
        "operating system",
        "computer networks",
        "cn",
        "machine learning",
        "ai",
        "web development",
        "html",
        "css",
        "javascript",
        "react",
        "sql",
        "aptitude"

    ]

    query_lower = query.lower()

    for sub in subjects:

        if sub in query_lower:

            result = search_geeksforgeeks(query)

            if result:
                return result

    return None


# ----------------------------------------
# MAIN SEARCH
# ----------------------------------------
def search_web(query):

    sources = [

        search_education,
        search_duckduckgo,
        search_wikipedia

    ]

    for source in sources:

        result = source(query)

        if result:

            return result

    return "No web information found."