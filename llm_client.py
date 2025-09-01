from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_BASE_URL


def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
