import argparse
from encryptor import encrypt
from runner import loader

def main():
    parser = argparse.ArgumentParser(
        description=(
            "ShadowSeal - Author: 〲ɱ๏ɳᴀʳᴄʜ ⌾ғ sʜᴀᴅᴏᴡˢ〴 [Monarch of Shadows]\n\n"),
        usage=("shadowseal {encrypt,run} ...\n"
                 "  shadowseal encrypt <script>.py [-o <output>.shc]\n"
                 "  shadowseal run <script>.shc"),
    )
    subparsers = parser.add_subparsers(dest='command')

    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a Python file')
    encrypt_parser.add_argument('input', help='Input Python (.py) file to encrypt')
    encrypt_parser.add_argument('-o', '--output', required=True, help='Output encrypted .shc file')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run an encrypted .shc file')
    run_parser.add_argument('file', help='Encrypted .shc file to run')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == 'encrypt':
        print(f"Encrypting {args.input} to {args.output} ...")
        encrypt.encrypt_file(args.input, args.output)
        print("Encryption complete.")
        print("\\nEncryption details:")
        print(" - Uses a custom reversible math-based algorithm: E(x) = (ord(char) * 3 + 7) % 256")
        print(" - Output file format: binary packed blob + metadata (SHA256 hash, version, timestamp)")
        print(" - No RSA/ECC or cryptography libraries used.")
        print(" - Encrypted file extension: .shc")
        print("\\nExample usage:")
        print("  shadowseal encrypt script.py -o script.shc")
        print("  shadowseal run script.shc")
    elif args.command == 'run':
        loader.run_shc(args.file)

if __name__ == '__main__':
    main()
