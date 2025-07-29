# cache_manager.py

import json
import os

CACHE_FILE = "cache.json"

def load_cache():
    """Load the cache from file, or return an empty dict."""
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_cache(cache):
    """Save the cache dict to file."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)

def get_cached_reference(translation, snippet):
    """Retrieve a cached reference, if available."""
    cache = load_cache()
    key = f"{translation.lower()}::{snippet.lower()}"
    return cache.get(key)

def add_to_cache(translation, snippet, reference):
    """Add a new lookup to the cache."""
    cache = load_cache()
    key = f"{translation.lower()}::{snippet.lower()}"
    cache[key] = reference
    save_cache(cache)