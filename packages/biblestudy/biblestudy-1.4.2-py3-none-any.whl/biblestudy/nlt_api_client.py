# nlt_api_client.py

import requests
from bs4 import BeautifulSoup
from .config_loader import get_nlt_api_key

BASE_URL = "https://api.nlt.to/api/passages"

def fetch_nlt_text(reference: str) -> str:
    """
    Fetch clean NLT passage text from api.nlt.to,
    preserving verse numbers and removing footnotes, anchors, and headers.
    """
    api_key = get_nlt_api_key()

    if not api_key:
        raise Exception("❌ NLT API key is missing. Set NLT_API_KEY in your environment or config.py.")

    params = {
        "ref": reference,
        "key": api_key
    }

    print(f"Fetching NLT passage: {reference}...", end=" ")
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200 or "Custom Page Error" in response.text:
        print("failed.")
        raise Exception(f"NLT API Error: {response.status_code} — Check the reference or API key.")

    print("done.")
    soup = BeautifulSoup(response.text, "html.parser")

    all_verses = []

    for verse_tag in soup.select("verse_export"):
        # Remove footnotes, anchors, and headers
        for tag in verse_tag.select(".tn, a, h2, h3"):
            tag.decompose()

        # Extract verse number
        verse_num = verse_tag.select_one(".vn")
        verse_num_text = verse_num.get_text(" ", strip=True) if verse_num else ""

        # Extract full verse content
        verse_text = verse_tag.get_text(" ", strip=True)

        # Strip duplicate number if it appears in the text
        if verse_text.startswith(verse_num_text):
            verse_text = verse_text[len(verse_num_text):].lstrip()

        full_line = f"[{verse_num_text}] {verse_text}" if verse_text else ""
        if full_line.strip():
            all_verses.append(full_line)

    return "\n".join(all_verses).strip()