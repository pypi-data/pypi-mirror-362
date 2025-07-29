# notes_manager.py

import os
from datetime import datetime
from .config_loader import get_notes_directory

NOTES_DIR = get_notes_directory()

def save_note(reference, translation, action_title, content):
    """Save a note to the notes directory, organized by session."""
    
    # Ensure notes directory exists
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
    
    # Build a filename based on the current date and time
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"session-{timestamp}.txt"
    filepath = os.path.join(NOTES_DIR, filename)

    # Build the note content
    note_content = f"""
===========================================
Reference: {reference} ({translation})
Action: {action_title}
Timestamp: {timestamp}
===========================================

{content.strip()}

\n
"""

    # Write to file (append if file exists, should be rare but safe)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(note_content)

    return filepath