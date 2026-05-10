import requests

# 🌦 WEATHER
def get_weather(city="Vijayawada"):
    try:
        url = f"https://wttr.in/{city}?format=3"
        res = requests.get(url)
        return res.text
    except:
        return "Unable to fetch weather."

# 📰 NEWS
def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_NEWS_API_KEY"
        data = requests.get(url).json()

        articles = data.get("articles", [])[:5]

        if not articles:
            return "No news found."

        news = "\n\n".join([f"📰 {a['title']}" for a in articles])
        return news

    except:
        return "News service unavailable."

# 📈 STOCK
def get_stock(symbol="AAPL"):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        data = requests.get(url).json()

        price = data["quoteResponse"]["result"][0]["regularMarketPrice"]

        return f"{symbol} Stock Price: ${price}"

    except:
        return "Stock data unavailable."