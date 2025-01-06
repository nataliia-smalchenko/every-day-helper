import pickle
from utils import parse_input
from models import AddressBook
from handlers import greet, add_birthday, add_contact, show_all_contacts, show_birthday, show_phone, show_upcoming_birthdays, change_contact


# тут майже все переписати треба
FILENAME = "addressbook.pkl"

# Перннести як класс у моделс
def save_data(book, filename=FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename=FILENAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")

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
            print("Good bye!")
            save_data(book)
            break

        if command in handlers:
            print(handlers[command](args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()