import ctypes
import sys
import os

def is_admin():
    """
    Checks if the current process has administrative privileges.
    Works on Windows and Unix-like systems.
    """
    try:
        # Windows check
        if sys.platform == 'win32':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # Unix-like check
            return os.getuid() == 0
    except (AttributeError, Exception):
        return False

def elevate():
    """
    Triggers the Windows UAC dialog to restart the script as an administrator.
    Only applicable on Windows.
    """
    if is_admin():
        return True

    if sys.platform == 'win32':
        # Re-run the script with administrative privileges
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        try:
            # ShellExecuteW(hwnd, lpOperation, lpFile, lpParameters, lpDirectory, nShowCmd)
            # lpOperation: "runas" triggers UAC
            ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            if ret > 32:
                # Successfully started the process
                sys.exit(0)
            else:
                return False
        except Exception:
            return False

    return False
