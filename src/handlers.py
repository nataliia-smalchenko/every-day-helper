from src.utils import input_error
from src.models import Record

def greet(args, book):
    return "How can I help you?"

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Usage: add <name> <phone> [email] [birthday] [address] [note]")

    name, phone, *other = args
    birthday = None
    address = None
    note = None
    email = None

    if len(other) > 0:
        birthday = other[0]
    if len(other) > 1:
        address = other[1]
    if len(other) > 2:
        note = other[2]
    if len(other) > 3:
        email = other[3]

    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)
    if address:
        record.add_address(address)
    if note:
        record.add_note(note)
    if email:
        record.add_email(email)

    return message


@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Usage: change <name> <field> <new_value>")

    name, field, new_value = args
    record = book.find(name)

    if record:
        if field == "phone":
            record.edit_phone(new_value)
        elif field == "birthday":
            record.add_birthday(new_value)
        elif field == "address":
            record.add_address(new_value)
        elif field == "note":
            record.add_note(new_value)
        elif field == "email":
            record.add_email(new_value)
        else:
            raise ValueError("Invalid field. Valid fields: phone, birthday, address, note, email.")

        return f"{field.capitalize()} updated."

    return "Contact not found."


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
    return str(book)


@input_error
def add_email(args, book):
    if len(args) < 2:
        raise ValueError("Usage: add_email <name> <email>")

    name, email = args
    record = book.find(name)

    if record:
        record.add_email(email)
        return "Email added."

    return "Contact not found."


@input_error
def change_email(args, book):
    if len(args) < 2:
        raise ValueError("Usage: change_email <name> <new_email>")

    name, new_email = args
    record = book.find(name)

    if record:
        record.add_email(new_email)
        return "Email updated."

    return "Contact not found."


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)

    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)

    if record and record.birthday:
        return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"
    return "No birthday found for this contact."


# додати можливість задати кількість днів в ручну
@input_error
def show_upcoming_birthdays(_, book):
    upcoming = book.upcoming_birthdays()

    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}" for record in upcoming)