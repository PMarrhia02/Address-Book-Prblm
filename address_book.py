import logging
import os
import re

# Setup logger to store logs inside the same directory as the script
log_filename = os.path.join(os.path.dirname(__file__), "address_book.log")
logging.basicConfig(
    filename=log_filename,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Contact:
    """
    A class to represent a contact with validation and duplicate check.
    """
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone, email):
        if not first_name or not last_name:
            raise ValueError("First and last name cannot be empty.")
        if not re.match(r"^\d{6}$", zip_code):
            raise ValueError("Invalid ZIP code! It must be a 6-digit number.")
        if not re.match(r"^\d{10,12}$", phone):
            raise ValueError("Invalid phone number! It must be 10 or 12 digits.")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            raise ValueError("Invalid email format! Example: name@example.com")
        
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.email = email
    
    def __eq__(self, other):
        return isinstance(other, Contact) and self.first_name == other.first_name and self.last_name == other.last_name

    def __str__(self):
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Address: {self.address}, {self.city}, {self.state}, {self.zip_code}\n"
                f"Phone: {self.phone}\n"
                f"Email: {self.email}\n")

class AddressBook:
    """
    A class to manage multiple contacts in an address book.
    """
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        if contact in self.contacts:
            logging.warning(f"Duplicate Entry Detected: {contact.first_name} {contact.last_name}")
            print(f"Contact '{contact.first_name} {contact.last_name}' already exists!")
        else:
            self.contacts.append(contact)
            logging.info(f"Contact Added: {contact.first_name} {contact.last_name}")
            print(f"\nContact '{contact.first_name} {contact.last_name}' added successfully!\n")
    
    def display_contacts(self):
        if not self.contacts:
            print("\nAddress Book is empty!\n")
        else:
            print("\nYour Address Book:")
            for contact in self.contacts:
                print(contact)

class AddressBookApp:
    """
    Main application interface for user interaction.
    """
    @staticmethod
    def get_validated_input(prompt, pattern, error_message):
        while True:
            user_input = input(prompt).strip()
            if re.match(pattern, user_input):
                return user_input
            print(error_message)

    @staticmethod
    def create_contact():
        try:
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            address = input("Enter Address: ").strip()
            city = input("Enter City: ").strip()
            state = input("Enter State: ").strip()
            zip_code = AddressBookApp.get_validated_input(
                "Enter ZIP Code (6 digits): ",
                r"^\d{6}$", "Invalid ZIP Code! Must be 6 digits."
            )
            phone = AddressBookApp.get_validated_input(
                "Enter Phone Number (10 or 12 digits): ",
                r"^\d{10,12}$", "Invalid Phone Number! Must be 10 or 12 digits."
            )
            email = AddressBookApp.get_validated_input(
                "Enter Email: ",
                r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", "Invalid Email! Please enter a valid email."
            )

            return Contact(first_name, last_name, address, city, state, zip_code, phone, email)
        except ValueError as e:
            logging.error(f"Error: {e}")
            print(f"Error: {e}")
            return None

def main():
    print("\nWelcome to the Address Book System!\n")
    address_book = AddressBook()

    while True:
        print("\nMenu:")
        print("1. Add Contact")
        print("2. Display Contacts")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            contact = AddressBookApp.create_contact()
            if contact:
                address_book.add_contact(contact)
        elif choice == "2":
            address_book.display_contacts()
        elif choice == "3":
            print("\nExiting Address Book. Goodbye!\n")
            break
        else:
            print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
