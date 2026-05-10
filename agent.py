from openai import OpenAI
from config import API_KEY
from web import search_web
from automation import run_command
from reasoning import think_and_answer
from calculator import solve_math
from summarizer import summarize_text
from math_solver import solve_math_steps
from api_tools import get_weather, get_news, get_stock
from memory import save_memory, recall_memory
from retriever import retrieve_context
from learner import learn

import webbrowser



client = OpenAI(api_key=API_KEY)


def get_ai_response(user_input):

    web_data = search_web(user_input)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are probe.ai, a helpful assistant."
                },
                {
                    "role": "user",
                    "content": f"{user_input}\nWeb info: {web_data}"
                }
            ],
            timeout=10
        )

        return response.choices[0].message.content

    except:
        return web_data if web_data else "I couldn't get a response right now."


def handle_input(user_input):

    user = user_input.lower()

    # 👋 Greeting
    if user in [
        "hiii", "hello", "heyyy",
        "hi", "hey", "hii",
        "hii...", "hiii...", "hiiii..."
    ]:
        return "Hello! I am probe.ai. How can I help you?"

    # ⚡ Automation
    action = run_command(user)

    if action:
        return action

    # 🧠 Retrieve past memory
    memory_context = retrieve_context(user)

    # 🌐 Web search
    web_data = search_web(user)

    # 🧮 Quick calculator
    math_result = solve_math(user)

    if math_result:
        learn(user, math_result)
        return math_result

    # 🧠 MEMORY CHECK
    past = recall_memory(user)

    if past:
        return past

    # 🧾 SUMMARIZER
    if "summarize" in user:
        return summarize_text(user_input)

    # 🧮 STEP-BY-STEP MATH
    if any(x in user for x in ["solve", "+", "-", "*", "/", "="]):

        math = solve_math_steps(user_input)

        if math:
            return math

    # 🌦 WEATHER WEBSITE OPEN
    if "weather" in user:

        webbrowser.open_new_tab("https://weather.com/")

        weather_data = get_weather("https://weather.com/")

        return f"Opening Weather Website...\n\n{weather_data}"

    # 📰 NEWS WEBSITE OPEN
    if "news" in user:

        webbrowser.open_new_tab("https://www.india.com/news/")

        news_data = get_news("https://www.india.com/news/")

        return f"Opening News Website...\n\n{news_data}"

    # 📈 STOCK WEBSITE OPEN
    if "stock" in user:

        webbrowser.open_new_tab("https://www.bseindia.com/")

        stock_data = get_stock("https://www.bseindia.com/")

        return f"Opening Stock Website...\n\n{stock_data}"

     
    # 🙏 THANK YOU HANDLER
    if any(word in user for word in [
        "thanks",
        "thank you",
        "thankyou",
        "thx"
    ]):

        return "__END_CHAT__ Thank you so much! 😊 It was great helping you. If you need anything again, just ask. Have a great day!"

    # 🤖 LOGICAL ENGINE
    reply = think_and_answer(
        user_input,
        web_data,
        memory_context
    )

    # 🤖 Fallback AI
    if not reply:
        reply = get_ai_response(user_input)

    # 🧠 Learn from interaction
    learn(user, reply)

    save_memory(user, reply)

    return reply
