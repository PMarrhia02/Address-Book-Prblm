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
        Represents a contact in an address book with personal details.

    Parameters:
        first_name - First name of the contact.
        last_name -Last name of the contact.
        phone - Phone number of the contact.
        email - Email address of the contact.
        address - Street address of the contact.
        city - City where the contact resides.
        state - State where the contact resides.
        zip_code - 6-digit postal code of the contact.

    Returns:
        None

    Raises:
        ValueError: If first_name or last_name is empty, phone is invalid, email format is incorrect, or zip_code is not 6 digits.
    """
    def __init__(self, first_name, last_name, phone, email, address, city, state, zip_code):
        if not first_name or not last_name:
            raise ValueError("First name and last name cannot be empty.")
        if not re.match(r"^\d{10,12}$", phone):
            raise ValueError("Phone number must be 10 or 12 digits long.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        if not re.match(r"^\d{6}$", zip_code):
            raise ValueError("ZIP code must be exactly 6 digits.")
        
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        logging.info(f"Contact created: {self.first_name} {self.last_name}")
    
    def __eq__(self, other):
        """
        Description:
            Checks equality between two contacts based on first and last names (case insensitive).
        
        Parameters:
            other (Contact): Another contact to compare.
        
        Returns:
            bool: True if first and last names match (case insensitive), False otherwise.
        """
        if isinstance(other, Contact):
            return (self.first_name.lower() == other.first_name.lower() and 
                    self.last_name.lower() == other.last_name.lower())
        return False

    def __hash__(self):
        """
        Description:
            Defines a unique hash for a contact based on its first and last names.
        
        Returns:
            int: Hash of the contact's first and last names.
        """
        return hash((self.first_name.lower(), self.last_name.lower()))
    
    def __str__(self):
        """
        Description:
            Returns a formatted string representation of the contact.
        
        Returns:
            str: Formatted contact details.
        """
        return f"{self.first_name} {self.last_name} | {self.phone} | {self.email} | {self.address}, {self.city}, {self.state} {self.zip_code}"

class AddressBook:
    """
    Description:
        Represents an address book that stores multiple contacts.

    Parameters:
        book_name (str): Name of the address book.

    Returns:
        None
    """
    def __init__(self, book_name):
        self.book_name = book_name
        self.contacts = set()
        logging.info(f"Address Book '{book_name}' created.")

    def add_contact(self, first_name, last_name, phone, email, address, city, state, zip_code):
        """
        Description:
            Adds a new contact to the address book if it does not already exist.
        
        Parameters:
            first_name - First name of the contact.
            last_name -Last name of the contact.
            phone - Phone number.
            email - Email address.
            address - Street address.
            city - City.
            state - State.
            zip_code - 6-digit postal code.

        Returns:
            None

        Raises:
            ValueError: If contact details are invalid.
        """
        try:
            contact = Contact(first_name, last_name, phone, email, address, city, state, zip_code)
            if contact in self.contacts:
                logging.warning(f"Duplicate contact '{first_name} {last_name}' not added.")
                print(f"Error: Contact '{first_name} {last_name}' already exists in {self.book_name}.")
            else:
                self.contacts.add(contact)
                logging.info(f"Contact '{first_name} {last_name}' added to {self.book_name}.")
        except ValueError as e:
            logging.error(f"Error adding contact: {e}")
            print(f"Error: {e}")

    def display_contacts(self):
        """
        Description:
            Displays all contacts in the address book.
        
        Returns:
            None
        """
        if not self.contacts:
            print(f"{self.book_name} Address Book is empty.")
            logging.info(f"{self.book_name} Address Book is empty.")
            return
        print(f"\nContacts in {self.book_name}:")
        for contact in self.contacts:
            print(contact)
            logging.info(f"Displayed contact: {contact.first_name} {contact.last_name}")

    def edit_contact(self, first_name, last_name, updated_contact):
        """
        Description:
            Edits an existing contact in the address book.
        
        Parameters:
            first_name (str): First name of the contact to be edited.
            last_name (str): Last name of the contact to be edited.
            updated_contact (Contact): Updated contact object.
        
        Returns:
            None
        """
        try:
            for contact in self.contacts:
                if (contact.first_name.lower() == first_name.lower() and 
                    contact.last_name.lower() == last_name.lower()):
                    self.contacts.remove(contact)
                    self.contacts.add(updated_contact)
                    logging.info(f"Contact '{first_name} {last_name}' updated successfully!")
                    print(f"Contact '{first_name} {last_name}' updated successfully!")
                    return
            logging.warning(f"Contact '{first_name} {last_name}' not found in the address book.")
            print(f"Contact '{first_name} {last_name}' not found in the address book.")
        except Exception as e:
            logging.error(f"Error editing contact: {e}")
            print(f"Error editing contact: {e}")

    def delete_contact(self, first_name, last_name):
        """
        Description:
            Deletes a contact from the address book.

        Parameters:
            first_name - First name of the contact to be deleted.
            last_name - Last name of the contact to be deleted.
        
        Returns:
            None
        """
        try:
            for contact in self.contacts:
                if (contact.first_name.lower() == first_name.lower() and 
                    contact.last_name.lower() == last_name.lower()):
                    self.contacts.remove(contact)
                    logging.info(f"Contact '{first_name} {last_name}' deleted successfully!")
                    print(f"Contact '{first_name} {last_name}' has been deleted.")
                    return
            logging.warning(f"Contact '{first_name} {last_name}' not found in the address book.")
            print(f"Contact '{first_name} {last_name}' not found.")
        except Exception as e:
            logging.error(f"Error deleting contact: {e}")
            print(f"Error deleting contact: {e}")

class AddressBookSystem:
    """
    Description:
        Manages multiple address books.

    Returns:
        None
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
        
        Returns:
            None
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
        
        Returns:
            None
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
            Searches for contacts based on city across multiple address books.

        Parameters:
            city (str, optional): City to search.

        Returns:
            None
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

    def search_person_state(self, state=None):
        """
        Description:
            Searches for contacts based on state across multiple address books.

        Parameters:
            state (str, optional): State to search.

        Returns:
            None
        """
        if state:
            results = [contact for book in self.address_books.values()
                       for contact in book.contacts
                       if contact.state.lower() == state.lower()]
        else:
            print("Please provide a State to search.")
            return

        if results:
            print("\nSearch Results:")
            for result in results:
                print(result)
        else:
            print("No contacts found in the given State.")

