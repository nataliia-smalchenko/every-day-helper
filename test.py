import unittest

from src.models import AddressBook, Record
from src.handlers import ( greet, add_contact, change_contact, show_phone, show_all_contacts, add_birthday, show_birthday, show_upcoming_birthdays, )
from datetime import datetime

class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        self.record = Record("John Doe")
        self.record.add_phone("1234567890")
        self.record.add_birthday("01.01.1990")
        self.book.add_record(self.record)

    def test_greet(self):
        self.assertEqual(greet([], self.book), "How can I help you?")

    def test_add_contact(self):
        response = add_contact(["Jane Doe", "0987654321", "02.02.1992"], self.book)
        self.assertEqual(response, "Contact added.")
        self.assertIn("Jane Doe", self.book)
        self.assertEqual(len(self.book["Jane Doe"].phones), 1)

    def test_add_contact_existing(self):
        response = add_contact(["John Doe", "1112223333"], self.book)
        self.assertEqual(response, "Contact updated.")
        self.assertEqual(len(self.book["John Doe"].phones), 2)

    def test_show_phone(self):
        response = show_phone(["John Doe"], self.book)
        self.assertEqual(response, "John Doe: 1234567890")

    def test_add_birthday(self):
        response = add_birthday(["Jane Doe", "03.03.1993"], self.book)
        self.assertEqual(response, "Contact not found.")

        add_contact(["Jane Doe", "0987654321"], self.book)
        response = add_birthday(["Jane Doe", "03.03.1993"], self.book)
        self.assertEqual(response, "Birthday added.")
        self.assertEqual(self.book["Jane Doe"].birthday.value.strftime("%d.%m.%Y"), "03.03.1993")

    def test_show_birthday(self):
        response = show_birthday(["John Doe"], self.book)
        self.assertEqual(response, "John Doe: 01.01.1990")

        response = show_birthday(["Jane Doe"], self.book)
        self.assertEqual(response, "No birthday found for this contact.")

    def test_show_all_contacts(self):
        response = show_all_contacts([], self.book)
        self.assertIn("John Doe", response)

if __name__ == "__main__":
    unittest.main()
