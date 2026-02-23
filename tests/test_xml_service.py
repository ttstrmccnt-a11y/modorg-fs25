import unittest
import os
import shutil
from core.xml_service import XMLService

class TestXMLService(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_game.xml"
        with open(self.test_file, "w") as f:
            f.write("<root><node>old</node></root>")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_file + ".bak"):
            os.remove(self.test_file + ".bak")

    def test_smart_patch(self):
        success = XMLService.smart_patch(self.test_file, "/root/node", "new")
        self.assertTrue(success)

        with open(self.test_file, "r") as f:
            content = f.read()
            self.assertIn("<node>new</node>", content)

        # Check backup
        self.assertTrue(os.path.exists(self.test_file + ".bak"))
        with open(self.test_file + ".bak", "r") as f:
            self.assertIn("<node>old</node>", f.read())

    def test_smart_patch_not_found(self):
        success = XMLService.smart_patch(self.test_file, "/root/nonexistent", "value")
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()
