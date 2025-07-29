import os
import sys
import ctypes
import platform
import subprocess

def check_ptrace():
    return False

def check_debugger_processes():
    debuggers = ['gdb', 'lldb', 'strace', 'ltrace', 'ida', 'ollydbg', 'x64dbg', 'windbg']
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("tasklist", shell=True, text=True)
        else:
            output = subprocess.check_output(["ps", "aux"], text=True)
        for dbg in debuggers:
            if dbg.lower() in output.lower():
                return True
    except Exception:
        pass
    return False

def check_debugger_env():
    debugger_vars = ['LD_PRELOAD', 'PYTHONBREAKPOINT', 'PYTHONINSPECT']
    for var in debugger_vars:
        if os.environ.get(var):
            return True
    return False

def check_tracerpid():
    if platform.system() != "Linux":
        return False
    try:
        with open("/proc/self/status", "r") as f:
            for line in f:
                if line.startswith("TracerPid:"):
                    tracerpid = int(line.split()[1])
                    if tracerpid != 0:
                        return True
    except Exception:
        pass
    return False

def anti_debug():
    if check_ptrace():
        return True
    if check_debugger_processes():
        return True
    if check_debugger_env():
        return True
    if check_tracerpid():
        return True
    if sys.gettrace() is not None:
        return True
    return False
