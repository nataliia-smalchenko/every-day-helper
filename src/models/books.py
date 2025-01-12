from collections import UserDict
import pickle
from datetime import datetime, timedelta
from settings import DATE_FORMAT

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete_record(self, name):
        if name not in self.data:
            raise ValueError(f"Contact with name {name} does not exists")
        self.data.pop(name)

    def search(self, query):
        """ 
        Case-insensitive search for records containing the given query in any of 
        the following fields: name, phones, emails, birthday, address.
        """
        results = []
        query_lower = query.lower()

        for record in self.data.values():
            if query_lower in record.name.value.lower():
                results.append(record)
                continue

            if all(query_lower in phone.value for phone in record.phones):
                results.append(record)
                continue
            
            not_empty_emails = []
            for email in record.emails:
                if bool(email.value.strip()):
                    not_empty_emails.append(email)

            if not_empty_emails:
                if all(query_lower in email.value.lower() for email in not_empty_emails):
                    results.append(record)
                    continue

            if record.birthday is not None:
                if query_lower in record.birthday.value:
                    results.append(record)
                    continue

            if record.address is not None:
                if query_lower in record.address.value.lower():
                    results.append(record)
                    continue

        return results

    def upcoming_birthdays(self, days=7):
        """
        Display a list of contacts whose birthday is in a given number of days from the current date.
        
        :param days: Number of days to search for upcoming birthdays. Default is 7.
        """
        today = datetime.today().date()
        end_date = today + timedelta(days=days)
        upcoming_birthdays_list = []

        for record in self.data.values():
            if hasattr(record, 'birthday') and record.birthday:
                # Ensure the birthday is a date object
                birthday_str = record.birthday.value
                birthday = datetime.strptime(birthday_str, DATE_FORMAT).date()

                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= end_date:
                    upcoming_birthdays_list.append((record, birthday_this_year))

        return upcoming_birthdays_list
    
    def save_data(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
            
    @classmethod
    def load_data(cls, filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return cls()

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())        

class NotesBook(UserDict):

    def add_note(self, note):
        """Add note indexed."""
        self.data[note.id] = note
        return note.id

    def edit_note(self, note_id, new_title=None, new_text=None, new_tags=None):
        """Edit a note's title, text, and/or tags."""
        if note_id in self.data:
            note = self.data[note_id]
            if new_title is not None:
                note.title = new_title
            if new_text is not None:
                note.text = new_text
            if new_tags is not None:
                note.tags = new_tags
            note.edited_at = datetime.now()
        else:
            raise ValueError("Note not found with the given timestamp.")

    def delete_note(self, timestamp):
        """Delete a note by its timestamp."""
        if timestamp in self.data:
            del self.data[timestamp]
        else:
            raise ValueError("Note not found with the given timestamp.")

    def search(self, query):
        """Search notes by title, text, or tags."""
        results = []
        query_lower = query.lower()
        for note in self.data.values():
            if (query_lower in note.title.lower() or
                query_lower in note.text.lower() or
                any(query_lower in tag.lower() for tag in note.tags)):
                results.append(note)
        return results
    
    def save_data(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
            
    @classmethod
    def load_data(cls, filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return cls()

    def __str__(self):
        """Return a human-readable string representation of all notes."""
        if not self.data:
            return "No notes available."
        
        result = []
        for ts, note in self.data.items():
            created = datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M:%S')
            tags = ", ".join(note.tags) if note.tags else "No tags"
            result.append(
                f"ID: {ts}\n"
                f"created: {created}\n"
                f"Title: {note.title}\n"
                f"Text: {note.text}\n"
                f"Tags: {tags}\n"
                "───────────────────────────"
            )
        return "\n".join(result)
