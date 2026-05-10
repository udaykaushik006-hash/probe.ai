from flask import Flask, request, jsonify, render_template
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

import json
import os
import datetime
import random

# ============================================
# FLASK APP
# ============================================
app = Flask(__name__)

@app.route("/")
def home():
    return "probe ai is live,, ready to assist you! 🚀"

# ============================================
# OPENAI CLIENT
# ============================================
client = OpenAI(api_key=API_KEY)

# ============================================
# HISTORY FILE
# ============================================
HISTORY_FILE = "history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

# ============================================
# LOAD HISTORY
# ============================================
def load_history():

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

# ============================================
# SAVE HISTORY
# ============================================
def save_history(user, bot):

    history = load_history()

    history.append({
        "type": "user",
        "message": user,
        "time": current_time()
    })

    history.append({
        "type": "bot",
        "message": bot,
        "time": current_time()
    })

    # keep only last 100 chats
    history = history[-100:]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# ============================================
# CURRENT TIME
# ============================================
def current_time():
    return datetime.datetime.now().strftime("%I:%M %p")

# ============================================
# OPENAI RESPONSE
# ============================================
def get_ai_response(user_input):

    web_data = search_web(user_input)

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    """
                    You are probe.ai,
                    an advanced futuristic AI assistant.

                    Rules:
                    - Be intelligent
                    - Friendly
                    - Helpful
                    - Short but informative
                    - Modern AI tone
                    """
                },

                {
                    "role": "user",
                    "content": f"""
                    User Input:
                    {user_input}

                    Web Data:
                    {web_data}
                    """
                }

            ],

            temperature=0.7,
            max_tokens=500

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"⚠️ OpenAI API Error: {str(e)}"

# ============================================
# MAIN AI ENGINE
# ============================================
def handle_input(user_input):

    user = user_input.lower()

    # ====================================
    # GREETING
    # ====================================
    if user in [
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii"
    ]:

        return "👋 Hello! I am probe.ai. How can I help you today?"

    # ====================================
    # AUTOMATION
    # ====================================
    action = run_command(user)

    if action:
        return action

    # ====================================
    # MEMORY CONTEXT
    # ====================================
    memory_context = retrieve_context(user)

    # ====================================
    # WEB SEARCH
    # ====================================
    web_data = search_web(user)

    # ====================================
    # QUICK MATH
    # ====================================
    math_result = solve_math(user)

    if math_result:

        learn(user, math_result)

        return math_result

    # ====================================
    # RECALL MEMORY
    # ====================================
    past = recall_memory(user)

    if past:
        return past

    # ====================================
    # SUMMARIZER
    # ====================================
    if "summarize" in user:

        return summarize_text(user_input)

    # ====================================
    # STEP-BY-STEP MATH
    # ====================================
    if any(x in user for x in [
        "solve",
        "+",
        "-",
        "*",
        "/",
        "="
    ]):

        math = solve_math_steps(user_input)

        if math:
            return math

    # ====================================
    # WEATHER
    # ====================================
    if "weather" in user:

        weather_data = get_weather("india")

        return f"🌦 {weather_data}"

    # ====================================
    # NEWS
    # ====================================
    if "news" in user:

        news_data = get_news("technology")

        return f"📰 {news_data}"

    # ====================================
    # STOCK
    # ====================================
    if "stock" in user:

        stock_data = get_stock("TCS")

        return f"📈 {stock_data}"

    # ====================================
    # THANK YOU
    # ====================================
    if any(word in user for word in [
        "thanks",
        "thank you",
        "thankyou",
        "thx"
    ]):

        return """
😊 You're welcome!

It was great helping you.
If you need anything again,
just ask anytime 🚀
"""

    # ====================================
    # LOGICAL ENGINE
    # ====================================
    reply = think_and_answer(

        user_input,
        web_data,
        memory_context

    )

    # ====================================
    # FALLBACK OPENAI
    # ====================================
    if not reply:

        reply = get_ai_response(user_input)

    # ====================================
    # LEARN + SAVE MEMORY
    # ====================================
    learn(user, reply)

    save_memory(user, reply)

    return reply

# ============================================
# HOME PAGE
# ============================================
@app.route("/")
def home():

    return render_template("index.html")

# ============================================
# CHAT API
# ============================================
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message")

    if not user_message:

        return jsonify({
            "response": "⚠️ Empty message"
        })

    # AI RESPONSE
    bot_reply = handle_input(user_message)

    # SAVE CHAT
    save_history(user_message, bot_reply)

    return jsonify({

        "response": bot_reply,
        "time": current_time()

    })

# ============================================
# HISTORY API
# ============================================
@app.route("/history")
def history():

    return jsonify(load_history())

# ============================================
# CLEAR CHAT API
# ============================================
@app.route("/clear", methods=["POST"])
def clear():

    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

    return jsonify({
        "status": "success"
    })

# ============================================
# FILE UPLOAD API
# ============================================
@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:

        return jsonify({

            "status": "error",
            "message": "No file uploaded"

        })

    file = request.files["file"]

    upload_folder = "uploads"

    if not os.path.exists(upload_folder):

        os.makedirs(upload_folder)

    filepath = os.path.join(

        upload_folder,
        file.filename

    )

    file.save(filepath)

    return jsonify({

        "status": "success",
        "filename": file.filename

    })

# ============================================
# RUN SERVER
# ============================================
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(debug=True)(
        host="0.0.0.0",
        port=port
    )