from cryptography.fernet import Fernet
import os

def generate_fernet_key(key_name):
    """
    Generate a Fernet key and save it to a file, asking the user twice if they want to override an existing file.
    """
    if os.path.exists(key_name):
        user_response = input(f"{key_name} already exists. Do you want to override it? (yes/no): ").lower()
        if user_response != 'yes':
            print("Key generation aborted.")
            return
        if user_response == 'yes':
            # Double-check with the user
            double_check = input("\nAre you really sure you want to generate a new key and override the existing file? \n If YES, write 'I WANT TO OVERRIDE THE KEY' and press Enter \n : ").lower()
            if double_check.lower() != 'i want to override the key':
                print("Key generation aborted.")
                return

    key = Fernet.generate_key()

    with open(key_name, 'wb') as key_file:
        key_file.write(key)

    print(f"\nFernet key generated and saved as {key_name}")

if __name__ == "__main__":
    generate_fernet_key('enckey.key')
