import re 
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
    """
    Description:
        Represents a contact in an address book.

    Parameters:
        name (str): Name of the contact.
        phone (str): Phone number of the contact.
        email (str): Email address of the contact.
        address (str): Street address of the contact.
        city (str): City where the contact resides.
        state (str): State where the contact resides.

    Raises:
        ValueError: If name is empty, phone is invalid, or email format is incorrect.
    """
    def __init__(self, name, phone, email, address, city, state):
        if not name:
            raise ValueError("Name cannot be empty.")
        if not re.match(r"^\d{10,12}$", phone):
            raise ValueError("Phone number must be 10 or 12 digits long.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        logging.info(f"Contact created: {self.name}")
    
    def __eq__(self, other):
        """
        Description:
            Checks equality between two contacts based on name (case insensitive).
        
        Parameters:
            other (Contact): Another contact to compare.
        
        Returns:
            bool: True if names match (case insensitive), False otherwise.
        """
        if isinstance(other, Contact):
            return self.name.lower() == other.name.lower()
        return False

    def __hash__(self):
        """
        Description:
            Defines a unique hash for a contact based on its name.
        
        Returns:
            int: Hash of the contact name.
        """
        return hash(self.name.lower())
    
    def __str__(self):
        """
        Description:
            Returns a formatted string representation of the contact.
        
        Returns:
            str: Formatted contact details.
        """
        return f"{self.name} | {self.phone} | {self.email} | {self.address}, {self.city}, {self.state}"

class AddressBook:
    """
    Description:
        Represents an address book that stores multiple contacts.
    
    Parameters:
        book_name (str): Name of the address book.
    
    Attributes:
        contacts (set): A set of Contact objects.
    """
    def __init__(self, book_name):
        self.book_name = book_name
        self.contacts = set()
        logging.info(f"Address Book '{book_name}' created.")

    def add_contact(self, name, phone, email, address, city, state):
        """
        Description:
            Adds a new contact to the address book if it does not already exist.
        
        Parameters:
            name (str): Contact name.
            phone (str): Phone number.
            email (str): Email address.
            address (str): Street address.
            city (str): City.
            state (str): State.

        Raises:
            ValueError: If contact details are invalid.
        """
        try:
            contact = Contact(name, phone, email, address, city, state)
            if contact in self.contacts:
                logging.warning(f"Duplicate contact '{name}' not added.")
                print(f"Error: Contact '{name}' already exists in {self.book_name}.")
            else:
                self.contacts.add(contact)
                logging.info(f"Contact '{name}' added to {self.book_name}.")
        except ValueError as e:
            logging.error(f"Error adding contact: {e}")
            print(f"Error: {e}")

    def display_contacts(self):
        """
        Description:
            Displays all contacts in the address book.
        """
        if not self.contacts:
            print(f"{self.book_name} Address Book is empty.")
            logging.info(f"{self.book_name} Address Book is empty.")
            return
        print(f"\nContacts in {self.book_name}:")
        for contact in self.contacts:
            print(contact)
            logging.info(f"Displayed contact: {contact.name}")

    def edit_contact(self, name, updated_contact):
        """
        Description:
            Edits an existing contact in the address book.
        
        Parameters:
            name (str): Full name of the contact to be edited.
            updated_contact (Contact): Updated contact object.
        """
        try:
            for contact in self.contacts:
                if contact.name.lower() == name.lower():
                    self.contacts.remove(contact)
                    self.contacts.add(updated_contact)
                    logging.info(f"Contact '{name}' updated successfully!")
                    print(f"Contact '{name}' updated successfully!")
                    return
            logging.warning(f"Contact '{name}' not found in the address book.")
            print(f"Contact '{name}' not found in the address book.")
        except Exception as e:
            logging.error(f"Error editing contact: {e}")
            print(f"Error editing contact: {e}")

    def delete_contact(self, name):
        """
        Description:
            Deletes a contact from the address book.

        Parameters:
            name (str): Full name of the contact to be deleted.
        
        Returns:
            KeyError: If the contact does not exist.
        """
        try:
            for contact in self.contacts:
                if contact.name.lower() == name.lower():
                    self.contacts.remove(contact)
                    logging.info(f"Contact '{name}' deleted successfully!")
                    print(f"Contact '{name}' has been deleted.")
                    return
            logging.warning(f"Contact '{name}' not found in the address book.")
            print(f"Contact '{name}' not found.")
        except Exception as e:
            logging.error(f"Error deleting contact: {e}")
            print(f"Error deleting contact: {e}")

class AddressBookSystem:
    """
    Description:
        Manages multiple address books.

    Attributes:
        address_books (dict): Dictionary to store multiple address books.
    """
    def __init__(self):
        self.address_books = {}
        logging.info("Address Book System initialized.")

    def add_address_book(self, book_name):
        """
        Description:
            Creates a new address book if it does not already exist.
        
        Parameters:
            book_name (str): Name of the address book.
        """
        if book_name in self.address_books:
            print(f"Address Book '{book_name}' already exists!")
            logging.warning(f"Address Book '{book_name}' already exists!")
        else:
            self.address_books[book_name] = AddressBook(book_name)
            print(f"Address Book '{book_name}' created.")
            logging.info(f"Address Book '{book_name}' created.")

    def get_address_book(self, book_name):
        """
        Description:
            Retrieves an address book by name.
        
        Parameters:
            book_name (str): Name of the address book.
        
        Returns:
            AddressBook: The requested address book or None if not found.
        """
        return self.address_books.get(book_name, None)

    def display_all_books(self):
        """
        Description:
            Displays all available address books.
        """
        if not self.address_books:
            print("No Address Books available.")
            logging.info("No Address Books available.")
        else:
            print("\nAvailable Address Books:")
            for book_name in self.address_books:
                print(f"- {book_name}")
                logging.info(f"Displayed Address Book: {book_name}")
    
    def search_person_city(self, city=None):
        """
        Description:
            Searches for contacts based only on city across multiple address books.

        Parameters:
            city (str, optional): City to search.

        Returns:
            list: List of matching Contact objects.
        """
        if city:
            results = [contact for book in self.address_books.values()
                       for contact in book.contacts
                       if contact.city.lower() == city.lower()]
        else:
            print("Please provide a city to search.")
            return

        if results:
            print("\nSearch Results:")
            for result in results:
                print(result)
        else:
            print("No contacts found in the given city.")

def main():
    """
    Description:
        Main function that provides a menu-driven interface for the address book system.
    """
    system = AddressBookSystem()
    
    while True:
        print("\n1. Add Address Book")
        print("2. Add Contact to Address Book")
        print("3. Display Contacts")
        print("4. Display All Address Books")
        print("5. Search Person by City")
        print("6. Edit Contact")
        print("7. Delete Contact")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            book_name = input("Enter Address Book name: ").strip()
            system.add_address_book(book_name)
        elif choice == "2":
            book_name = input("Enter Address Book name: ").strip()
            address_book = system.get_address_book(book_name)
            if address_book:
                name = input("Enter Contact Name: ").strip()
                phone = input("Enter Phone Number: ").strip()
                email = input("Enter Email: ").strip()
                address = input("Enter Address: ").strip()
                city = input("Enter City: ").strip()
                state = input("Enter State: ").strip()
                address_book.add_contact(name, phone, email, address, city, state)
            else:
                print(f"Address Book '{book_name}' does not exist!")
        elif choice == "3":
            book_name = input("Enter Address Book name: ").strip()
            address_book = system.get_address_book(book_name)
            if address_book:
                address_book.display_contacts()
            else:
                print(f"Address Book '{book_name}' does not exist!")
        elif choice == "4":
            system.display_all_books()
        elif choice == "5":
            city = input("Enter City: ").strip()
            system.search_person_city(city if city else None)
        elif choice == "6":
            book_name = input("Enter Address Book name: ").strip()
            address_book = system.get_address_book(book_name)
            if address_book:
                name = input("Enter the name of the contact to edit: ").strip()
                new_name = input("Enter New Contact Name: ").strip()
                phone = input("Enter New Phone Number: ").strip()
                email = input("Enter New Email: ").strip()
                address = input("Enter New Address: ").strip()
                city = input("Enter New City: ").strip()
                state = input("Enter New State: ").strip()
                updated_contact = Contact(new_name, phone, email, address, city, state)
                address_book.edit_contact(name, updated_contact)
            else:
                print(f"Address Book '{book_name}' does not exist!")
        elif choice == "7":
            book_name = input("Enter Address Book name: ").strip()
            address_book = system.get_address_book(book_name)
            if address_book:
                name = input("Enter the name of the contact to delete: ").strip()
                address_book.delete_contact(name)
            else:
                print(f"Address Book '{book_name}' does not exist!")
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()