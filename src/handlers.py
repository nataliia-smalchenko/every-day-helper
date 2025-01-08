from src.utils import input_error
from src.models.record import Record
from src.models.note import Note
from src.models.books import NotesBook, AddressBook
from settings import ADRRESS_BOOK_FILENAME, NOTES_BOOK_FILENAME


def greet(args, book):
    return "How can I help you?"

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Usage: add <name> <phone> [email] [birthday] [address]")

    name, phone, *other = args
    birthday = None
    address = None
    email = None

    if len(other) > 0:
        birthday = other[0]
    if len(other) > 1:
        address = other[1]
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
        elif field == "email":
            record.add_email(new_value)
        else:
            raise ValueError("Invalid field. Valid fields: phone, birthday, address, email.")

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

@input_error
def show_upcoming_birthdays(_, book):
    upcoming = book.upcoming_birthdays()

    if not upcoming:
        return "No birthdays in the next days."
    return "\n".join(f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}" for record in upcoming)

@input_error
def add_note(args, notes_book):
    """Додає нову нотатку."""
    if len(args) < 2:
        raise ValueError("Usage: add_note '<title>' '<text>' [tags...]")

    title = args[0]
    text = args[1]
    tags = args[2:] if len(args) > 2 else []

    note = Note(title.strip("'\""), text.strip("'\""), [tag.strip("'\"") for tag in tags])
    note_id = notes_book.add_note(note)
    notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Note added with ID {note_id}."

@input_error
def edit_note(args, notes_book):
    """Редагує існуючу нотатку."""
    if len(args) < 2:
        raise ValueError("Usage: edit_note <note_id> '[new_title]' '[new_text]' '[new_tags...]'")
    note_id = float(args[0])
    new_title = args[1] if len(args) > 1 else None
    new_text = args[2] if len(args) > 2 else None
    new_tags = args[3:] if len(args) > 3 else None

    notes_book.edit_note(note_id, new_title, new_text, new_tags)
    notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Note with ID {note_id} updated."

@input_error
def delete_note(args, notes_book):
    """Видаляє нотатку за її ID."""
    if len(args) != 1:
        raise ValueError("Usage: delete_note <note_id>")
    note_id = float(args[0])
    notes_book.delete_note(note_id)
    notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Note with ID {note_id} deleted."

@input_error
def search_notes(args, notes_book):
    """Шукає нотатки за ключовим словом."""
    if not args:
        raise ValueError("Usage: search_notes <query>")
    query = " ".join(args)
    results = notes_book.search(query)
    if not results:
        return "No notes found for the query."
    return f"{'n'.join(str(note) for note in results)}"

@input_error
def list_notes(args, notes_book):
    """Список всіх нотаток."""
    if not notes_book.data:
        return "No notes available."
    return str(notes_book)

@input_error
def add_tag(args, notes_book):
    """Додає тег до нотатки."""
    if len(args) < 2:
        raise ValueError("Usage: add_tag <note_id> <tag>")
    note_id = float(args[0])
    tag = args[1]
    note = notes_book.data.get(note_id)
    if not note:
        raise ValueError("Note not found.")
    note.add_tag(tag)
    notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Tag '{tag}' added to note with ID {note_id}."

@input_error
def remove_tag(args, notes_book):
    """Видаляє тег з нотатки."""
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
    notes_book.save_data(NOTES_BOOK_FILENAME)
    return f"Tag '{tag}' removed from note with ID {note_id}."
