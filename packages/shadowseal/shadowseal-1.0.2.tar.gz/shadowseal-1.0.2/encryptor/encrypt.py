import os
import sys
import time
import struct
import hashlib
import base64

VERSION = 1
BLOCK_SIZE = 16
ROUNDS = 1

def encrypt_char(c):
    return (ord(c) * 3 + 7) % 256

def decrypt_char(b):
    return chr((171 * (b - 7)) % 256)

def pad_data(data):
    padding_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    if padding_len == 0:
        padding_len = BLOCK_SIZE
    return data + bytes([padding_len] * padding_len)

def unpad_data(data):
    if not data:
        return data
    padding_len = data[-1]
    if padding_len == 0 or padding_len > BLOCK_SIZE:
        return data
    if data[-padding_len:] != bytes([padding_len] * padding_len):
        return data
    return data[:-padding_len]

def encrypt_data(data: bytes) -> bytes:
    data = pad_data(data)
    new_data = bytearray()
    for b in data:
        new_data.append(encrypt_char(chr(b)))
    return bytes(new_data)

def simple_checksum(data: bytes) -> int:
    csum = 0
    for b in data:
        csum = (csum + b) & 0xFFFFFFFF
    return csum

def pack_shc(encrypted_data: bytes, version: int = VERSION) -> bytes:
    checksum = simple_checksum(encrypted_data)
    timestamp = int(time.time())
    header = struct.pack('>I I Q', checksum, version, timestamp)
    return header + encrypted_data

def encrypt_file(input_path: str, output_path: str):
    if not input_path.endswith('.py'):
        raise ValueError("Input file must be a .py file")
    with open(input_path, 'rb') as f:
        data = f.read()
    data = base64.b64encode(data)
    encrypted = encrypt_data(data)
    packed = pack_shc(encrypted)
    with open(output_path, 'wb') as f:
        f.write(packed)
    print(f"Encrypted {input_path} -> {output_path}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Basic single-round encrypt Python file to .shc')
    parser.add_argument('input', help='Input .py file')
    parser.add_argument('-o', '--output', help='Output .shc file', required=True)
    args = parser.parse_args()
    encrypt_file(args.input, args.output)

if __name__ == '__main__':
    main()
