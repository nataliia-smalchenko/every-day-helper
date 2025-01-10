from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

# hints dictionary
HINTS = {
    "hello": {
        "args": 0,
        "hint": None
    },
    "add_contact": {
        "args": 2,
        "optional_args": 3,
        "hint": ["<name>", "<phone (XXXXXXXXXX)>", "[email]", "[birthday]", "'[address]'"]
    },
    "change_contact": {
        "args": 3,
        "hint": ["<name>", ["phone", "birthday", "'address'", "email"], "<new_value (last srgument)>"]
    },
    "phone": {
        "args": 1,
        "hint": ["<name>"]
    },
    "all_contacts": {
        "args": 0,
        "hint": None
    },
    "search_contacts": {
        "args": 1,
        "hint": ["<query>"]
    },
    "delete_contact": {
        "args": 1,
        "hint": ["<name>"]
    },
    "add_birthday": {
        "args": 2,
        "hint": ["<name>", "<new birthday DD.MM.YYYY (last srgument)>"]
    },
    "show_birthday": {
        "args": 1,
        "hint": ["<name>"]
    },
    "upcoming_birthdays": {
        "optional_args": 1,
        "hint": ["[max days to birthday]"]
    },
    "add_note": {
        "args": 2,
        "optional_args": 1,
        "hint": ["'<title>'", "'<text>'", "[tags...]"]
    },
    "edit_note": {
        "args": 1,
        "optional_args": 3,
        "hint": ["<note id>", "'[new_title]'",  "'[new_text]'", "'[new_tags...]'"]
    },
    "delete_note": {
        "args": 1,
        "hint": ["<note id>"]
    },
    "search_notes": {
        "args": 1,
        "hint": ["<query>"]
    },
    "all_notes": {
        "args": 0,
        "hint": None
    },
    "add_tag": {
        "args": 2,
        "hint": ["<note_id>", "<tag>"]
    },
    "remove_tag": {
        "args": 2,
        "hint": ["<note_id>", "<tag>"]
    },
}

class CustomCompleter(Completer):

    def get_completions(self, document: Document, _):
        words = document.text.split()

        # Handle the first word (commands)
        if len(words) == 0 or (len(words) == 1 and not document.text.endswith(" ")):
            for command in HINTS:
                if command.startswith(document.text):
                    yield Completion(command, start_position=-len(document.text))
            return

        # Handle subsequent words
        if len(words) < 1:
            return

        command = words[0]
        command_info = HINTS.get(command)

        # Return if the command is unknown
        if not command_info:
            return

        # Check if more arguments can be entered
        current_arg_count = len(words) - 1
        max_args = command_info.get("args", 0) + command_info.get("optional_args", 0)
        if current_arg_count > max_args:
            return

        # Get the current hint
        hints = command_info["hint"]
        if not hints or current_arg_count > len(hints):
            return

        current_hint = (
            hints[current_arg_count]
            if document.text.endswith(" ") and current_arg_count < max_args
            else hints[current_arg_count - 1]
        )

        # Handle hints that are lists
        if isinstance(current_hint, list):
            last_word = words[-1] if not document.text.endswith(" ") else ""
            for option in current_hint:
                if last_word == "" or option.lower().startswith(last_word.lower()):
                    yield Completion(option, start_position=-len(last_word))
            return

        # Handle hints that are strings
        if isinstance(current_hint, str):
            yield Completion(current_hint, display=current_hint, start_position=0)
