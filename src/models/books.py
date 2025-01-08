from collections import UserDict
import pickle
from datetime import datetime, timedelta

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def search(self, query):
        results = []
        query_lower = query.lower()
        for record in self.data.values():
            if query_lower in record.name.value.lower():
                results.append(record)
                continue
            if any(query_lower in phone.value for phone in record.phones):
                results.append(record)
                continue
            if any(query_lower in email.value.lower() for email in record.emails):
                results.append(record)
                continue
            if any(query_lower in address.value.lower() for address in record.address):
                results.append(record)
                continue
        return results

    def upcoming_birthdays(self, days=7):
        today = datetime.today()
        end_date = today + timedelta(days=days)
        return [record for record in self.data.values() if record.birthday and today <= record.birthday.value.replace(year=today.year) <= end_date]
   
    def save_data(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
            
    @classmethod
    def load_data(cls, filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
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
                print(str(note))
        return results
    
    def save_data(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)
            
    @classmethod
    def load_data(cls, filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
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
                "---------------------------"
            )
        return "\n".join(result)
