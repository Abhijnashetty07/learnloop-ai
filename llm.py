import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=10000,
        retry_options=types.HttpRetryOptions(attempts=1),
    ),
)

MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest",
]
last_good = [None]


def ask_gemini(prompt):
    """Try the last working model first, then the others. Return text or None."""
    order = MODELS[:]
    if last_good[0] in order:
        order.remove(last_good[0])
        order.insert(0, last_good[0])
    for model in order:
        try:
            r = client.models.generate_content(model=model, contents=prompt)
            if r.text:
                last_good[0] = model
                return r.text
        except Exception as e:
            print("failed:", model, str(e)[:60])
    return None


if __name__ == "__main__":
    print(ask_gemini("Explain gradient descent in one sentence using a hiker in fog."))
