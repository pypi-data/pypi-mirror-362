# esv_api_client.py

import requests
from .config_loader import get_esv_api_key

BASE_URL = "https://api.esv.org/v3/passage/text/"

def fetch_esv_text(reference: str) -> str:
    """
    Fetch ESV passage text from api.esv.org and clean it for terminal display.
    """
    api_key = get_esv_api_key()

    if not api_key:
        raise Exception("❌ ESV API key is missing. Set ESV_API_KEY in your environment or config.py.")

    headers = {
        "Authorization": f"Token {api_key}"
    }

    params = {
        "q": reference,
        "include-footnotes": False,
        "include-headings": False,
        "include-verse-numbers": True,
        "include-short-copyright": False
    }

    print(f"Fetching ESV passage: {reference}...", end=" ")
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        print("failed.")
        raise Exception(f"ESV API Error: {response.status_code} — {response.text}")

    print("done.")

    data = response.json()
    passages = data.get("passages", [])

    if not passages:
        raise Exception("No passage text returned by ESV API.")

    # Clean up extra spacing
    text = passages[0].strip().replace("  ", " ")
    return text