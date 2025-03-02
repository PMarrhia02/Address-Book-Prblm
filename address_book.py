import re
import os
import logging

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



class ContactError(Exception):
    """Custom exception for contact-related errors."""
    pass


class ContactPerson:
    """Represents a contact with personal details."""

    def __init__(self, first_name: str, last_name: str, address: str, city: str, state: str,
                 zip_code: int, phone: int, email: str) -> None:
        """Initialize a ContactPerson with validated details.

        Args:
            first_name: Contact's first name.
            last_name: Contact's last name.
            address: Street address.
            city: City of residence.
            state: State of residence.
            zip_code: 6-digit ZIP code.
            phone: 10 or 12-digit phone number.
            email: Email address.

        Raises:
            ContactError: If validation fails for any field.
        """
        try:
            if not first_name.strip() or not last_name.strip():
                raise ContactError("First and last name cannot be empty.")

            if not isinstance(zip_code, int) or len(str(zip_code)) != 6:
                raise ContactError("ZIP code must be a 6-digit number.")

            if not isinstance(phone, int) or len(str(phone)) not in (10, 12):
                raise ContactError("Phone number must be 10 or 12 digits.")

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
                raise ContactError("Invalid email format.")

            self.first_name = first_name.strip()
            self.last_name = last_name.strip()
            self.address = address.strip()
            self.city = city.strip()
            self.state = state.strip()
            self.zip_code = zip_code
            self.phone = phone
            self.email = email.strip()

            logging.info(f"Contact created: {self.first_name} {self.last_name}")
        except ContactError as e:
            logging.error(f"Failed to create contact: {e}")
            raise

    def __str__(self) -> str:
        """Return a formatted string of contact details.

        Returns:
            str: Contact information in a readable format.
        """
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Address: {self.address}, {self.city}, {self.state}, {self.zip_code}\n"
                f"Phone: {self.phone}\n"
                f"Email: {self.email}\n")


class AddressBook:
    """Manages a collection of contact entries."""

    def __init__(self) -> None:
        """Initialize an empty address book."""
        self.contacts = {}

    def add_contact(self, contact: ContactPerson) -> None:
        """Add a contact to the address book.

        Args:
            contact: ContactPerson instance to add.

        Raises:
            ContactError: If contact is not a ContactPerson instance or already exists.
        """
        try:
            if not isinstance(contact, ContactPerson):
                raise ContactError("Contact must be a ContactPerson instance.")

            full_name = f"{contact.first_name} {contact.last_name}"
            if full_name in self.contacts:
                logging.warning(f"Duplicate contact attempted: {full_name}")
                raise ContactError(f"Contact '{full_name}' already exists.")
            
            self.contacts[full_name] = contact
            logging.info(f"Contact '{full_name}' added successfully")
            print(f"\nContact '{full_name}' added successfully!\n")
        except ContactError as e:
            logging.error(f"Error adding contact: {e}")
            print(f"Error: {e}")

    def display_contacts(self) -> None:
        """Display all contacts in the address book."""
        try:
            if not self.contacts:
                logging.info("Address book is empty")
                print("\nAddress Book is empty!\n")
            else:
                logging.info("Displaying all contacts")
                print("\nYour Address Book:")
                for contact in self.contacts.values():
                    print(contact)
        except Exception as e:
            logging.error(f"Error displaying contacts: {e}")
            print(f"Error: {e}")


class AddressBookMain:
    """Main interface for user interaction with the address book."""

    @staticmethod
    def _get_validated_input(prompt: str, validation_func, error_message: str) -> str:
        """Get user input with validation.

        Args:
            prompt: Message to display to the user.
            validation_func: Function to validate the input.
            error_message: Message to show if validation fails.

        Returns:
            str: Validated user input.

        Raises:
            ContactError: If input validation fails repeatedly.
        """
        while True:
            try:
                user_input = input(prompt).strip()
                if validation_func(user_input):
                    return user_input
                raise ContactError(error_message)
            except ContactError as e:
                logging.error(f"Validation error: {e}")
                print(error_message)

    @staticmethod
    def create_contact() -> ContactPerson:
        """Create a new contact from user input.

        Returns:
            ContactPerson: Newly created contact object, or None if creation fails.
        """
        try:
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            address = input("Enter Address: ").strip()
            city = input("Enter City: ").strip()
            state = input("Enter State: ").strip()

            zip_code = AddressBookMain._get_validated_input(
                "Enter ZIP Code (6 digits): ",
                lambda z: z.isdigit() and len(z) == 6,
                "Invalid ZIP Code! It must be a 6-digit number."
            )

            phone = AddressBookMain._get_validated_input(
                "Enter Phone Number (10 or 12 digits): ",
                lambda p: p.isdigit() and len(p) in (10, 12),
                "Invalid Phone Number! It must be 10 or 12 digits."
            )

            email = AddressBookMain._get_validated_input(
                "Enter Email: ",
                lambda e: re.match(r"[^@]+@[^@]+\.[^@]+", e),
                "Invalid Email! Please enter a valid email address."
            )

            return ContactPerson(first_name, last_name, address, city, state, int(zip_code), int(phone), email)
        except ContactError as e:
            logging.error(f"Error creating contact: {e}")
            print(f"Error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error creating contact: {e}")
            print(f"Unexpected error: {e}")
            return None


def main() -> None:
    """Run the Address Book application."""
    try:
        print("\nWelcome to the Address Book System!\n")
        address_book = AddressBook()

        while True:
            print("\nMenu:")
            print("1. Add Contact")
            print("2. Display Contacts")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                contact = AddressBookMain.create_contact()
                if contact:
                    address_book.add_contact(contact)
            elif choice == "2":
                address_book.display_contacts()
            elif choice == "3":
                logging.info("Exiting Address Book Application")
                print("\nExiting Address Book. Goodbye!\n")
                break
            else:
                logging.warning(f"Invalid menu choice: {choice}")
                print("Invalid choice! Please select a valid option.")
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
        print("\nProgram terminated by user.")
    except Exception as e:
        logging.error(f"Unexpected error in main: {e}")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()