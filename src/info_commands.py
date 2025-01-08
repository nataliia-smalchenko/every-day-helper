def print_command_list():
    commands = [
        {"command": "hello", "description": "Привітати користувача"},
        {"command": "add", "description": "Додати контакт"},
        {"command": "change", "description": "Змінити контакт"},
        {"command": "phone", "description": "Показати телефон контакту"},
        {"command": "all", "description": "Показати всі контакти"},
        {"command": "add-birthday", "description": "Додати день народження до контакту"},
        {"command": "show-birthday", "description": "Показати день народження контакту"},
        {"command": "birthdays", "description": "Показати найближчі дні народження"},
        {"command": "close/exit", "description": "Вийти з програми"},
    ]

    table_width = 55

    print("Список доступних команд:")
    print("=" * table_width)
    print(f"| {'Команда'.ljust(15)} | {'Опис'.ljust(35)}|")
    print("=" * table_width)

    for cmd in commands:
        print(f"| {cmd['command'].ljust(15)} | {cmd['description'].ljust(35)}|")

    print("=" * table_width)
