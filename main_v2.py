from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from src.utils import parse_input
from src.models.books import AddressBook, NotesBook
from src.handlers import (greet, add_birthday, add_contact, show_all_contacts, 
                          show_birthday, show_phone, show_upcoming_birthdays, 
                          change_contact, add_note, edit_note, delete_note, 
                          search_notes, list_notes, add_tag, remove_tag)
from settings import ADRRESS_BOOK_FILENAME, NOTES_BOOK_FILENAME

# Завантаження даних
adrress_book = AddressBook.load_data(ADRRESS_BOOK_FILENAME)
notes_book = NotesBook.load_data(NOTES_BOOK_FILENAME)

# Словник для збереження стану
user_states = {}

helper_messages = {
    "add_contact": "add_contact <name> <phone> [email] [birthday] '[address]'",
    "change_contact": "change <name> <field> <new_value>",
    "phone": "show_phone <name>",
    "add_mail": "add_email <name> <email>",
    "change_email": "change_email <name> <new_email",
    "add_birthday": "add_birthday <name> <birthday>",
    "show_birthday": "show_birthday <name>",
    "search_contacts": "search_contacts <query>",
    "delete_contact": "delete_contact <name>",
    "add_note": "'<title>' '<text>' [tags...]",
    "edit_note": "edit_note <note_id> '[new_title]' '[new_text]' '[new_tags...]'",
    "delete_note": "delete_note <note_id>",
    "search_notes": "search_notes <query>",
    "add_tag": "add_tag <note_id> <tag>",
    "remove_tag": "remove_tag <note_id> <tag>"
}

# Словники команд
handlers_contacts = {
    "hello": greet,
    "add_contact": add_contact,
    "change_contact": change_contact,
    "phone": show_phone,
    "all_contacts": show_all_contacts,
    "add_birthday": add_birthday,
    "show_birthday": show_birthday,
    "upcoming_birthdays": show_upcoming_birthdays,
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

# Обробка команд
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text  # Отримуємо текст від користувача
    command, args = parse_input(user_input)

    # Обробка команди
    try:
        if command in ["close", "exit"]:
            response = "Good bye!"
            adrress_book.save_data(ADRRESS_BOOK_FILENAME)
            notes_book.save_data(NOTES_BOOK_FILENAME)
            await update.message.reply_text(response)
            print(response)  # Друкуємо в термінал
            return

        if command in handlers_contacts:
            response = handlers_contacts[command](args, adrress_book)
        elif command in handlers_notes:
            response = handlers_notes[command](args, notes_book)
        else:
            response = "Invalid command."

        keyboard = [
            [InlineKeyboardButton("Main menu", callback_data="main menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Відправка повідомлення та вивід у термінал
        await update.message.reply_text(
            f"{response}\n\n"
            f"Do you want comeback to main menu?\n", 
            reply_markup=reply_markup
        )
        print(response)

    except Exception as e:
        error_message = f"Error: {e}"
        await update.message.reply_text(error_message)
        print(error_message)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Welcome to your assistant bot! Here's what I can do:\n"
        "- Manage contacts\n"
        "- Manage notes\n\n"
        "Use the buttons below to get started!"
    )
    # Створення кнопок
    keyboard = [
        [InlineKeyboardButton("Contacts", callback_data="contacts")],
        [InlineKeyboardButton("Notes", callback_data="notes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Відправка повідомлення з кнопками
    # Перевіряємо, чи це callback-запит, чи звичайне повідомлення
    if update.message:
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_message, reply_markup=reply_markup)
    print(welcome_message)  # Друкуємо в термінал

# Обробка натискання кнопок (Contacts або Notes)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Підтверджуємо натискання кнопки

    if query.data == "contacts":
        # Створюємо кнопки для управління контактами
        keyboard = [
            [InlineKeyboardButton("Add Contact", callback_data="add_contact")],
            [InlineKeyboardButton("Change Contact", callback_data="change_contact")],
            [InlineKeyboardButton("Show All Contacts", callback_data="all_contacts")],
            [InlineKeyboardButton("Show phone of contact", callback_data="phone")],
            [InlineKeyboardButton("Add birthday to contacts", callback_data="add_birthday")],
            [InlineKeyboardButton("Show birthday of contact", callback_data="show_birthday")],
            [InlineKeyboardButton("Show upcoming birthday of contact", callback_data="show_upcoming_birthdays")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Choose an action for contacts:", reply_markup=reply_markup)

    elif query.data == "notes":
        # Створюємо кнопки для управління нотатками
        keyboard = [
            [InlineKeyboardButton("Add Note", callback_data="add_note")],
            [InlineKeyboardButton("Edit Note", callback_data="edit_note")],
            [InlineKeyboardButton("Delete note", callback_data="delete_note")],
            [InlineKeyboardButton("Show All Notes", callback_data="all_notes")],
            [InlineKeyboardButton("Search Notes", callback_data="search_notes")],
            [InlineKeyboardButton("Add tag to Note", callback_data="add_tag")],
            [InlineKeyboardButton("Delete tag from Note", callback_data="remove_tag")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Choose an action for notes:", reply_markup=reply_markup)

    elif query.data in ("back", "main menu"):
        # Повертаємось до головного меню
        await start(update, context)

    else:
        command = query.data
        message = ''
        reply_markup = None
        keyboard = [
            [InlineKeyboardButton("Main menu", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if command in helper_messages:
            message = (
                "Please use the next construction and send me message\n\n"
                f"{helper_messages[command]}\n\n"
                "Types of data:\n"
                "<data> - Required information\n"
                "[data] - Optional information\n"
                "'<data>' or '[data]' - The data must be in brackets 'Example' or \"Example\"\n"  
            )
        
        elif command in ("all_notes", "all_contacts"):
            if command == "all_notes":
                message = list_notes(None, notes_book)
            else:
                message = list_notes(None, adrress_book)

        await query.edit_message_text(text=message, reply_markup=reply_markup)

# Основна функція
def main():
    TOKEN = "5090905514:AAE0GXTemoBhz3tnuDVnWPfgxT-2OUTwOjs"

    # Створення бота
    app = Application.builder().token(TOKEN).build()

    # Додавання хендлерів
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_command))

    # Запуск бота
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

