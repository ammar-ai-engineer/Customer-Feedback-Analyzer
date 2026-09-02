# Sets up ONE connection, to whichever AI provider config.py says to use.
# Every other file just calls get_client_and_model() - nobody else
# needs to know Gemini and Ollama even work differently underneath.

from openai import OpenAI
from dotenv import load_dotenv
import os
from config import AI_PROVIDER, GEMINI_MODEL, OLLAMA_MODEL

load_dotenv(override=True)


def get_client_and_model():
    """
    Returns the right client and model name, based on config.AI_PROVIDER.
    """
    if AI_PROVIDER == "gemini":
        google_api_key = os.getenv("GOOGLE_API_KEY")
        client = OpenAI(
            api_key=google_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        model = GEMINI_MODEL

    elif AI_PROVIDER == "ollama":
        client = OpenAI(
            api_key="ollama",  # Ollama ignores this, but the library needs something here
            base_url="http://localhost:11434/v1"
        )
        model = OLLAMA_MODEL

    else:
        raise ValueError(f"Unknown AI_PROVIDER: {AI_PROVIDER}. Use 'gemini' or 'ollama'.")

    return client, model