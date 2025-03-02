import logging
import os
import re

# Setup logger to ensure logs are appended to the same file
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
log_file_path = os.path.join(script_dir, "address_book.log")

logging.basicConfig(
    filename=log_file_path,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.info("Address Book Program - Logging started.")


class ContactPerson:
    """
    Represents a contact person with validated personal details.
    """
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def __init__(self, first_name, last_name, address, city, state, zip_code, phone, email):
        try:
            self.validate_inputs(first_name, last_name, zip_code, phone, email)
            self.first_name = first_name
            self.last_name = last_name
            self.address = address
            self.city = city
            self.state = state
            self.zip_code = zip_code
            self.phone = phone
            self.email = email
            logging.info(f"Contact created: {self.first_name} {self.last_name}")
        except ValueError as e:
            logging.error(f"Error creating contact: {e}")
            raise

    @staticmethod
    def validate_inputs(first_name, last_name, zip_code, phone, email):
        """ Validates the input data for a contact person. """
        if not first_name or not last_name:
            raise ValueError("First and last name cannot be empty.")
        if not isinstance(zip_code, int) or not re.fullmatch(r"\d{6}", str(zip_code)):
            raise ValueError("ZIP code must be a 6-digit number.")
        if not isinstance(phone, int) or not re.fullmatch(r"\d{10,12}", str(phone)):
            raise ValueError("Phone number must be 10 or 12 digits long.")
        if not re.match(ContactPerson.EMAIL_REGEX, email):
            raise ValueError("Invalid email format.")

    def __str__(self):
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Address: {self.address}, {self.city}, {self.state}, {self.zip_code}\n"
                f"Phone: {self.phone}\n"
                f"Email: {self.email}\n")

class AddressBook:
    """
    Manages multiple contact entries in an address book.
    """
    def __init__(self):
        self.contacts = {}
        logging.info("Address book initialized.")

    def add_contact(self, contact):
        """ Adds a new contact to the address book. """
        try:
            if not isinstance(contact, ContactPerson):
                raise TypeError("Invalid contact type. Must be a ContactPerson instance.")
            full_name = f"{contact.first_name} {contact.last_name}"
            if full_name in self.contacts:
                logging.warning(f"Contact '{full_name}' already exists.")
            else:
                self.contacts[full_name] = contact
                logging.info(f"Contact '{full_name}' added successfully!")
        except Exception as e:
            logging.error(f"Error adding contact: {e}")

    def edit_contact(self, name, updated_contact):
        """ Edits an existing contact in the address book. """
        try:
            if name in self.contacts:
                self.contacts[name] = updated_contact
                logging.info(f"Contact '{name}' updated successfully!")
            else:
                logging.warning(f"Contact '{name}' not found in the address book.")
        except Exception as e:
            logging.error(f"Error editing contact: {e}")

    def display_contacts(self):
        """ Displays all contacts in the address book. """
        try:
            if not self.contacts:
                logging.info("Address book is empty.")
                print("\nAddress Book is empty!\n")
            else:
                for contact in self.contacts.values():
                    print(contact)
                    logging.info(f"Displayed contact: {contact.first_name} {contact.last_name}")
        except Exception as e:
            logging.error(f"Error displaying contacts: {e}")

class AddressBookMain:
    """ Provides the main interface for the address book system. """
    @staticmethod
    def get_validated_input(prompt, pattern, error_message):
        """ Gets validated user input based on a regex pattern. """
        while True:
            try:
                user_input = input(prompt).strip()
                if re.fullmatch(pattern, user_input):
                    return user_input
                logging.warning(error_message)
                print(error_message)
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                print(f"Unexpected error: {e}")

    @staticmethod
    def create_contact():
        """ Collects user input and creates a new contact. """
        try:
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            address = input("Enter Address: ").strip()
            city = input("Enter City: ").strip()
            state = input("Enter State: ").strip()

            zip_code = AddressBookMain.get_validated_input("Enter ZIP Code (6 digits): ", r"\d{6}", "Invalid ZIP Code! It must be a 6-digit number.")
            phone = AddressBookMain.get_validated_input("Enter Phone Number (10 or 12 digits): ", r"\d{10,12}", "Invalid Phone Number! It must be 10 or 12 digits long.")
            email = AddressBookMain.get_validated_input("Enter Email: ", ContactPerson.EMAIL_REGEX, "Invalid Email! Please enter a valid email address.")

            return ContactPerson(first_name, last_name, address, city, state, int(zip_code), int(phone), email)
        except Exception as e:
            logging.error(f"Error creating contact: {e}")
            return None

def main():
    """ Entry point of the program. Manages address book operations. """
    logging.info("Address Book Application Started")
    address_book = AddressBook()

    while True:
        try:
            print("\nMenu:")
            print("1. Add Contact")
            print("2. Display Contacts")
            print("3. Edit Contact")
            print("4. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                contact = AddressBookMain.create_contact()
                if contact:
                    address_book.add_contact(contact)
            elif choice == "2":
                address_book.display_contacts()
            elif choice == "3":
                name = input("Enter full name of the contact to edit: ").strip()
                updated_contact = AddressBookMain.create_contact()
                if updated_contact:
                    address_book.edit_contact(name, updated_contact)
            elif choice == "4":
                logging.info("Exiting Address Book. Goodbye!")
                print("\nExiting Address Book. Goodbye!\n")
                break
            else:
                logging.warning("Invalid choice! Please select a valid option.")
                print("Invalid choice! Please select a valid option.")
        except Exception as e:
            logging.critical(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
    
