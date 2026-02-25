import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(prompt):
    """
    Sends a prompt to the AI model and returns the response.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight + cheap
        messages=[
            {"role": "system", "content": "You are a helpful workplace assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()