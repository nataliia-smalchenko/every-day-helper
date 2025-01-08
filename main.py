from src.utils import parse_input
from src.models import AddressBook
from src.handlers import ( greet, add_birthday, add_contact, show_all_contacts, show_birthday, show_phone, show_upcoming_birthdays, change_contact, )
from src.info_commands import print_command_list

FILENAME = "addressbook.pkl"


def main():
    book = AddressBook.load_data(FILENAME)
    print("Welcome to the assistant bot!")
    print(f"Loaded {len(book.data)} contacts.")
    print_command_list()

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        handlers = {
            "hello": greet,
            "add": add_contact,
            "change": change_contact,
            "phone": show_phone,
            "all": show_all_contacts,
            "add-birthday": add_birthday,
            "show-birthday": show_birthday,
            "birthdays": show_upcoming_birthdays,
        }
        
        if command in ["close", "exit"]:
            book.save_data(FILENAME)
            break

        if command in handlers:
            print(handlers[command](args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()