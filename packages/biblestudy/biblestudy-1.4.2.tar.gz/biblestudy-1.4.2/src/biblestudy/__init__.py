"""
BibleStudy CLI - A text-based Bible study companion for your terminal.

Powered by api.bible, api.nlt.to, api.esv.org, and OpenAI.
"""

__version__ = "1.4.2"
__author__ = "labrack"
__description__ = "A text-based Bible study companion for your terminal"

from .cli import main

__all__ = ["main"]
