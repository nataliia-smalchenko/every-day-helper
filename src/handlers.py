from tabulate import tabulate
from src.utils import input_error, is_valid_date
from src.models.record import Record
from src.models.note import Note
from settings import DATE_FORMAT
# from settings import ADRRESS_BOOK_FILENAME, NOTES_BOOK_FILENAME


def greet(_, __):
    """Returns a greeting message."""
    return "How can I help you?"

@input_error
def add_contact(args, book):
    """
    Adds a new contact to the address book.

    Usage: add_contact <name> <phone> [email] [birthday] '[address]'
    """
    if len(args) < 2:
        raise ValueError("Usage: add_contact <name> <phone> [email] [birthday] '[address]'")

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
    if birthday and not is_valid_date(birthday):
        raise ValueError("Invalid date format. Use DD.MM.YYYY.")    
    
    record = Record(name)
    book.add_record(record)

    contact_info = f"Name: {name}, Phone: {phone}, Email: {email if email else ' '}, \
        Birthday: {birthday if birthday else ' '}, Address: {address if address else ' '}"
    message = f"Contact added. Details: {contact_info}"

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
    """
    Changes a contact's information.

    Usage: change <name> <field> <new_value>
    """
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
    """
    Displays a contact's phone numbers.

    Usage: show_phone <name>
    """
    name, *_ = args
    record = book.find(name)

    if record:
        phones = ", ".join(phone.value for phone in record.phones)
        return f"{name}: {phones}"
    return "Contact not found."

@input_error
def show_all_contacts(_, book, max_col_width=30):
    """
    Displays all contacts in a tabular format.
    """
    if not book.data:
        return "No contacts found."

    data = []
    for record in book.data.values():
        name = record.name.value
        phones = "; ".join(p.value for p in record.phones) if record.phones else " "
        emails = "; ".join(e.value for e in record.emails) if record.emails else " "
        birthday = str(record.birthday) if record.birthday else " "
        address = str(record.address) if record.address else " "
        data.append([name, phones, emails, birthday, address])

    headers = ["Name", "Phones", "Emails", "Birthday", "Address"]

    table = tabulate(data, headers=headers, tablefmt="rounded_outline", stralign="left", maxcolwidths=[max_col_width] * len(headers))

    return table

@input_error
def add_email(args, book):
    """
    Adds an email to a contact.

    Usage: add_email <name> <email>
    """
    if len(args) < 2:
        raise ValueError("Usage: add_email <name> <email>")

    name, email = args
    record = book.find(name)

    if record:
        record.add_email(email)
        return f"Email '{email}' added."

    return "Contact not found."

@input_error
def add_birthday(args, book):
    """
    Adds a birthday to a contact.

    Usage: add_birthday <name> <birthday>
    """
    name, birthday, *_ = args
    record = book.find(name)

    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    """
    Displays a contact's birthday.

    Usage: show_birthday <name>
    """
    name, *_ = args
    record = book.find(name)

    if record and record.birthday:
        return f"{name}: {record.birthday}"
    return "No birthday found for this contact."

@input_error
def show_upcoming_birthdays(args, book, max_col_width=30):
    """
    Displays contacts with birthdays within a given number of days.

    Usage: show_upcoming_birthdays <days>
    """
    days = int(args[0]) if args else 7   # Default is 7 days

    if days < 0:
        raise ValueError("Days must be a positive integer.")

    upcoming = book.upcoming_birthdays(days)

    if not upcoming:
        return "No upcoming birthdays."

    # Sort upcoming birthdays by date
    upcoming.sort(key=lambda x: x[1])

    data = []
    for record, birthday in upcoming:
        name = record.name.value
        phones = "; ".join(p.value for p in record.phones) if record.phones else "No phone"
        emails = "; ".join(e.value for e in record.emails) if record.emails else "No email"
        birthday_str = birthday.strftime(DATE_FORMAT).ljust(14)
        address = str(record.address) if record.address else "No address"
        data.append([name, phones, emails, birthday_str, address])

    headers = ["Name", "Phones", "Emails", "Birthday", "Address"]

    table = tabulate(data, headers=headers, tablefmt="rounded_outline", stralign="left", maxcolwidths=[max_col_width] * len(headers))
    return table


