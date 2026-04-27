import unittest
import os
import datetime
from main import BirthdayManager, FileHandler
from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message): pass


class TestBirthdayManager(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_birthdays.csv"
        FileHandler._instance = None
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        self.manager = BirthdayManager(filename=self.test_filename)
        self.test_user = "Vartotojas"

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_birthday(self):
        self.manager.add_birthday(self.test_user, "John Doe", "1990-04-28")
        self.assertEqual(self.manager.data[self.test_user][0]['name'], "John Doe")

    def test_file_persistence(self):
        self.manager.add_birthday(self.test_user, "Jane Smith", "1995-04-28")
        FileHandler._instance = None
        new_manager = BirthdayManager(filename=self.test_filename)
        self.assertEqual(new_manager.data[self.test_user][0]['name'], "Jane Smith")

    def test_3day_reminder(self):
        in_3_days = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        self.manager.add_birthday(self.test_user, "Early Bird", in_3_days)

        reminders = []

        class MockNotifier(Notification):
            def send(self, message):
                reminders.append(message)

        self.manager.check_reminders(self.test_user, MockNotifier())
        self.assertTrue(any("3 days" in r for r in reminders))


if __name__ == "__main__":
    unittest.main()