def main():
    """
    Description:
        Main function that provides a menu-driven interface for the address book system.
    
    Returns:
        None
    """
    system = AddressBookSystem()
    
    while True:
        print("\n1. Add Address Book")
        print("2. Add Contact to Address Book")
        print("3. Display Contacts")
        print("4. Display All Address Books")
        print("5. Search Person by City")
        print("6. Search Person by State")
        print("7. Edit Contact")
        print("8. Delete Contact")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            book_name = input("Enter Address Book name: ").strip()
            system.add_address_book(book_name)
        elif choice == "2":
            book_name = input("Enter Address Book name: ").strip()
            address_book = system.get_address_book(book_name)
            if address_book:
                first_name = input("Enter First Name: ").strip()
                last_name = input("Enter Last Name: ").strip()
                phone = input("Enter Phone Number: ").strip()
                email = input("Enter Email: ").strip()
                address = input("Enter Address: ").strip()
                city = input("Enter City: ").strip()
                state = input("Enter State: ").strip()
                zip_code = input("Enter ZIP Code (6 digits): ").strip()
                address_book.add_contact(first_name, last_name, phone, email, address, city, state, zip_code)
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
            state = input("Enter State: ").strip()
            system.search_person_state(state if state else None)
        elif choice == "7":
            book_name = input("Enter Address Book name: ").strip()
            address_book = system.get_address_book(book_name)
            if address_book:
                first_name = input("Enter the first name of the contact to edit: ").strip()
                last_name = input("Enter the last name of the contact to edit: ").strip()
                new_first_name = input("Enter New First Name: ").strip()
                new_last_name = input("Enter New Last Name: ").strip()
                phone = input("Enter New Phone Number: ").strip()
                email = input("Enter New Email: ").strip()
                address = input("Enter New Address: ").strip()
                city = input("Enter New City: ").strip()
                state = input("Enter New State: ").strip()
                zip_code = input("Enter New ZIP Code (6 digits): ").strip()
                updated_contact = Contact(new_first_name, new_last_name, phone, email, address, city, state, zip_code)
                address_book.edit_contact(first_name, last_name, updated_contact)
            else:
                print(f"Address Book '{book_name}' does not exist!")
        elif choice == "8":
            book_name = input("Enter Address Book name: ").strip()
            address_book = system.get_address_book(book_name)
            if address_book:
                first_name = input("Enter the first name of the contact to delete: ").strip()
                last_name = input("Enter the last name of the contact to delete: ").strip()
                address_book.delete_contact(first_name, last_name)
            else:
                print(f"Address Book '{book_name}' does not exist!")
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()



