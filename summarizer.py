from openai import OpenAI
client = OpenAI()

def summarize_text(text):
    if not text or len(text) < 30:
        return "Text too short to summarize."

    sentences = text.split(".")
    summary = ". ".join(sentences[:2])

    return "🧾 Summary:\n" + summary.strip()