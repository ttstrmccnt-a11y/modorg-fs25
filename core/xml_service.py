import os
import shutil
from lxml import etree
from core.privilege_manager import PrivilegeManager

class XMLService:
    """
    Robust XML handler using lxml to preserve comments and formatting.
    """
    @staticmethod
    def smart_patch(file_path, xpath, value):
        """
        Navigates to the node(s) specified by xpath and updates their value.
        Automatically creates a .bak copy before writing.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Create .bak copy
        bak_path = file_path + ".bak"
        try:
            shutil.copy2(file_path, bak_path)
        except PermissionError:
            PrivilegeManager.elevate()
            shutil.copy2(file_path, bak_path)

        try:
            # Use a parser that preserves comments and doesn't strip blank text
            parser = etree.XMLParser(remove_blank_text=False, resolve_entities=False, strip_cdata=False)
            tree = etree.parse(file_path, parser)

            nodes = tree.xpath(xpath)
            if not nodes:
                # If xpath doesn't find anything, we don't write.
                # Depending on requirements, we might want to create the path.
                # For now, let's just log or raise.
                print(f"Warning: XPath '{xpath}' not found in {file_path}")
                return False

            for node in nodes:
                node.text = str(value)

            # Write operation
            def do_write():
                tree.write(
                    file_path,
                    encoding='utf-8',
                    xml_declaration=True,
                    pretty_print=False,
                    method="xml"
                )

            try:
                do_write()
            except PermissionError:
                PrivilegeManager.elevate()
                do_write()

            return True

        except Exception as e:
            print(f"Error during XML patch: {e}")
            # Restore from backup if something went wrong during parsing/writing
            if os.path.exists(bak_path):
                shutil.copy2(bak_path, file_path)
            raise e
