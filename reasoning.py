from openai import OpenAI
from config import API_KEY

client = OpenAI(api_key=API_KEY)

def think_and_answer(user_input, web_data=None, memory_data=None):
    """
    Performs structured reasoning + self-verification.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are probe.ai, a logical AI assistant.\n"
                        "Follow this process internally:\n"
                        "1. Understand the question\n"
                        "2. Break into steps\n"
                        "3. Solve carefully\n"
                        "4. Verify the answer\n"
                        "Return ONLY the final correct answer clearly.\n"
                    )
                },
                {
                    "role": "user",
                    "content": f"""
User Question: {user_input}

Web Info: {web_data}
Memory: {memory_data}

Give the most accurate and logically correct answer.
"""
                }
            ],
            timeout=12
        )

        return response.choices[0].message.content

    except Exception as e:
        return None