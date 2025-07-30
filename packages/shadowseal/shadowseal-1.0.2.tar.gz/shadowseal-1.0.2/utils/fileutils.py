"""
Advanced file utilities for shadowcrypt package.

Provides robust file handling, checksum calculation, and safe file operations.
"""

import os
import hashlib
import shutil

def read_file_bytes(path):
    """
    Read the entire file content as bytes.

    Args:
        path (str): File path.

    Returns:
        bytes: File content.
    """
    with open(path, 'rb') as f:
        return f.read()

def write_file_bytes(path, data):
    """
    Write bytes data to a file safely.

    Args:
        path (str): File path.
        data (bytes): Data to write.
    """
    temp_path = path + '.tmp'
    with open(temp_path, 'wb') as f:
        f.write(data)
    os.replace(temp_path, path)

def file_exists(path):
    """
    Check if a file exists.

    Args:
        path (str): File path.

    Returns:
        bool: True if file exists, else False.
    """
    return os.path.isfile(path)

def get_file_size(path):
    """
    Get the size of a file in bytes.

    Args:
        path (str): File path.

    Returns:
        int: File size in bytes.
    """
    return os.path.getsize(path)

def compute_sha256(path):
    """
    Compute SHA256 checksum of a file.

    Args:
        path (str): File path.

    Returns:
        str: Hexadecimal SHA256 digest.
    """
    sha256_hash = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def safe_delete(path):
    """
    Safely delete a file if it exists.

    Args:
        path (str): File path.
    """
    try:
        if file_exists(path):
            os.remove(path)
    except Exception:
        pass

def copy_file(src, dst):
    """
    Copy a file from src to dst.

    Args:
        src (str): Source file path.
        dst (str): Destination file path.
    """
    shutil.copy2(src, dst)
