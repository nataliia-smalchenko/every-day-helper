import pickle
from src.utils import parse_input
from src.models.books import AddressBook, NotesBook
from src.handlers import ( greet, add_birthday, add_contact,
                         show_all_contacts, show_birthday, show_phone,
                         show_upcoming_birthdays, change_contact,
                         add_note, edit_note, delete_note, search_notes,
                         list_notes, add_tag, remove_tag)
from settings import ADRRESS_BOOK_FILENAME, NOTES_BOOK_FILENAME

def main():
    adrress_book = AddressBook.load_data(ADRRESS_BOOK_FILENAME)
    notes_book = NotesBook.load_data(NOTES_BOOK_FILENAME)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        handlers_address = {
            "hello": greet,
            "add_contact": add_contact,
            "change": change_contact,
            "phone": show_phone,
            "all": show_all_contacts,
            "add-birthday": add_birthday,
            "show-birthday": show_birthday,
            "birthdays": show_upcoming_birthdays,
        }

        handlers_notes = {
            "add_note": add_note,
            "edit_note": edit_note,
            "delete_note": delete_note,
            "search_notes": search_notes,
            "list_notes": list_notes,
            "add_tag": add_tag,
            "remove_tag": remove_tag,
        }
        
        if command in ["close", "exit"]:
            print("Good bye!")
            adrress_book.save_data(ADRRESS_BOOK_FILENAME)
            notes_book.save_data(NOTES_BOOK_FILENAME)
            break

        if command in handlers_address:
            print(handlers_address[command](args, adrress_book))
        elif command in handlers_notes:
            print(handlers_notes[command](args, notes_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
