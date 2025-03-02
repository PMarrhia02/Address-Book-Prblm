import re
import os
import logging

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(SCRIPT_DIR, "address_book.log")


# Setup logger to ensure logs are appended to the same file
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
log_file_path = os.path.join(script_dir, "address_book.log")

logging.basicConfig(
    filename=log_file_path,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.info("Address Book System - Logging started.")


# Global address book dictionary
address_book = {}

class ContactError(Exception):
    """Custom exception for contact-related errors."""
    pass

def validate_zip_code(zip_code):
    """Validate that the ZIP code is a 6-digit number.

    Args:
        zip_code: The ZIP code to validate.

    Returns:
        str: Validated ZIP code as a string.

    Raises:
        ContactError: If the ZIP code is not a 6-digit number.
    """
    cleaned_zip = zip_code.strip()
    if not re.match(r"^\d{6}$", cleaned_zip):
        raise ContactError("ZIP code must be a 6-digit number.")
    return cleaned_zip

def validate_phone_number(phone):
    """Validate that the phone number is 10 or 12 digits.

    Args:
        phone: The phone number to validate.

    Returns:
        str: Validated phone number as a string.

    Raises:
        ContactError: If the phone number is not 10 or 12 digits.
    """
    cleaned_phone = phone.strip()
    if not re.match(r"^\d{10}$|^\d{12}$", cleaned_phone):
        raise ContactError("Phone number must be 10 or 12 digits.")
    return cleaned_phone

def validate_email(email):
    """Validate that the email contains '@' and '.' characters.

    Args:
        email: The email address to validate.

    Returns:
        str: Validated email address.

    Raises:
        ContactError: If the email format is invalid.
    """
    cleaned_email = email.strip()
    if "@" not in cleaned_email or "." not in cleaned_email:
        raise ContactError("Email must contain '@' and '.' characters.")
    return cleaned_email

def create_contact():
    """Create a new contact and add it to the address book.

    Collects user input for contact details, validates them, and stores them in the global
    address_book dictionary with the full name as the key.

    Raises:
        ContactError: If any validation fails during contact creation.
    """
    try:
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        address = input("Enter Address: ").strip()
        city = input("Enter City: ").strip()
        state = input("Enter State: ").strip()

        if not all([first_name, last_name, address, city, state]):
            raise ContactError("All fields (name, address, city, state) must be non-empty.")

        # Validate ZIP code with retry loop
        while True:
            try:
                zip_code = validate_zip_code(input("Enter ZIP Code: ").strip())
                break
            except ContactError as e:
                logging.error(f"ZIP code input error: {e}")
                print(f"Invalid ZIP Code! {e} Please enter again.")

        # Validate phone number with retry loop
        while True:
            try:
                phone = validate_phone_number(input("Enter Phone Number: ").strip())
                break
            except ContactError as e:
                logging.error(f"Phone number input error: {e}")
                print(f"Invalid Phone Number! {e} Please enter again.")

        # Validate email with retry loop
        while True:
            try:
                email = validate_email(input("Enter Email: ").strip())
                break
            except ContactError as e:
                logging.error(f"Email input error: {e}")
                print(f"Invalid Email! {e} Please enter again.")

        # Store contact in address_book
        contact_name = f"{first_name} {last_name}"
        address_book[contact_name] = {
            "Address": address,
            "City": city,
            "State": state,
            "ZIP": zip_code,
            "Phone": phone,
            "Email": email
        }

        logging.info(f"Contact '{contact_name}' added successfully")
        print(f"\nContact '{contact_name}' added successfully!\n")
        print(address_book[contact_name])

    except ContactError as e:
        logging.error(f"Contact creation failed: {e}")
        print(f"Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in create_contact: {e}")
        print(f"An unexpected error occurred: {e}")

def main():
    """Run the Address Book application to create a contact."""
    try:
        print("Welcome to Address Book")
        create_contact()
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
        print("\nProgram terminated by user.")
    except Exception as e:
        logging.error(f"Unexpected error in main: {e}")
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    main()