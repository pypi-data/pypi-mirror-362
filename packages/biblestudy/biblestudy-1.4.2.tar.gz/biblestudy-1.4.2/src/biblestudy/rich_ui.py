# rich_ui.py

from rich.console import Console
from rich.panel import Panel

console = Console()

def print_main_banner():
    console.rule("[bold blue]📖 Welcome to the Bible Study CLI 📖")

def print_result_banner(reference):
    console.rule(f"[bold green]📜 {reference}")

def print_menu_options():
    console.rule("[bold yellow]What would you like to do?")

    options = [
        "[1] ✏️  Simplify",
        "[2] 🗣️  Modern English",
        "[3] 🏺 Background",
        "[4] 🔗 Cross-References",
        "[5] 🔍 Keyword Focus",
        "[6] 🛠️ Life Application",
        "[7] 🔄 Change Translation for Current Reference",
        "[8] ➕ Enter a New Bible Reference",
        "[9] 📅 Get the Verse of the Day",
        "[0] 🚪 Exit"
    ]

    for option in options:
        console.print(option)

def prompt_user_for_action(action, verse_text):
    # Stub: you will fill this out when wiring up menu actions
    console.print(f"\n[bold cyan]You selected option {action}. (Functionality coming soon!)\n")