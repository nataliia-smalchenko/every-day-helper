from src.utils import input_error
from src.models import Record


def greet(args, book):
    return "How can I help you?"


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Usage: add <name> <phone> [email] [birthday] [address]")

    name, phone, *other = args
    
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Phone number must consist of exactly 10 digits.")
    
    email = None
    birthday = None
    address = None
    
    if book.find(name):
        return f"Contact with name '{name}' already exists."

    if len(other) > 0 and '@' in other[0]:
        email = other[0]
    if len(other) > 1 and '@' not in other[1]:
        birthday = other[1]
    if len(other) > 2 and '@' not in other[2]:
        address = other[2]

    record = Record(name)
    book.add_record(record)
 
    message = f"Contact '{name}' add."

    if phone:
        record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)
    if address:
        record.add_address(address)
    if email:
        record.add_email(email)

    return message


@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Usage: change <name> <field> <new_value>")

    name, field, new_value = args
    record = book.find(name)

    if not record:
        return f"Contact '{name}' not found."

    if field == "phone":
        record.edit_phone(new_value)
    elif field == "birthday":
        record.add_birthday(new_value)
    elif field == "address":
        record.add_address(new_value)
    elif field == "email":
        record.add_email(new_value)
    else:
        raise ValueError("Invalid field. Valid fields: phone, birthday, address, email.")

    return f"{field.capitalize()} updated."


@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)

    if record:
        phones = ", ".join(phone.value for phone in record.phones)
        return f"{name}: {phones}"
    return "Contact not found."


@input_error
def show_all_contacts(_, book):
    if not book.data:
        return "No contacts found."

    table_width = 120

    table = "=" * table_width + "\n"
    table += f"| {'Name'.ljust(20)} | {'Phones'.ljust(20)} | {'Emails'.ljust(25)} | {'Birthday'.ljust(15)} | {'Address'.ljust(24)} |\n"
    table += "=" * table_width + "\n"

    for record in book.data.values():
        name = record.name.value.ljust(20)
        phones = "; ".join(p.value for p in record.phones).ljust(20) if record.phones else " ".ljust(20)
        emails = "; ".join(e.value for e in record.emails).ljust(25) if record.emails else " ".ljust(25)
        birthday = record.birthday.value.strftime("%d.%m.%Y").ljust(15) if record.birthday else " ".ljust(15)
        address = str(record.address).ljust(24) if record.address else " ".ljust(24)

        table += f"| {name} | {phones} | {emails} | {birthday} | {address} |\n"

    table += "=" * table_width
    return table


@input_error
def add_email(args, book):
    if len(args) < 2:
        raise ValueError("Usage: add_email <name> <email>")

    name, email = args
    record = book.find(name)

    if record:
        record.add_email(email)
        return f"Email '{email}' added."

    return "Contact not found."


@input_error
def change_email(args, book):
    if len(args) < 2:
        raise ValueError("Usage: change_email <name> <new_email>")

    name, new_email = args
    record = book.find(name)

    if record:
        record.add_email(new_email)
        return f"Email '{new_email}' updated."

    return "Contact not found."


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)

    if record:
        record.add_birthday(birthday)
        return f"Birthday added for '{name}'."
    return f"Contact '{name}' not found."


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)

    if record and record.birthday:
        return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"
    return "No birthday found for this contact."


@input_error
def show_upcoming_birthdays(_, book):
    upcoming = book.upcoming_birthdays()

    if not upcoming:
        return "No birthdays in the next 7 days."

    table_width = 40
    table = "=" * table_width + "\n"
    table += f"| {'Name'.ljust(20)} | {'Birthday'.ljust(14)} |\n"
    table += "=" * table_width + "\n"

    for record in upcoming:
        name = record.name.value.ljust(20)
        birthday = record.birthday.value.strftime("%d.%m.%Y").ljust(14)
        table += f"| {name} | {birthday} |\n"

    table += "=" * table_width
    return table

