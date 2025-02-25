import logging
import os

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
    def __init__(self, name, phone, city, state):
        self.name = name
        self.phone = phone
        self.city = city
        self.state = state

    def __eq__(self, other):
        return isinstance(other, Contact) and self.name.lower() == other.name.lower()

    def __hash__(self):
        return hash(self.name.lower())

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, City: {self.city}, State: {self.state}"

class AddressBook:
    def __init__(self):
        self.contacts = set()  # Using a set to prevent duplicates

    def add_contact(self, contact):
        if contact in self.contacts:
            print(f" Duplicate entry found: {contact.name}. Cannot add again.")
            logging.info(f"Attempted to add duplicate contact: {contact.name}")
        else:
            self.contacts.add(contact)
            print(f" Contact added successfully: {contact.name}")
            logging.info(f"Added new contact: {contact}")

    def edit_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                new_phone = input(f"Enter new phone number for {name}: ")
                new_city = input(f"Enter new city for {name}: ")
                new_state = input(f"Enter new state for {name}: ")
                
                # Update contact details
                self.contacts.remove(contact)
                updated_contact = Contact(name, new_phone, new_city, new_state)
                self.contacts.add(updated_contact)

                print(f" Contact '{name}' updated successfully.")
                logging.info(f"Edited contact: {updated_contact}")
                return
        print(f" Contact '{name}' not found.")

    def delete_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                self.contacts.remove(contact)
                print(f" Contact '{name}' deleted successfully.")
                logging.info(f"Deleted contact: {contact.name}")
                return
        print(f" Contact '{name}' not found.")

    def display_contacts(self):
        if not self.contacts:
            print(" No contacts available in this Address Book.")
        else:
            print("\n Contacts in Address Book:")
            for contact in self.contacts:
                print(contact)

class AddressBookSystem:
    def __init__(self):
        self.address_books = {}  # Dictionary to store multiple address books

    def add_address_book(self, book_name):
        if book_name in self.address_books:
            print(f" Address Book '{book_name}' already exists.")
            logging.info(f"Attempted to add duplicate Address Book: {book_name}")
        else:
            self.address_books[book_name] = AddressBook()
            print(f" Address Book '{book_name}' created successfully.")
            logging.info(f"Created new Address Book: {book_name}")

    def get_address_book(self, book_name):
        return self.address_books.get(book_name, None)

    def display_address_books(self):
        if not self.address_books:
            print(" No Address Books available.")
        else:
            print("\n Available Address Books:")
            for book_name in self.address_books.keys():
                print(f"- {book_name}")

# Main Execution
if __name__ == "__main__":
    system = AddressBookSystem()

    while True:
        print("\n🔹 Address Book System Menu 🔹")
        print("1️ Add New Address Book")
        print("2️ Add Contact to Address Book")
        print("3️ Edit Contact")
        print("4️ Delete Contact")
        print("5️ Display Contacts in an Address Book")
        print("6️ Display All Address Books")
        print("7️ Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            book_name = input("Enter Address Book name: ")
            system.add_address_book(book_name)

        elif choice == "2":
            book_name = input("Enter Address Book name: ")
            book = system.get_address_book(book_name)
            if book:
                name = input("Enter Name: ")
                phone = input("Enter Phone Number: ")
                city = input("Enter City: ")
                state = input("Enter State: ")
                book.add_contact(Contact(name, phone, city, state))
            else:
                print(f" Address Book '{book_name}' not found.")

        elif choice == "3":
            book_name = input("Enter Address Book name: ")
            book = system.get_address_book(book_name)
            if book:
                name = input("Enter Name of Contact to Edit: ")
                book.edit_contact(name)
            else:
                print(f" Address Book '{book_name}' not found.")

        elif choice == "4":
            book_name = input("Enter Address Book name: ")
            book = system.get_address_book(book_name)
            if book:
                name = input("Enter Name of Contact to Delete: ")
                book.delete_contact(name)
            else:
                print(f" Address Book '{book_name}' not found.")

        elif choice == "5":
            book_name = input("Enter Address Book name: ")
            book = system.get_address_book(book_name)
            if book:
                book.display_contacts()
            else:
                print(f" Address Book '{book_name}' not found.")

        elif choice == "6":
            system.display_address_books()

        elif choice == "7":
            print(" Exiting Address Book System. Goodbye! 🔻")
            break

        else:
            print(" Invalid choice. Please enter a valid option.")
