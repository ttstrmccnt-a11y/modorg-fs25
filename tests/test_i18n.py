import unittest
import os
import json
from core.config_manager import ConfigManager
from core.i18n import Translator

class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.test_config_path = "test_config_i18n.json"
        self.lang_dir = "test_lang"
        os.makedirs(self.lang_dir, exist_ok=True)

        with open(os.path.join(self.lang_dir, "en.json"), "w") as f:
            json.dump({"HELLO": "Hello"}, f)
        with open(os.path.join(self.lang_dir, "de.json"), "w") as f:
            json.dump({"HELLO": "Hallo"}, f)

        self.cm = ConfigManager(self.test_config_path)

    def tearDown(self):
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)
        import shutil
        if os.path.exists(self.lang_dir):
            shutil.rmtree(self.lang_dir)

    def test_translation_en(self):
        self.cm.set_global("language", "en")
        translator = Translator(self.cm, lang_dir=self.lang_dir)
        self.assertEqual(translator.translate("HELLO"), "Hello")

    def test_translation_de(self):
        self.cm.set_global("language", "de")
        translator = Translator(self.cm, lang_dir=self.lang_dir)
        self.assertEqual(translator.translate("HELLO"), "Hallo")

    def test_translation_fallback(self):
        self.cm.set_global("language", "fr") # Not existing
        translator = Translator(self.cm, lang_dir=self.lang_dir)
        self.assertEqual(translator.translate("HELLO"), "Hello") # Should fallback to en

    def test_missing_key(self):
        translator = Translator(self.cm, lang_dir=self.lang_dir)
        self.assertEqual(translator.translate("MISSING"), "MISSING")

if __name__ == "__main__":
    unittest.main()
