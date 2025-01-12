from prompt_toolkit import PromptSession, print_formatted_text, HTML
from src.utils import parse_input
from src.models.books import AddressBook, NotesBook
from src.handlers import ( greet, add_birthday, add_contact,
                         show_all_contacts, show_birthday, show_phone,
                         show_upcoming_birthdays, change_contact,
                         search_contacts, delete_contact,
                         add_note, edit_note, delete_note, search_notes,
                         list_notes, add_tag, remove_tag)
from src.info_commands import print_command_list
from src.animations import running_text_animation
from src.completer import CustomCompleter, CustomLexer, STYLE, HINTS
from settings import ADRRESS_BOOK_FILENAME, NOTES_BOOK_FILENAME

def main():
    """
    Main function to run the application.

    - Loads data for the address book and notes book.
    - Initializes the command-line interface with a custom prompt.
    - Provides command handlers for managing contacts and notes.
    - Supports commands like adding, editing, deleting, and searching data.
    - Handles exit commands and saves data before exiting.
    """
    adrress_book = AddressBook.load_data(ADRRESS_BOOK_FILENAME)
    notes_book = NotesBook.load_data(NOTES_BOOK_FILENAME)

    session = PromptSession(lexer=CustomLexer(HINTS), completer=CustomCompleter(HINTS), style=STYLE)
    running_text_animation()
    print(f"Loaded {len(adrress_book.data)} contacts.")
    print(f"Loaded {len(notes_book.data)} notes.")
    print_command_list(show_all=False)

    while True:
        try:
            user_input = session.prompt([("class:prompt", ">>> ")])
            command, args = parse_input(user_input)

            handlers_contacts = {
                "hello": greet,
                "add_contact": add_contact,
                "change_contact": change_contact,
                "phone": show_phone,
                "all_contacts": show_all_contacts,
                "add_birthday": add_birthday,
                "show_birthday": show_birthday,
                "upcoming_birthdays": show_upcoming_birthdays,
                "search_contacts" : search_contacts, 
                "delete_contact" : delete_contact, 
            }

            handlers_notes = {
                "add_note": add_note,
                "edit_note": edit_note,
                "delete_note": delete_note,
                "search_notes": search_notes,
                "all_notes": list_notes,
                "add_tag": add_tag,
                "remove_tag": remove_tag,
            }

            if command in ["close", "exit"]:
                print("Good bye!")
                adrress_book.save_data(ADRRESS_BOOK_FILENAME)
                notes_book.save_data(NOTES_BOOK_FILENAME)
                break
            elif command == "show_all_commands":
                print_command_list(show_all=True)
            elif command in handlers_contacts:
                print_formatted_text(HTML(handlers_contacts[command](args, adrress_book)))
            elif command in handlers_notes:
                print_formatted_text(HTML(handlers_notes[command](args, notes_book)))
            else:
                print_formatted_text(HTML("<ansired>Invalid command.</ansired>"))

        except KeyboardInterrupt:
            adrress_book.save_data(ADRRESS_BOOK_FILENAME)
            notes_book.save_data(NOTES_BOOK_FILENAME)
            break
        except EOFError:
            adrress_book.save_data(ADRRESS_BOOK_FILENAME)
            notes_book.save_data(NOTES_BOOK_FILENAME)
            break

if __name__ == "__main__":
    main()
