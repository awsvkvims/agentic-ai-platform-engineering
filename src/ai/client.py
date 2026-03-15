import os
from dotenv import load_dotenv
from openai import OpenAI
from src.ai.config import MODEL_NAME, DEFAULT_SYSTEM_ROLE

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_model(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {"role": "system", "content": DEFAULT_SYSTEM_ROLE},
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text