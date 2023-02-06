import json
import re

CONTACT_FILE_PATH = "contacts.json"
MENU_PRINT = """
The following is a list of useable commands:
    "add": Adds a contact.
    "delete": Deletes a contact.
    "list": Lists all contacts.
    "search": Searches for a contact by name.
    "q": Quits the program and saves the contact list.
        """


def read_contacts(file_path):
    try:
        with open(file_path, 'r') as f:
            contacts = json.load(f)['contacts']
    except FileNotFoundError:
        contacts = []

    return contacts


def write_contacts(file_path, contacts):
    with open(file_path, 'w') as f:
        contacts = {"contacts": contacts}
        json.dump(contacts, f)


def verify_email_address(email):
    if email == "":
        return True

    if "@" not in email:
        return False

    split_email = email.split("@")
    identifier = "".join(split_email[:-1])
    domain = split_email[-1]

    if len(identifier) < 1:
        return False

    if "." not in domain:
        return False

    split_domain = domain.split(".")

    for section in split_domain:
        if len(section) == 0:
            return False

    return True


def verify_phone_number(phone_number):
    print(re.sub(r'\W+', '', phone_number))
    return re.search("\d{10}", re.sub(r'\W+', '', phone_number)) or phone_number in ["", None]


def required(entry):
    return entry not in ["", None]


def is_contact_duplicated(contacts, candidate):
    return any(contact["first_name"] == candidate["first_name"]
               and contact["last_name"] == candidate["last_name"] for contact in contacts)


CONTACT_FIELDS = [
    {"key": "first_name", "display": "First name: ", "rules": [required]},
    {"key": "last_name", "display": "Last name: ", "rules": [required]},
    {"key": "mobile_phone_number", "display": "Mobile phone number: ",
        "rules": [verify_phone_number]},
    {"key": "home_phone_number", "display": "Home phone Number: ",
        "rules": [verify_phone_number]},
    {"key": "email_address", "display": "Email address: ",
        "rules": [verify_email_address]},
    {"key": "address", "display": "Address: ", "rules": []}
]


def add_contact(contacts):
    new_contact = {}
    for field in CONTACT_FIELDS:
        entry = input(field["display"]).strip()
        for rule in field["rules"]:
            if not rule(entry):
                print("You entered invalid information, this contact was not added.")
                return
        new_contact[field["key"]] = entry
    if is_contact_duplicated(contacts, new_contact):
        print("A contact with this name already exists.")
        print("You entered invalid information, this contact was not added.")
        return
    contacts.append(new_contact)


def search_for_contact(contacts):
    entry = {}
    for field in CONTACT_FIELDS:
        if field["key"] in ["last_name", "first_name"]:
            entry[field["key"]] = input(field["display"]).strip().lower()

    res = list(filter(
        lambda x: entry["first_name"] in x["first_name"] and entry["last_name"] in x["last_name"],
        contacts))

    if not res:
        print("No contact found")

    for idx, contact in enumerate(res):
        display_contact(idx, contact)


def delete_contact(contacts):
    entry = {}
    for field in CONTACT_FIELDS:
        if field["key"] in ["last_name", "first_name"]:
            entry[field["key"]] = input(field["display"]).strip()

    res = list(filter(lambda x: (x[key] == entry[key]
                                 for key in ["last_name", "first_name"]), contacts))

    if len(res) <= 0:
        print("No contact with this name exists.")
        return

    display_contact(1, res[0])

    confirm = input(
        "Are you sure you would like to delete this contact (y/n)? ").strip().lower()
    if confirm in ["yes", "y"]:
        contacts.remove(res[0])
        print("Contact deleted!")
    return


def list_contacts(contacts):
    for idx, contact in enumerate(contacts):
        display_contact(idx, contact)


def display_contact(idx, contact):
    print(f"{idx+1}. {contact['first_name']} {contact['last_name']}")
    for field in CONTACT_FIELDS:
        if field["key"] in ["first_name", "last_name"] or contact[field["key"]] == "":
            continue
        print(f"      {field['display']}{contact[field['key']]}")


def main(contacts_path):
    contacts = read_contacts(contacts_path)
    commands = {"add": add_contact, "delete": delete_contact,
                "search": search_for_contact, "list": list_contacts}
    print("*********************************")
    print("* Welcome to your contact list! *")
    print("*********************************")
    while True:
        print(MENU_PRINT)
        command = input("Type a command: ")

        if command in ["q", "quit", "exit"]:
            write_contacts(contacts_path, contacts)
            print("\nContacts were saved successfully.\n")
            break
        elif command not in commands.keys():
            print("Invalid input")
            continue
        else:
            print("\n")
            commands[command](contacts)
            print("\n--")


if __name__ == "__main__":
    main(CONTACT_FILE_PATH)
