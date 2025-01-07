from collections import UserDict
import re
import pickle
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Email(Field):
    def __init__(self, value):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must consist of exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")

class Address(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Address cannot be empty.")
        super().__init__(value)
        
        
class Note:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content
class Record:
   # Дописати логіку для збереження адресси

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None
        self.address = None
        self.note = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone number {old_phone} not found.")

    def add_email(self, email):
        self.emails.append(Email(email))

    def remove_email(self, email):
        self.emails = [e for e in self.emails if e.value != email]

    def edit_email(self, old_email, new_email):
        for i, e in enumerate(self.emails):
            if e.value == old_email:
                self.emails[i] = Email(new_email)
                return
        raise ValueError(f"Email {old_email} not found.")
    
    def add_address(self, address):
        self.address = Address(address)

    def add_note(self, note):
        self.note = Note(note)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) if self.phones else "N/A"
        emails = "; ".join(e.value for e in self.emails) if self.emails else "N/A"
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        address = str(self.address) if self.address else "N/A"
        note = str(self.note) if self.note else "N/A"
        return (f"Name: {self.name.value}\n"
                f"Phones: {phones}\n"
                f"Emails: {emails}\n"
                f"Birthday: {birthday}\n"
                f"Address: {address}\n"
                f"Note: {note}")

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    # def upcoming_birthdays(self):
    #     today = datetime.today()
    #     next_week = today + timedelta(days=7)
    #     return [record for record in self.data.values() if record.birthday and today <= record.birthday.value.replace(year=today.year) <= next_week]
    
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


