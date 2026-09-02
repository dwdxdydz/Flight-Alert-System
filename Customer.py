import os
import re

from dotenv import load_dotenv

from data_manager import DataManager


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_valid_email() -> str:
    while True:
        email = input("Email: ").strip()
        confirmation = input("Confirm email: ").strip()
        if email == confirmation and EMAIL_PATTERN.match(email):
            return email
        print("Please enter a valid email address and confirm it correctly.")


def main() -> None:
    load_dotenv()

    data_manager = DataManager(
        os.getenv("SHEETY_ENDPOINT", ""),
        os.getenv("SHEETY_BEARER_TOKEN", ""),
    )

    print("\nWelcome to Flight Alert System!")
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = get_valid_email()

    data_manager.add_user(first_name, last_name, email)
    print("Subscription created successfully.")


if __name__ == "__main__":
    main()
