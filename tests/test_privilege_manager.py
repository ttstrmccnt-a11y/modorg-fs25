import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import ctypes
from core.privilege_manager import is_admin, elevate

class TestPrivilegeManager(unittest.TestCase):

    @patch('sys.platform', 'win32')
    @patch('ctypes.windll', create=True)
    def test_is_admin_windows_true(self, mock_windll):
        mock_windll.shell32.IsUserAnAdmin.return_value = 1
        self.assertTrue(is_admin())

    @patch('sys.platform', 'win32')
    @patch('ctypes.windll', create=True)
    def test_is_admin_windows_false(self, mock_windll):
        mock_windll.shell32.IsUserAnAdmin.return_value = 0
        self.assertFalse(is_admin())

    @patch('sys.platform', 'linux')
    @patch('os.getuid')
    def test_is_admin_linux_root(self, mock_getuid):
        mock_getuid.return_value = 0
        self.assertTrue(is_admin())

    @patch('sys.platform', 'linux')
    @patch('os.getuid')
    def test_is_admin_linux_user(self, mock_getuid):
        mock_getuid.return_value = 1000
        self.assertFalse(is_admin())

    @patch('sys.platform', 'win32')
    @patch('core.privilege_manager.is_admin')
    @patch('ctypes.windll', create=True)
    @patch('sys.exit')
    def test_elevate_windows_success(self, mock_exit, mock_windll, mock_is_admin):
        mock_is_admin.return_value = False
        mock_windll.shell32.ShellExecuteW.return_value = 33 # Greater than 32 means success

        elevate()

        mock_windll.shell32.ShellExecuteW.assert_called_once()
        mock_exit.assert_called_once_with(0)

if __name__ == '__main__':
    unittest.main()
