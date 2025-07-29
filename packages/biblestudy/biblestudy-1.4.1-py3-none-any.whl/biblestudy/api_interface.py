# An API Interface for...stuff...
from biblestudy.esv_api_client import fetch_verse_text as fetch_esv
from biblestudy.nlt_api_client import fetch_verse_text as fetch_nlt

def fetch_verse(reference: str, translation: str = "NLT") -> str:
    if translation.upper() == "ESV":
        return fetch_esv(reference)
    return fetch_nlt(reference)
