import customtkinter as ctk
from threading import Thread
import datetime
import time
import requests

from agent import handle_input
from voice import speak, listen
from bs4 import BeautifulSoup

# FEATURES
from summarizer import summarize_text
from math_solver import solve_math_steps
from wake_word import listen_wake_word

# SOUND
try:
    from playsound import playsound
    SOUND = True
except:
    SOUND = False

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ---------------- WEATHER API ----------------
def get_weather(city):

    api_key = "YOUR_OPENWEATHER_API_KEY"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:

        data = requests.get(url).json()

        temp = data["main"]["temp"]

        desc = data["weather"][0]["description"]

        return f"""
🌦 Weather in {city}

🌡 Temperature: {temp}°C
☁ Condition: {desc}
"""

    except:

        return "Weather data not available."


# ---------------- NEWS API ----------------
def get_news():

    url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"

    try:

        response = requests.get(url)

        soup = BeautifulSoup(response.content, "xml")

        items = soup.find_all("item")

        headlines = []

        for item in items[:10]:

            headlines.append("• " + item.title.text)

        return "📰 Latest News Headlines:\n\n" + "\n".join(headlines)

    except Exception as e:

        return f"News fetch error: {e}"


# ---------------- STOCK API ----------------
def get_stock():

    try:

        url = "https://query1.finance.yahoo.com/v8/finance/chart/^NSEI"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        data = requests.get(url, headers=headers).json()

        result = data["chart"]["result"][0]["meta"]

        price = result["regularMarketPrice"]

        prev = result["previousClose"]

        change = round(price - prev, 2)

        return f"""
📈 NIFTY 50 Update

Current Price: {price}
Previous Close: {prev}
Change: {change}
"""

    except Exception as e:

        return f"Stock fetch error: {e}"


# ======================================================
# ===================== MAIN APP =======================
# ======================================================

