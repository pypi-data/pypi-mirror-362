import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return api_key

def explain_with_openai(code):
    api_key = get_openai_api_key()
    client = OpenAI()

    client.api_key = api_key

    prompt = (
        "Explain the following Python code in a way that a 5-year-old can understand. "
        "Use simple language and analogies. Here is the code:\n\n"
        f"{code}\n\n"
        "Explanation:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to get explanation from OpenAI: {str(e)}")
    
def explain_with_openrouter(code):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None, "OPENROUTER_API_KEY is not set."

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"  
    )

    prompt = (
        "Explain this Python function in a way that a 5-year-old can understand. "
        "Use simple words and examples:\n\n"
        f"{code}\n\nExplanation:"
    )

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip(), None

    except Exception as e:
        return None, f"OpenRouter error: {e}"


    