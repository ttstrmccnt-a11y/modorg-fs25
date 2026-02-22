import json
import os

class Translator:
    """
    Handles localization by loading translation files based on configuration.
    """
    def __init__(self, config_manager, lang_dir="lang"):
        self.config_manager = config_manager
        self.lang_dir = lang_dir
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        """Loads the translation file for the configured language."""
        lang = self.config_manager.get_global("language", "en")
        lang_file = os.path.join(self.lang_dir, f"{lang}.json")

        if not os.path.exists(lang_file):
            # Fallback to English if the configured language file is missing
            lang_file = os.path.join(self.lang_dir, "en.json")

        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading translations: {e}")
        else:
            self.translations = {}

    def translate(self, key):
        """Returns the translation for the given key, or the key itself if not found."""
        return self.translations.get(key, key)

# Global translator instance
_translator_instance = None

def initialize_i18n(config_manager):
    """Initializes the global translator instance."""
    global _translator_instance
    _translator_instance = Translator(config_manager)

def _(key):
    """Global translation function."""
    if _translator_instance:
        return _translator_instance.translate(key)
    return key
