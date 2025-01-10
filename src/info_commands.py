from tabulate import tabulate

def print_command_list(show_all=False):
    commands = [
        {"command": "hello", "description": "Greet the user"},
        {"command": "add_contact", "description": "Add a contact"},
        {"command": "add_note", "description": "Add a note"},
        {"command": "close/exit", "description": "Exit the application"},
        {"command": "show_all_commands", "description": "Show all commands"},
        {"command": "change_contact", "description": "Modify a contact"},
        {"command": "phone", "description": "Show the contact's phone number"},
        {"command": "all_contacts", "description": "Show all contacts"},
        {"command": "add_birthday", "description": "Add a birthday to a contact"},
        {"command": "show_birthday", "description": "Show a contact's birthday"},
        {"command": "upcoming_birthdays", "description": "Show upcoming birthdays"},
        {"command": "search_contacts", "description": "Search for a contact"},
        {"command": "delete_contact", "description": "Delete a contact"},
        {"command": "edit_note", "description": "Edit a note"},
        {"command": "delete_note", "description": "Delete a note"},
        {"command": "search_notes", "description": "Search for a note"},
        {"command": "all_notes", "description": "Show all notes"},
        {"command": "add_tag", "description": "Add a tag to a note"},
        {"command": "remove_tag", "description": "Remove a note's tag"},
    ]

    headers = ["Command", "Description"]
    
    if not show_all:
        commands = commands[:5]  

    table_data = [[cmd['command'], cmd['description']] for cmd in commands]

    print("List of available commands:")
    print(tabulate(table_data, headers=headers, tablefmt="rounded_outline"))
