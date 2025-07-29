# An API Interface for...stuff...
from .esv_api_client import fetch_esv_text
from .nlt_api_client import fetch_nlt_text
from .api_bible_client import fetch_verse_text as fetch_generic

def fetch_verse(reference: str, translation: str = "ESV") -> str:
    """
    Dispatches the verse fetch based on the selected translation.
    """
    if translation.upper() == "ESV":
        return fetch_esv_text(reference)
    elif translation.upper() == "NLT":
        return fetch_nlt_text(reference)
    else:
        return fetch_generic(reference, translation)
