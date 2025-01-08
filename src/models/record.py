from datetime import datetime
from src.models.fields import Name, Phone, Email, Address, Birthday

class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None
        self.address = None

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

    def edit_address(self, old_address, new_address):
        if self.address == old_address:
            self.address = Phone(new_address)
            return
        raise ValueError("User does'nt have this address.")

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
        birthday = self.birthday if self.birthday else "N/A"
        address = str(self.address) if self.address else "N/A"
        return (f"Name: {self.name.value}\n"
                f"Phones: {phones}\n"
                f"Emails: {emails}\n"
                f"Birthday: {birthday}\n"
                f"Address: {address}\n")
