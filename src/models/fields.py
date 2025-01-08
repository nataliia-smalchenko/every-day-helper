import re
from datetime import datetime

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
            super().__init__(value)
        except ValueError as e:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.") from e

class Address(Field):

    def __init__(self, value):
        if not value:
            raise ValueError("Address cannot be empty.")
        super().__init__(value)
