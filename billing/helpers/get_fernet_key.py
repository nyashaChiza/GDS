from cryptography.fernet import Fernet

def generate_key():
    
    # Generate a key
    key = Fernet.generate_key()

    # Print the key, and you'll need to store this securely
    return key.decode()
