# openai_client.py

from openai import OpenAI
from .config_loader import get_openai_api_key

client = OpenAI(api_key=get_openai_api_key())

PROMPTS = {
    "simplify": "Simplify the meaning of this Bible verse into basic, clear terms:",
    "modern": "Reword this Bible verse into everyday modern English:",
    "background": "Explain the historical background and context of this Bible verse:",
    "crossref": "List 2-3 other Bible verses that relate closely to this verse:",
    "keywords": "Highlight key words in this Bible verse and explain their meaning:",
    "lifeapp": "Suggest practical ways to apply the meaning of this Bible verse today:"
}

def ask_openai(action, verse_text):
    """Send a prompt to OpenAI and get a response."""
    if action not in PROMPTS:
        raise ValueError(f"Unknown action: {action}")

    prompt = f"{PROMPTS[action]} \"{verse_text}\""

    print("Generating response...", end=" ")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # You could also use "gpt-3.5-turbo" if you want cheaper queries
            messages=[
                {"role": "system", "content": "You are a helpful Bible study assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        print("done.")
        return content
    except Exception as e:
        print("failed.")
        raise Exception(f"Error generating interpretation: {str(e)}")
