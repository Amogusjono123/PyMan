import os
import json
from cryptography.fernet import Fernet

# Generate a key and save it to a file (Run this once and save the key securely)
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the key from the file
def load_key():
    if not os.path.exists("key.key"):
        print("Key file not found. Generating a new key.")
        generate_key()
    return open("key.key", "rb").read()

# Encrypt a password
def encrypt_password(password, key):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode()).decode()

# Decrypt a password
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password.encode()).decode()

# Save passwords to a JSON file
def save_passwords(passwords, filename="passwords.json"):
    with open(filename, "w") as file:
        json.dump(passwords, file, indent=4)

# Load passwords from a JSON file
def load_passwords(filename="passwords.json"):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as file:
        return json.load(file)

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main function
def main():
    key = load_key()
    passwords = load_passwords()

    while True:
        clear_screen()  # Clear the screen before showing the menu

        print("\nPassword Manager")
        print("1. Add a new password")
        print("2. View passwords")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            clear_screen()  # Clear the screen before adding password
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            encrypted_password = encrypt_password(password, key)
            passwords[service] = {"username": username, "password": encrypted_password}
            save_passwords(passwords)
            print("Password saved successfully!")
            input("Press Enter to return to the menu...")

        elif choice == "2":
            clear_screen()  # Clear the screen before viewing passwords
            if not passwords:
                print("No passwords stored.")
            else:
                for service, creds in passwords.items():
                    username = creds["username"]
                    decrypted_password = decrypt_password(creds["password"], key)
                    print(f"Service: {service}\nUsername: {username}\nPassword: {decrypted_password}\n")
            input("Press Enter to return to the menu...")

        elif choice == "3":
            clear_screen()  # Clear the screen before exiting
            print("Exiting Password Manager.")
            break

        else:
            clear_screen()  # Clear the screen before showing error message
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
