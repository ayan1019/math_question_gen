# src/llm_client.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment (see README).")

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_questions_from_prompt(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.2, max_tokens: int = 1500) -> str:
    """
    Calls OpenAI chat completion API to generate questions.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that must output ONLY the question blocks in the exact format described by the user."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content
