from cryptography.fernet import Fernet

def generate_fernet_key(key_name):
    """
    Generate a Fernet key and save it to a file.
    """
    key = Fernet.generate_key()

    with open(key_name, 'wb') as key_file:
        key_file.write(key)

    print("Fernet key generated and saved to 'enckey.key'.")

if __name__ == "__main__":
    generate_fernet_key('enckey.key')

