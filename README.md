# Every Day Helper

## Overview

**Every Day Helper** is a powerful system for organizing and managing your contacts and notes efficiently. Designed to simplify everyday tasks, it offers comprehensive features to keep your information accessible and organized.

## Telegram Bot link

[Telegram Bot]()

## Key Features

- **Contact Management:**

  - Add new contacts with detailed information, including:
    - Name
    - Address
    - Phone number
    - Email
    - Birthday
  - Search contacts by multiple criteria such as name.
  - Edit and delete existing contacts.
  - Display a list of contacts with upcoming birthdays within a specified time frame.
  - Validate phone numbers and email addresses during contact creation or editing.

- **Notes Management:**

  - Create, search, edit, and delete text notes.
  - Add "tags" to categorize notes.
  - Search and sort notes by tags.

- **Data Persistence:**

  - All data (contacts and notes) are securely stored on the user's hard drive.
  - Persistent data ensures no loss of information even after restarting the application.

- **Intelligent Assistance:**

  - The system predicts user intentions based on input text and suggests the closest matching commands.

- **Telegram Integration:**
  - Manage contacts and notes directly through a user-friendly Telegram bot interface.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nataliia-smalchenko/every-day-helper
   ```

2. Navigate to the project directory:

   ```bash
   cd every-day-helper
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application from the command line:

```bash
every-day-helper
```

### Available Commands

| Command              | Description                     |
| -------------------- | ------------------------------- |
| `hello`              | Greet the user                  |
| `show_all_commands`  | Show all commands               |
| `close/exit`         | Exit the application            |
| `add-contact`        | Add a new contact               |
| `change_contact`     | Modify a contact                |
| `phone`              | Show the contact's phone number |
| `all_contacts`       | Show all contacts               |
| `add_birthday`       | Add a birthday to a contact     |
| `show_birthday`      | Show a contact's birthday       |
| `upcoming_birthdays` | Show upcoming birthdays         |
| `search_contacts`    | Search for a contact            |
| `delete_contact`     | Delete a contact                |
| `add_note`           | Add a note                      |
| `edit_note`          | Edit a note                     |
| `delete_note`        | Delete a note                   |
| `search_notes`       | Search for a note               |
| `all_notes`          | Show all notes                  |
| `add_tag`            | Add a tag to a note             |
| `remove_tag`         | Remove a note's tag             |

## Developers

- [Nataliia Smalchenko](https://github.com/nataliia-smalchenko)
- [Andrii Veremii](https://github.com/AndriiVeremi)
- [Oleksandr Mamrenko](https://github.com/Mamrenko-Alex)
- [Maryna Korbet](https://github.com/Maryna-Korbet)

## Contact

For questions or feedback, please contact: yarokrilka@gmail.com

## License

This project is licensed under the MIT License.