class ProbeAI:

    def __init__(self):

        self.app = ctk.CTk()
        self.app.geometry("1100x650")
        self.app.title("probe.ai")

        # GREETING
        hour = datetime.datetime.now().hour

        if hour < 12:
            greet = "Good Morning ☀️"

        elif hour < 18:
            greet = "Good Afternoon 🌤"

        else:
            greet = "Good Evening 🌙"

        # STATES
        self.chat_history = []
        self.voice_enabled = True
        self.dark_mode = True
        self.sidebar_open = False

        # ---------------- TOP BAR ----------------
        self.topbar = ctk.CTkFrame(
            self.app,
            height=50,
            fg_color="#0f172a"
        )

        self.topbar.pack(fill="x")

        self.time_label = ctk.CTkLabel(
            self.topbar,
            text="",
            font=("Arial", 16)
        )

        self.time_label.pack(pady=10)

        self.update_time()

        # ---------------- MAIN FRAME ----------------
        self.main_frame = ctk.CTkFrame(self.app)

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # ---------------- SIDEBAR ----------------
        self.sidebar = ctk.CTkFrame(
            self.main_frame,
            width=230,
            fg_color="#111827",
            corner_radius=0
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Dashboard",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 15))

        # BUTTONS
        buttons = [

            ("➕ New Chat", self.new_chat),
            ("🧠 History", self.show_history),
            ("🗑 Clear Chat", self.clear_chat),
            ("⚙️ Settings", self.toggle_settings),
            ("🌦 Weather", self.show_weather),
            ("📰 News", self.show_news),
            ("📈 Stock", self.show_stock),
            ("🧾 Summarize", self.summarize_input),
            ("🧮 Solve Math", self.solve_math)

        ]

        for text, cmd in buttons:

            ctk.CTkButton(
                self.sidebar,
                text=text,
                width=190,
                command=cmd
            ).pack(pady=6)

        # ---------------- CHAT FRAME ----------------
        self.chat_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#1e1e1e"
        )

        self.chat_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        # MENU BUTTON
        self.toggle_btn = ctk.CTkButton(
            self.chat_frame,
            text="☰",
            width=40,
            height=40,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.toggle_sidebar
        )

        self.toggle_btn.pack(
            anchor="nw",
            padx=10,
            pady=10
        )

        # LOGO
        self.avatar = ctk.CTkLabel(
            self.chat_frame,
            text="🔗",
            font=("Arial", 40)
        )

        self.avatar.pack(pady=(10, 0))

        self.title = ctk.CTkLabel(
            self.chat_frame,
            text="probe.ai",
            font=("Arial", 28, "bold")
        )

        self.title.pack(pady=(0, 10))

        # CHAT AREA
        self.chat_canvas = ctk.CTkScrollableFrame(
            self.chat_frame,
            fg_color="#1a1a1a"
        )

        self.chat_canvas.pack(
            pady=10,
            padx=10,
            fill="both",
            expand=True
        )

        # INPUT AREA
        self.input_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )

        self.input_frame.pack(pady=10)

        self.entry = ctk.CTkEntry(
            self.input_frame,
            width=500,
            height=40
        )

        self.entry.grid(
            row=0,
            column=0,
            padx=10
        )

        # SEND BUTTON
        ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=120,
            height=40,
            command=self.send
        ).grid(row=0, column=1, padx=5)

        # VOICE BUTTON
        ctk.CTkButton(
            self.input_frame,
            text="Voice 🎤",
            width=120,
            height=40,
            command=self.voice
        ).grid(row=0, column=2, padx=5)

        # WELCOME
        self.add_bot_message_stream(
            f"{greet}..! Hiii I am probe.ai. How can I help you?"
        )

        # WAKE WORD THREAD
        Thread(
            target=self.wake_listener,
            daemon=True
        ).start()

    # ---------------- WAKE WORD ----------------
    def wake_listener(self):

        while True:

            if listen_wake_word():

                self.add_bot_message_stream(
                    "Yes, I am listening..."
                )

                self.voice()

    # ---------------- WEATHER ----------------
    def show_weather(self):

        city = self.entry.get()

        if not city:
            city = "Hyderabad"

        result = get_weather(city)

        self.add_bot_message_stream(result)

    # ---------------- NEWS ----------------
    def show_news(self):

        result = get_news()

        self.add_bot_message_stream(result)

    # ---------------- STOCK ----------------
    def show_stock(self):

        result = get_stock()

        self.add_bot_message_stream(result)

    # ---------------- SUMMARIZE ----------------
    def summarize_input(self):

        text = self.entry.get()

        if text:

            result = summarize_text(text)

            self.add_bot_message_stream(result)

    # ---------------- MATH ----------------
    def solve_math(self):

        text = self.entry.get()

        if text:

            result = solve_math_steps(text)

            self.add_bot_message_stream(result)

    # ---------------- TIME ----------------
    def update_time(self):

        now = datetime.datetime.now()

        self.time_label.configure(
            text=now.strftime("%A | %d %B %Y | %H:%M:%S")
        )

        self.app.after(
            1000,
            self.update_time
        )

    # ---------------- SIDEBAR ----------------
    def toggle_sidebar(self):

        if self.sidebar_open:

            self.sidebar.pack_forget()

            self.sidebar_open = False

        else:

            self.sidebar.pack(
                side="left",
                fill="y",
                before=self.chat_frame
            )

            self.sidebar_open = True

    # ---------------- NEW CHAT ----------------
    def new_chat(self):

        for widget in self.chat_canvas.winfo_children():

            widget.destroy()

        self.add_bot_message_stream(
            "New chat started."
        )

    # ---------------- HISTORY ----------------
    def show_history(self):

        if not self.chat_history:

            self.add_bot_message_stream(
                "No chat history yet."
            )

            return

        history_text = "\n\n".join(
            self.chat_history[-10:]
        )

        self.add_bot_message_stream(
            "🧠 Recent Chats:\n\n" + history_text
        )

    # ---------------- CLEAR CHAT ----------------
    def clear_chat(self):

        for widget in self.chat_canvas.winfo_children():

            widget.destroy()

        self.chat_history.clear()

        self.add_bot_message_stream(
            "Chat cleared successfully."
        )

    # ---------------- SETTINGS ----------------
    def toggle_settings(self):

        self.voice_enabled = not self.voice_enabled

        self.dark_mode = not self.dark_mode

        ctk.set_appearance_mode(
            "dark" if self.dark_mode else "light"
        )

        self.add_bot_message_stream(
            f"⚙️ Voice: {'ON' if self.voice_enabled else 'OFF'} | Theme: {'Dark' if self.dark_mode else 'Light'}"
        )

    # ---------------- USER MESSAGE ----------------
    def add_user_message(self, text):

        ctk.CTkLabel(
            self.chat_canvas,
            text=text,
            fg_color="#2563eb",
            text_color="white",
            corner_radius=20,
            padx=12,
            pady=8,
            wraplength=400
        ).pack(
            anchor="e",
            padx=10,
            pady=6
        )

    # ---------------- BOT MESSAGE ----------------
    def add_bot_message_stream(self, text):

        bubble = ctk.CTkLabel(
            self.chat_canvas,
            text="",
            fg_color="#1f2937",
            text_color="#e5e7eb",
            corner_radius=20,
            padx=12,
            pady=8,
            wraplength=500,
            justify="left"
        )

        bubble.pack(
            anchor="w",
            padx=10,
            pady=6
        )

        for word in str(text).split():

            bubble.configure(
                text=bubble.cget("text") + word + " "
            )

            self.chat_canvas.update()

            time.sleep(0.02)

    # ---------------- AI PROCESS ----------------
    def process(self, text):

        reply = handle_input(text)

        self.chat_history.append(f"You: {text}")
        self.chat_history.append(f"AI: {reply}")

        self.add_bot_message_stream(reply)

        if self.voice_enabled:

            speak(reply)

    # ---------------- SEND ----------------
    def send(self):

        text = self.entry.get()

        if not text:
            return

        self.add_user_message(text)

        Thread(
            target=self.process,
            args=(text,)
        ).start()

        self.entry.delete(0, "end")

    # ---------------- VOICE ----------------
    def voice(self):

        def run():

            cmd = listen()

            if cmd:

                self.add_user_message(cmd)

                self.process(cmd)

        Thread(target=run).start()

    # ---------------- RUN ----------------
    def run(self):

        self.app.mainloop()


# ======================================================
# ===================== START ==========================
# ======================================================

if __name__ == "__main__":

    ProbeAI().run()