import os
import struct
import sys

BLOCK_SIZE = 16
ROUNDS = 1

def decrypt_char(b):
    return (171 * (b - 7)) % 256

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

def decrypt_block(block):
    return bytes(decrypt_char(b) for b in block)

def decrypt_data(data):
    new_data = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        new_data.extend(decrypt_block(block))
    data = bytes(new_data)
    data = unpad_data(data)
    return data

def simple_checksum(data):
    csum = 0
    for b in data:
        csum = (csum + b) & 0xFFFFFFFF
    return csum

from utils.anti_debug import anti_debug

def run_shc(filepath):
    try:
        if anti_debug():
            print("Debugging detected. Exiting.")
            return

        if not os.path.isfile(filepath):
            print(f"File not found: {filepath}")
            return

        with open(filepath, 'rb') as f:
            header = f.read(16)
            if len(header) != 16:
                print("Invalid file format.")
                return
            checksum, version, timestamp = struct.unpack('>I I Q', header)
            encrypted_data = f.read()

        computed_checksum = simple_checksum(encrypted_data)
        if computed_checksum != checksum:
            print("Checksum mismatch. File corrupted or tampered.")
            return

        data = decrypt_data(encrypted_data)

        import base64
        decoded_data = base64.b64decode(data)
        code_str = decoded_data.decode('utf-8')
        code_obj = compile(code_str, filepath, 'exec')
        exec(code_obj, globals())

    except Exception as e:
        print("Execution error:", e)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run encrypted .shc Python file')
    parser.add_argument('filepath', help='Path to the encrypted .shc file')
    args = parser.parse_args()
    run_shc(args.filepath)

if __name__ == '__main__':
    main()
