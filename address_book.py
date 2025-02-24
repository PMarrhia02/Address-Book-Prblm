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

logging.info("Address Book System - Logging started.")


class Contact:
    """
    A class to represent a contact with validation.
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

    def __str__(self):
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Address: {self.address}, {self.city}, {self.state}, {self.zip_code}\n"
                f"Phone: {self.phone}\n"
                f"Email: {self.email}\n")


class AddressBook:
    """
    A class to manage multiple contacts within an Address Book.
    """

    def __init__(self, name):
        self.name = name
        self.contacts = {}

    def add_contact(self, contact):
        """
        Add a new contact to the address book.
        """
        if not isinstance(contact, Contact):
            raise TypeError("Invalid contact type. Must be a Contact instance.")

        full_name = f"{contact.first_name} {contact.last_name}"
        if full_name in self.contacts:
            logging.warning(f"Attempted to add duplicate contact in {self.name}: {full_name}")
            print(f"Contact '{full_name}' already exists in '{self.name}'!")
        else:
            self.contacts[full_name] = contact
            logging.info(f"Contact added in {self.name}: {full_name}")
            print(f"\nContact '{full_name}' added successfully to '{self.name}'!\n")

    def delete_contact(self, name):
        """
        Delete a contact by name.
        """
        if name in self.contacts:
            del self.contacts[name]
            logging.info(f"Contact deleted from {self.name}: {name}")
            print(f"Contact '{name}' deleted successfully from '{self.name}'!\n")
        else:
            logging.warning(f"Attempted to delete non-existent contact in {self.name}: {name}")
            print(f"Contact '{name}' not found in '{self.name}'!\n")

    def display_contacts(self):
        """
        Display all contacts in the address book.
        """
        if not self.contacts:
            logging.info(f"Displayed Address Book '{self.name}': Empty")
            print(f"\nAddress Book '{self.name}' is empty!\n")
        else:
            logging.info(f"Displayed Address Book '{self.name}' Contacts")
            print(f"\nContacts in Address Book '{self.name}':")
            for contact in self.contacts.values():
                print(contact)


class AddressBookSystem:
    """
    A class to manage multiple Address Books.
    """

    def __init__(self):
        self.address_books = {}

    def add_address_book(self, name):
        """
        Add a new Address Book.
        """
        if name in self.address_books:
            logging.warning(f"Attempted to add duplicate Address Book: {name}")
            print(f"Address Book '{name}' already exists!")
        else:
            self.address_books[name] = AddressBook(name)
            logging.info(f"New Address Book created: {name}")
            print(f"\nAddress Book '{name}' created successfully!\n")

    def get_address_book(self, name):
        """
        Retrieve an Address Book by name.
        """
        return self.address_books.get(name)


class AddressBookApp:
    """
    Main application interface for user interaction.
    """

    @staticmethod
    def create_contact():
        """
        Create a new contact with user input.
        """
        try:
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            address = input("Enter Address: ").strip()
            city = input("Enter City: ").strip()
            state = input("Enter State: ").strip()
            zip_code = input("Enter ZIP Code (6 digits): ").strip()
            phone = input("Enter Phone Number (10 or 12 digits): ").strip()
            email = input("Enter Email: ").strip()

            return Contact(first_name, last_name, address, city, state, zip_code, phone, email)
        except ValueError as e:
            logging.error(f"Error creating contact: {e}")
            print(f"Error: {e}")
            return None

    @staticmethod
    def select_address_book(system):
        """
        Allow user to select an existing Address Book.
        """
        if not system.address_books:
            print("\nNo Address Books available. Please create one first.\n")
            return None

        print("\nAvailable Address Books:")
        for book_name in system.address_books.keys():
            print(f"- {book_name}")

        selected_name = input("\nEnter the Address Book name: ").strip()
        address_book = system.get_address_book(selected_name)

        if address_book:
            return address_book
        else:
            print("\nAddress Book not found! Try again.\n")
            return None


def main():
    print("\nWelcome to the Multi-Address Book System!\n")
    system = AddressBookSystem()

    while True:
        print("\nMenu:")
        print("1. Create New Address Book")
        print("2. Add Contact to an Address Book")
        print("3. Delete Contact from an Address Book")
        print("4. Display Contacts in an Address Book")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter the name of the new Address Book: ").strip()
            system.add_address_book(name)
        elif choice == "2":
            address_book = AddressBookApp.select_address_book(system)
            if address_book:
                contact = AddressBookApp.create_contact()
                if contact:
                    address_book.add_contact(contact)
        elif choice == "3":
            address_book = AddressBookApp.select_address_book(system)
            if address_book:
                name = input("Enter the full name of the contact to delete: ").strip()
                address_book.delete_contact(name)
        elif choice == "4":
            address_book = AddressBookApp.select_address_book(system)
            if address_book:
                address_book.display_contacts()
        elif choice == "5":
            logging.info("Exiting Address Book Application.")
            print("\nExiting Multi-Address Book System. Goodbye!\n")
            break
        else:
            logging.warning(f"Invalid menu choice: {choice}")
            print("Invalid choice! Please select a valid option.")


if __name__ == "__main__":
    main()
