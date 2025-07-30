"""
Advanced system check utilities for shadowcrypt package.

Provides platform detection, hardware binding, expiry lock, and environment checks.
"""

import platform
import hashlib
import uuid
import time
import os
import subprocess
import sys

def get_platform():
    """
    Get the current platform name.
    """
    return platform.system()

def get_machine_id():
    """
    Generate a hardware binding ID using MAC address and other system info.
    """
    try:
        mac = uuid.getnode()
        mac_hash = hashlib.sha256(str(mac).encode()).hexdigest()
    except Exception:
        mac_hash = None

    try:
        # Additional system info for binding
        uname = platform.uname()
        sys_info = f"{uname.system}-{uname.node}-{uname.release}-{uname.version}-{uname.machine}"
        sys_hash = hashlib.sha256(sys_info.encode()).hexdigest()
    except Exception:
        sys_hash = None

    combined = (mac_hash or '') + (sys_hash or '')
    return hashlib.sha256(combined.encode()).hexdigest()

def check_expiry(expiry_timestamp):
    """
    Check if the current time is before the expiry timestamp.

    Args:
        expiry_timestamp (int): Unix timestamp of expiry.

    Returns:
        bool: True if not expired, False if expired.
    """
    current = int(time.time())
    return current <= expiry_timestamp

def check_root():
    """
    Check if running as root/administrator.
    """
    try:
        return os.geteuid() == 0
    except AttributeError:
        # Windows fallback
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

def check_virtual_env():
    """
    Check if running inside a virtual environment.
    """
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )

def check_debugger_processes():
    """
    Check for common debugger processes running.
    """
    debuggers = ['gdb', 'lldb', 'strace', 'ltrace', 'ida', 'ollydbg']
    try:
        output = subprocess.check_output(['ps', 'aux'], text=True)
        for dbg in debuggers:
            if dbg in output:
                return True
    except Exception:
        pass
    return False
