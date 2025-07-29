# Changelog

## [1.3.0] - 2025-05-01

### Added
- 📅 New "Verse of the Day" feature!
  - User is prompted on startup to view a daily verse
  - Option 9 in the action menu lets you re-view the daily verse at any time
- 📚 Introduced `daily_verses.json`: 366 hand-picked references used across devotionals
- 🔁 New action menu flow for switching verses or translations without restarting the app

### Changed
- 🧼 Refactored `main.py` to improve structure, remove redundancy, and better separate logic
- ✂️ Removed old experimental OpenAI-powered verse suggestion logic

### Fixed
- 🐛 NLT client now correctly parses references with numeric book names (e.g., "1 Corinthians")
- 🧼 Stripped unwanted section headers and fixed empty line bugs in NLT output

---

## [1.2.1] – 2025-04-30

### 🐛 Bugfixes

- 🌐 Fixed URL encoding for NLT references containing spaces (e.g., `1 Corinthians`, `3 John`)
- 🧼 Removed extra content from NLT output:
  - Section and chapter headers (e.g., "Greetings", "Caring for the Lord’s Workers")
  - Footnotes and superscript anchors
- ✅ Now properly handles short/red-letter-free books like *3 John*
- 🔢 Ensures accurate verse numbering and clean, readable formatting

---

## [1.2.0] – 2025-04-30

### ✨ New Features

- 📖 Added support for the **ESV (English Standard Version)** via [api.esv.org](https://api.esv.org/)
- 🔐 Secure API key integration using `Authorization: Token ...` header
- 🔄 ESV available as option [2] in the translation menu
- 📜 ESV results include properly formatted verse numbers (e.g., `[16]`, `[17]`) for multi-verse passages

### 🧰 Internal Improvements

- Refactored `main.py` to route ESV lookups cleanly through `fetch_esv_text()`
- Added `get_esv_api_key()` in `config_loader.py` for safe fallback loading
- Updated `.env.example` and `config.py.sample` to include `ESV_API_KEY`

---

## [1.1.0] – 2025-04-28

### ✨ New Features

- 🔄 Added full support for the **NLT (New Living Translation)** using [api.nlt.to](https://api.nlt.to)
- 🔠 NLT moved to the default translation option (now option [1])
- 📜 Preserves verse numbers in multi-verse lookups
- 🔧 Added fallback-friendly API routing per translation
- 💾 Support saving study notes as always

### 🛠 Improvements

- Smarter verse parsing (BeautifulSoup) for clean CLI output
- Improved error handling for invalid references or missing API keys
- More readable main menu with “Change Translation” and “Enter New Reference”

### 🧹 Cleanup

- Removed unsupported/deprecated translations (NIV, CSB, NKJV)
- Updated config loader to support NLT API key
- Improved docs, environment handling, and README formatting
