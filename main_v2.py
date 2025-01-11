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
    user_input = update.message.text
    user_id = update.effective_user.id

    if user_id in user_states and user_states[user_id].get("command") == "add_contact":
        # Парсимо ім'я та номер телефону
        try:
            # Викликаємо функцію для додавання контакту
            _, args = parse_input(f"add_contact {user_input}")
            response = add_contact(args, adrress_book)
            print(args)

            # Відповідаємо користувачу
            await update.message.reply_text(response)

            # Очищуємо стан
            user_states[user_id] = {}
        except ValueError:
            await update.message.reply_text(
                "Invalid format. Please send the contact details as:\n\n"
                "<name> <phone>\n\n"
                "Example:\nJohn 0123456789"
            )
        return

    # Якщо немає активного стану, інша логіка
    await update.message.reply_text("Invalid state. Please start again from the main menu.")

    # Отримуємо контекст команди
    command = user_states[user_id]["command"]
    target = user_states[user_id]["target"]

    # Парсимо вхідні дані
    _, args = parse_input(user_input)
    try:
        if target == "contacts" and command in handlers_contacts:
            response = handlers_contacts[command](args, adrress_book)
        elif target == "notes" and command in handlers_notes:
            response = handlers_notes[command](args, notes_book)
        else:
            response = "Invalid command."

        await update.message.reply_text(response)
        user_states[user_id] = {}  # Скидаємо стан після виконання

    except Exception as e:
        error_message = f"Error: {e}"
        await update.message.reply_text(error_message)

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
    command = query.data
    user_id = update.effective_user.id

    await query.answer()  # Підтверджуємо натискання кнопки

    if command in ("contacts", "notes"):
        keyboard = []
        if command == "contacts":
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
        elif command == "notes":
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
        await query.edit_message_text(f"Choose an action for {command}:", reply_markup=reply_markup)

    elif command in ("back", "main menu"):
        # Повертаємось до головного меню
        await start(update, context)

    if command in handlers_contacts:
        # Зберігаємо стан для користувача
        user_states[user_id] = {
            "awaiting_input": True,
            "command": command,
            "target": "contacts" if command in handlers_contacts else "notes"
        }
        keyboard = [
            [InlineKeyboardButton("Back", callback_data=user_states[user_id]["target"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Інструкція для користувача
        await query.edit_message_text(
            "Please send me the contact details in the format:\n\n"
            f"{helper_messages[command]}\n\n"
            "Types of data:\n"
            "<data> - Required information\n"
            "[data] - Optional information\n"
            "'<data>' or '[data]' - The data must be in brackets 'Example' or \"Example\"\n\n"
            "Example:  John 0123456789",
            reply_markup=reply_markup
        )

    elif command in handlers_contacts or command in handlers_notes:
        keyboard = [
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = ''
        user_states[user_id] = {
            "awaiting_input": True,
            "command": command,
            "target": "contacts" if command in handlers_contacts else "notes"
        }

        if command in ("all_notes", "all_contacts"):
            if command == "all_notes":
                message = list_notes(None, notes_book)
            else:
                message = list_notes(None, adrress_book)
            await query.edit_message_text(
                message,
                reply_markup=reply_markup
            )

        await query.edit_message_text(
            "Please use the next construction and send me message\n\n"
            f"{helper_messages[command]}\n\n"
            "Types of data:\n"
            "<data> - Required information\n"
            "[data] - Optional information\n"
            "'<data>' or '[data]' - The data must be in brackets 'Example' or \"Example\"\n",
            reply_markup=reply_markup
        )

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

