import os
from dotenv import load_dotenv
from data_manager import DataManager

class Customer:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.email = ""

    def register(self):
        print("Welcome to Ajit's Flight Club.")
        print("We find the best flight deals and email you.")
        
        self.first_name = input("What is your first name? \n")
        self.last_name = input("What is your last name? \n")

        self.email = self._get_valid_email()
        print("Welcome to the club!")

    def _get_valid_email(self):
        """Prompts the user to enter and confirm their email address."""
        while True:
            email = input("What is your email address? \n")
            confirm_email = input("Type your email address again for confirmation: \n")
            if email == confirm_email:
                return email
            print("Emails do not match. Please provide your email address again!")

def main():
    load_dotenv()

    # Create the Data Manager
    endpoint = os.getenv('SHEETY_ENDPOINT')
    bearer_token = os.getenv('SHEETY_BEARER_TOKEN')
    data_manager = DataManager(endpoint, bearer_token)

    # Register new customer
    new_customer = Customer()
    new_customer.register()
    data_manager.add_user(new_customer)

if __name__ == "__main__":
    main()
