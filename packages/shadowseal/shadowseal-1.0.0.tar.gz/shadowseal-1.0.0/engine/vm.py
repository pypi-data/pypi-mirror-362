import types

class EncryptedVM:
    def __init__(self, key=0x5A):
        self.key = key

    def decrypt_char(self, b):
        return ((183 * ((b - 13) % 256)) % 256) ^ self.key

    def decrypt_data(self, data: bytes) -> bytes:
        return bytes(self.decrypt_char(b) for b in data)

    def run_encrypted_code(self, encrypted_data: bytes, filename='<encrypted>'):
        decrypted_data = self.decrypt_data(encrypted_data)
        try:
            code_str = decrypted_data.decode('utf-8')
            code_obj = compile(code_str, filename, 'exec')
            exec(code_obj, globals())
        except Exception as e:
            print("VM execution error:", e)
