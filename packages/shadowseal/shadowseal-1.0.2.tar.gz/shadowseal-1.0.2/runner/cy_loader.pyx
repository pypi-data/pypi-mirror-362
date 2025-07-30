from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cpython.ref cimport PyObject
from libc.stdio cimport FILE, fopen, fread, fclose, fseek, ftell, SEEK_END, SEEK_SET, sscanf
from libc.stdlib cimport malloc, free
from libc.string cimport memset, memcpy, strcmp
from libc.time cimport time

import sys
import os
import builtins

cdef unsigned char decrypt_char(unsigned char b):
    # Reverse of E(x) = (x*3 + 7) % 256
    # Modular inverse of 3 mod 256 is 171
    return (171 * (b - 7)) % 256

cdef int check_ptrace():
    # Linux ptrace detection by reading /proc/self/status using Python file IO
    try:
        with open("/proc/self/status", "r") as f:
            for line in f:
                if line.startswith("TracerPid:"):
                    tracerpid = int(line.split()[1])
                    if tracerpid != 0:
                        return 1
                    else:
                        return 0
    except:
        return 0
    return 0

cdef int check_ld_preload():
    # Check if LD_PRELOAD is set
    cdef bytes ld = os.environ.get("LD_PRELOAD", "").encode()
    if ld:
        return 1
    return 0

cdef int check_debugger():
    # Check sys.gettrace
    if sys.gettrace() is not None:
        return 1
    return 0

cdef int check_proc_debug():
    # Check for presence of gdb or strace in /proc/self/maps or /proc/self/status
    try:
        with open("/proc/self/maps", "r") as f:
            maps = f.read()
            if "gdb" in maps or "strace" in maps:
                return 1
    except:
        pass
    return 0

cdef int anti_debug():
    if check_ptrace():
        return 1
    if check_ld_preload():
        return 1
    if check_debugger():
        return 1
    if check_proc_debug():
        return 1
    return 0

cdef void secure_memzero(void* ptr, size_t len):
    # Securely zero memory
    cdef volatile char* p = <volatile char*>ptr
    cdef size_t i
    for i in range(len):
        p[i] = 0

cdef unsigned char* decrypt_data(unsigned char* data, size_t length):
    cdef unsigned char* decrypted = <unsigned char*>PyMem_Malloc(length)
    if not decrypted:
        return NULL
    cdef size_t i
    for i in range(length):
        decrypted[i] = decrypt_char(data[i])
    return decrypted

def run_shc(str filepath):
    if anti_debug():
        print("Debugging detected. Exiting.")
        return

    cdef FILE* f = fopen(filepath.encode('utf-8'), b"rb")
    if not f:
        print("Failed to open file.")
        return

    cdef unsigned char header[44]
    cdef size_t read_bytes = fread(header, 1, 44, f)
    if read_bytes != 44:
        fclose(f)
        print("Invalid file format.")
        return

    # Parse header: 32 bytes hash, 4 bytes version, 8 bytes timestamp
    cdef unsigned char* hash_digest = header
    cdef unsigned int version = (header[32] << 24) | (header[33] << 16) | (header[34] << 8) | header[35]
    cdef unsigned long long timestamp = 0
    cdef int i
    for i in range(8):
        timestamp = (timestamp << 8) | header[36 + i]

    # Read encrypted data
    fseek(f, 0, SEEK_END)
    cdef size_t file_size = ftell(f)
    cdef size_t data_size = file_size - 44
    fseek(f, 44, SEEK_SET)

    cdef unsigned char* encrypted_data = <unsigned char*>PyMem_Malloc(data_size)
    if not encrypted_data:
        fclose(f)
        print("Memory allocation failed.")
        return

    read_bytes = fread(encrypted_data, 1, data_size, f)
    fclose(f)
    if read_bytes != data_size:
        PyMem_Free(encrypted_data)
        print("Failed to read encrypted data.")
        return

    # Decrypt data
    cdef unsigned char* decrypted_data = decrypt_data(encrypted_data, data_size)
    PyMem_Free(encrypted_data)
    if not decrypted_data:
        print("Decryption failed.")
        return

    # Verify hash
    import hashlib
    cdef bytes decrypted_bytes = bytes([decrypted_data[i] for i in range(data_size)])
    cdef bytes computed_hash = hashlib.sha256(decrypted_bytes).digest()
    if computed_hash != bytes(hash_digest[:32]):
        secure_memzero(decrypted_data, data_size)
        PyMem_Free(decrypted_data)
        print("Hash mismatch. File corrupted or tampered.")
        return

    # Execute code in memory without storing plaintext string
    # Use builtins.exec with a code object compiled from decrypted bytes
    try:
        code_obj = compile(decrypted_bytes.decode('utf-8'), filepath, 'exec')
        exec(code_obj, globals(), globals())
    except Exception as e:
        print("Execution error:", e)

    # Securely clear decrypted data from memory
    secure_memzero(decrypted_data, data_size)
    PyMem_Free(decrypted_data)
