import os
import re
from dotenv import load_dotenv
from data_manager import DataManager

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def get_valid_email() -> str:
    while True:
        email, confirmation = input("Email: ").strip(), input("Confirm email: ").strip()
        if email == confirmation and EMAIL_PATTERN.match(email): return email
        print("Please enter a valid email address and confirm it correctly.")

def main() -> None:
    load_dotenv()
    manager = DataManager(os.getenv("SHEETY_ENDPOINT",""), os.getenv("SHEETY_BEARER_TOKEN",""))
    print("\nWelcome to Flight Alert System!")
    first, last = input("First name: ").strip(), input("Last name: ").strip()
    manager.add_user(first, last, get_valid_email())
    print("Subscription created successfully.")

if __name__ == "__main__":
    main()
