import re
import os
import logging

# Configure logging (log file stored in the same directory)
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "address_book.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Contact:
    """Class representing a contact in the Address Book."""
    
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, email):
        """Initialize a new Contact object with validation."""
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = self.validate_zip(zip_code)
        self.phone_number = self.validate_phone(phone_number)
        self.email = self.validate_email(email)
        
        # Log successful contact creation
        logging.info(f"New contact created: {self.first_name} {self.last_name}")

    def validate_zip(self, zip_code):
        """Validate zip code (must be exactly 6 digits)."""
        if not re.match(r'^\d{6}$', zip_code):
            logging.error(f"Invalid ZIP Code: {zip_code}")
            raise ValueError("Invalid ZIP Code. It should be exactly 6 digits.")
        return zip_code

    def validate_phone(self, phone_number):
        """Validate phone number (must be either 10 or 12 digits)."""
        if not re.match(r'^\d{10}$|^\d{12}$', phone_number):
            logging.error(f"Invalid Phone Number: {phone_number}")
            raise ValueError("Invalid Phone Number. It should be exactly 10 or 12 digits.")
        return phone_number

    def validate_email(self, email):
        """Validate email using regex."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            logging.error(f"Invalid Email: {email}")
            raise ValueError("Invalid Email Address.")
        return email

# Main Execution (For Testing Use Case 1)
if __name__ == "__main__":
    try:
        print("Enter Contact Details:")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        address = input("Address: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("ZIP Code (6 digits): ")
        phone_number = input("Phone Number (10 or 12 digits): ")
        email = input("Email: ")

        # Create a new Contact object
        contact = Contact(first_name, last_name, address, city, state, zip_code, phone_number, email)
        print("Contact created successfully!")

    except ValueError as ve:
        print(f"Error: {ve}")

    except Exception as e:
        print(f"Unexpected Error: {e}")
