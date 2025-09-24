from together import Together
from dotenv import load_dotenv
import os

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY environment variable is not set.")

def generate_recipe_response(message: str, ingredients: str):
    client = Together()
    prompt = f"""
You are Kitchen Buddy, a smart cooking assistant. The user has the following ingredients: {ingredients}.
They said: "{message}". Suggest a suitable recipe using their ingredients and match their mood.
Respond in a friendly and concise way.
"""

    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        print(chunk.choices[0].delta.content or "", end="", flush=True)
        
    return response