def search_contacts(args, book, max_col_width=30):
    """
    Searches for contacts by various fields.

    Usage: search_contacts <query>
    """
    if not args:
        raise ValueError("Usage: search_contacts <query>")
    query = args[0].strip("'").strip()
    results = book.search(query)
    if not results:
        return "No contacts found for the query."

    table_data = []
    headers = ["Name", "Phones", "Emails", "Birthday", "Address"]

    for record in results:
        name = record.name.value if record.name else ""
        phones = "; ".join(p.value for p in record.phones) if record.phones else ""
        emails = "; ".join(e.value for e in record.emails) if record.emails else ""
        birthday = str(record.birthday) if record.birthday else ""
        address = str(record.address) if record.address else ""
        table_data.append([name, phones, emails, birthday, address])

    return tabulate(table_data, headers=headers, tablefmt="rounded_outline", maxcolwidths=[max_col_width] * len(headers))


@input_error
def delete_contact(args, book):
    """
    Deletes a contact by name.
    
    Usage: delete_contact <name>
    """
    if len(args) != 1:
        raise ValueError("Usage: delete_contact <name>")
    name = args[0]
    book.delete_record(name)
    # book.save_data(ADRRESS_BOOK_FILENAME)
    return f"Contact with name {name} deleted."

@input_error
def add_note(args, notes_book):
    """
    Adds a new note to the notes book.

    Usage: add_note <title> <text>
    """
    if len(args) < 2:
        raise ValueError("Usage: add_note '<title>' '<text>' [tags...]")

    title = args[0]
    text = args[1]
    tags = args[2:] if len(args) > 2 else []

    note = Note(title.strip("'\""), text.strip("'\""), [tag.strip("'\"") for tag in tags])
    note_id = notes_book.add_note(note)
    # notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Note added with ID {note_id}."

@input_error
def edit_note(args, notes_book):
    """
    Edits an existing note.

    Usage: edit_note <note_id> '[new_title]' '[new_text]' '[new_tags...]'
    """
    if len(args) < 2:
        raise ValueError("Usage: edit_note <note_id> '[new_title]' '[new_text]' '[new_tags...]'")
    note_id = float(args[0])
    new_title = args[1] if len(args) > 1 else None
    new_text = args[2] if len(args) > 2 else None
    new_tags = args[3:] if len(args) > 3 else None

    notes_book.edit_note(note_id, new_title, new_text, new_tags)
    # notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Note with ID {note_id} updated."

@input_error
def delete_note(args, notes_book):
    """
    Deletes a note from the notes book.

    Usage: delete_note <note_id>
    """
    if len(args) != 1:
        raise ValueError("Usage: delete_note <note_id>")
    note_id = float(args[0])
    notes_book.delete_note(note_id)
    # notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Note with ID {note_id} deleted."

@input_error
def search_notes(args, notes_book):
    """
    Looks for the notes behind the keyword.

    Usage: search_notes <query>
    """
    if not args:
        raise ValueError("Usage: search_notes <query>")
    query = " ".join(args)
    results = notes_book.search(query)
    if not results:
        return "No notes found for the query."
    return f"{'n'.join(str(note) for note in results)}"

@input_error
def list_notes(_, notes_book):
    """
    Displays all notes in a tabular format.
    """
    if not notes_book.data:
        return "No notes available."
    return (
        "---------------------------\n"
        f"{str(notes_book)}"
    )

@input_error
def add_tag(args, notes_book):
    """
    Adds the tag to the exist note.

    Usage: add_tag <note_id> <tag>
    """
    if len(args) < 2:
        raise ValueError("Usage: add_tag <note_id> <tag>")
    note_id = float(args[0])
    tag = args[1]
    note = notes_book.data.get(note_id)
    if not note:
        raise ValueError("Note not found.")
    note.add_tag(tag)
    # notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Tag '{tag}' added to note with ID {note_id}."

@input_error
def remove_tag(args, notes_book):
    """
    Delet the tag to the exist note.

    Usage: remove_tag <note_id> <tag>
    """
    if len(args) < 2:
        raise ValueError("Usage: remove_tag <note_id> <tag>")
    note_id = float(args[0])
    tag = args[1]
    note = notes_book.data.get(note_id)
    if tag not in note.tags:
        raise ValueError("Selected note dont have this tag")
    if not note:
        raise ValueError("Note not found.")
    note.remove_tag(tag)
    # notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Tag '{tag}' removed from note with ID {note_id}."
