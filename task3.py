import json
import os

# File to store contacts
CONTACTS_FILE = 'contacts.json'

# Load contacts from JSON file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save contacts to JSON file
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

# Add a new contact
def add_contact(contacts):
    print("\nAdd New Contact")
    name = input("Name: ").strip()
    phone = input("Phone Number: ").strip()
    email = input("Email: ").strip()
    address = input("Address: ").strip()

    # Check for duplicate contact by name or phone
    for contact in contacts:
        if contact['name'].lower() == name.lower() or contact['phone'] == phone:
            print("A contact with this name or phone number already exists.")
            return

    contacts.append({
        'name': name,
        'phone': phone,
        'email': email,
        'address': address
    })
    save_contacts(contacts)
    print("Contact added successfully.")

# View all contacts
def view_contacts(contacts):
    if not contacts:
        print("\nNo contacts found.")
        return
    print("\nContact List:")
    for idx, contact in enumerate(contacts, 1):
        print(f"{idx}. {contact['name']} - {contact['phone']}")

# Search contacts by name or phone
def search_contacts(contacts):
    query = input("\nEnter name or phone to search: ").strip().lower()
    results = [c for c in contacts if query in c['name'].lower() or query in c['phone']]
    if results:
        print(f"\nSearch Results ({len(results)} found):")
        for c in results:
            print(f"Name: {c['name']}")
            print(f"Phone: {c['phone']}")
            print(f"Email: {c['email']}")
            print(f"Address: {c['address']}")
            print("-" * 20)
    else:
        print("No matching contacts found.")

# Update contact details
def update_contact(contacts):
    view_contacts(contacts)
    try:
        idx = int(input("\nEnter contact number to update: "))
        if 1 <= idx <= len(contacts):
            contact = contacts[idx - 1]
            print(f"\nUpdating Contact: {contact['name']}")
            new_name = input(f"New Name [{contact['name']}]: ").strip()
            new_phone = input(f"New Phone [{contact['phone']}]: ").strip()
            new_email = input(f"New Email [{contact['email']}]: ").strip()
            new_address = input(f"New Address [{contact['address']}]: ").strip()

            # Update only if input is provided
            if new_name:
                contact['name'] = new_name
            if new_phone:
                contact['phone'] = new_phone
            if new_email:
                contact['email'] = new_email
            if new_address:
                contact['address'] = new_address

            save_contacts(contacts)
            print("Contact updated successfully.")
        else:
            print("Invalid contact number.")
    except ValueError:
        print("Invalid input.")

# Delete a contact
def delete_contact(contacts):
    view_contacts(contacts)
    try:
        idx = int(input("\nEnter contact number to delete: "))
        if 1 <= idx <= len(contacts):
            removed = contacts.pop(idx - 1)
            save_contacts(contacts)
            print(f"Deleted contact: {removed['name']}")
        else:
            print("Invalid contact number.")
    except ValueError:
        print("Invalid input.")

# Main menu
def main():
    contacts = load_contacts()

    while True:
        print("\n--- Contact Management ---")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            view_contacts(contacts)
        elif choice == '3':
            search_contacts(contacts)
        elif choice == '4':
            update_contact(contacts)
        elif choice == '5':
            delete_contact(contacts)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()