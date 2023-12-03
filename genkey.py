from cryptography.fernet import Fernet

def generate_fernet_key():
    """
    Generate a Fernet key and save it to a file.
    """
    key = Fernet.generate_key()

    with open("enckey.key", 'wb') as key_file:
        key_file.write(key)

    print("Fernet key generated and saved to 'enckey.key'.")

if __name__ == "__main__":
    generate_fernet_key()

