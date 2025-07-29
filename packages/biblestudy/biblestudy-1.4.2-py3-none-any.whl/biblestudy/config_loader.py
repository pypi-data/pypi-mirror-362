# config_loader.py

import os

# Try to import config.py, but fall back to defaults if not available
try:
    import config
except ImportError:
    config = None

def get_bible_api_key():
    return os.getenv("BIBLE_API_KEY") or (config.BIBLE_API_KEY if config else "")

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY") or (config.OPENAI_API_KEY if config else "")

def get_notes_directory():
    return os.getenv("BIBLESTUDY_NOTES_DIRECTORY") or (config.BIBLESTUDY_NOTES_DIRECTORY if config else "notes")

def get_nlt_api_key():
    return os.getenv("NLT_API_KEY") or (config.NLT_API_KEY if config else "")

def get_esv_api_key():
    return os.getenv("ESV_API_KEY") or (config.ESV_API_KEY if config else "")