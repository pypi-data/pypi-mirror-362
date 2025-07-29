import sys

try:
    from .rich_ui import (
        print_main_banner,
        print_result_banner,
        print_menu_options
    )
    from .cache_manager import get_cached_reference, add_to_cache
    from .api_bible_client import fetch_verse_text
    from .nlt_api_client import fetch_nlt_text
    from .esv_api_client import fetch_esv_text
    from .openai_client import ask_openai
    from .notes_manager import save_note
    from .daily_verse_loader import get_today_verse_reference
except Exception as e:
    print("\u274c Exception caught during imports!")
    print(f"Error: {e}")
    sys.exit(1)

def select_translation():
    print("\nWhich translation would you like to use?")
    print("[1] NLT (New Living Translation)")
    print("[2] ESV (English Standard Version)")
    print("[3] FBV (Free Bible Version)")
    print("[4] KJV (King James Version)")
    print("[5] ASV (American Standard Version)")
    print("[6] WEB (World English Bible)")

    translation_options = {
        "1": "NLT",
        "2": "ESV",
        "3": "FBV",
        "4": "KJV",
        "5": "ASV",
        "6": "WEB"
    }

    choice = input("Enter the number for your translation [1-6]: ").strip()
    return translation_options.get(choice, "NLT")

def main_menu():
    print_menu_options()
    choice = input("\nChoose an option (0-9) [0/1/2/3/4/5/6/7/8/9]: ").strip()
    return choice

def show_verse(reference, verse_text):
    print_result_banner(reference)
    print(verse_text)

def error_message(message):
    print(f"\n\u274c {message}\n")

def goodbye_message():
    print("\n\U0001F44B Goodbye! Thanks for using the Bible Study CLI!\n")

def prompt_save():
    save = input("\nWould you like to save this result? (y/n): ").strip().lower()
    return save == "y"

def get_verse_text(reference, translation):
    if translation == "NLT":
        return fetch_nlt_text(reference)
    elif translation == "ESV":
        return fetch_esv_text(reference)
    else:
        return fetch_verse_text(reference, translation)

def perform_interpretation_loop(reference, translation, verse_text):
    show_verse(reference, verse_text)

    while True:
        choice = main_menu()

        if choice == "0":
            goodbye_message()
            break
        elif choice == "7":
            translation = select_translation()
            try:
                verse_text = get_verse_text(reference, translation)
                show_verse(reference, verse_text)
            except Exception as e:
                error_message(f"Error switching translation: {e}")
        elif choice == "8":
            return True
        elif choice == "9":
            reference = get_today_verse_reference()
            try:
                verse_text = get_verse_text(reference, translation)
                show_verse(reference, verse_text)
            except Exception as e:
                error_message(f"Error fetching daily verse: {e}")
        else:
            action_map = {
                "1": ("Simplified Explanation", "simplify"),
                "2": ("Modern English Version", "modern"),
                "3": ("Historical Background", "background"),
                "4": ("Cross References", "crossref"),
                "5": ("Keyword Focus", "keywords"),
                "6": ("Life Application", "lifeapp")
            }

            action_title, action_key = action_map.get(choice, (None, None))

            if not action_title:
                error_message("Invalid choice. Please select a valid menu option.")
                continue

            try:
                result = ask_openai(action_key, verse_text)
            except Exception as e:
                error_message(f"Error communicating with AI: {e}")
                continue

            print_result_banner(action_title)
            print(result)

            if prompt_save():
                try:
                    saved_file = save_note(
                        reference=reference,
                        translation=translation,
                        action_title=action_title,
                        content=result
                    )
                    print(f"\u2705 Note saved at: {saved_file}")
                except Exception as e:
                    error_message(f"Error saving note: {e}")
    return False

def main():
    try:
        print_main_banner()

        use_daily = input("Would you like to see the Verse of the Day? (y/n): ").strip().lower() == "y"
        if use_daily:
            reference = get_today_verse_reference()
            print(f"\n\U0001F4C5 Today's verse: {reference}")
        else:
            reference = input("\nEnter a Bible reference (e.g., John 3:16):\n\n>> ").strip()

        translation = select_translation()
        reference = get_cached_reference(translation, reference) or reference

        while True:
            try:
                verse_text = get_verse_text(reference, translation)
                break
            except Exception as e:
                error_message(f"Error fetching verse: {e}")
                reference = input("\nPlease enter a new valid Bible reference: ").strip()

        while True:
            enter_new = perform_interpretation_loop(reference, translation, verse_text)
            if not enter_new:
                break
            reference = input("\nEnter a new Bible reference: ").strip()
            translation = select_translation()
            reference = get_cached_reference(translation, reference) or reference

            try:
                verse_text = get_verse_text(reference, translation)
            except Exception as e:
                error_message(f"Error fetching new reference: {e}")
                break

    except Exception as e:
        print("\u274c Crash detected inside main()!")
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\u274c Exception caught inside __main__ startup.")
        print(f"Error: {e}")
