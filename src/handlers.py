from utils import input_error
from models import Record

def greet(args, book):
    return "How can I help you?"

# переписати логіку з урахуванням нових данних (адресса, мейл...)
# додати хендлери для обробки мейла (add, change)
# додати хендлер з параметрами пошуку
# додати обробники для нотаток (add_note, search_notes, edit_note_command, delete_note_command, show_all_notes)


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Usage: add <name> <phone> [email] [birthday]")
    name, phone, *other = args
    birthday = other[0] if other else None
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
    return message

@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Usage: change <name> <old_phone> <new_phone>")
    name, old_phone, new_phone = args
    record = book.find(name)

    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
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

@input_error
def show_all_contacts(_, book):
    if not book.data:
        return "No contacts found."
    return str(book)

# додати можливість задати кількість днів в ручну
@input_error
def show_upcoming_birthdays(_, book):
    upcoming = book.upcoming_birthdays()

    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}" for record in upcoming)