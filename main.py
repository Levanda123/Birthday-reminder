import csv
import os
import datetime
from abc import ABC, abstractmethod
from plyer import notification

# --- DESIGN PATTERN: Singleton ---
# Ensures a single, consistent connection to the data file.
class FileHandler:
    _instance = None

    def __new__(cls, filename="birthdays.csv"):
        if cls._instance is None:
            cls._instance = super(FileHandler, cls).__new__(cls)
            cls._instance.filename = filename
        return cls._instance

    def save_data(self, data):
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'name', 'date'])
            for user, birthdays in data.items():
                for b in birthdays:
                    writer.writerow([user, b['name'], b['date']])

    def load_data(self):
        data = {}
        if not os.path.exists(self.filename):
            return data
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = row['username']
                if user not in data:
                    data[user] = []
                data[user].append({'name': row['name'], 'date': row['date']})
        return data


# --- ABSTRACTION: Base class defining the interface ---
class Notification(ABC):
    @abstractmethod
    def send(self, message): pass


# --- INHERITANCE: Concrete implementation for Windows ---
class WindowsNotification(Notification):
    def send(self, message):
        notification.notify(
            title="Birthday Reminder",
            message=message,
            app_name="Birthday Reminder",
            timeout=10
        )


# --- ENCAPSULATION & COMPOSITION ---
class BirthdayManager:
    def __init__(self, filename="birthdays.csv"):
        self.file_handler = FileHandler(filename=filename)
        self.data = self.file_handler.load_data()

    def add_birthday(self, username, name, date=None):
        if date is None:
            date = datetime.date.today().strftime("%Y-%m-%d")
        if username not in self.data:
            self.data[username] = []
        self.data[username].append({'name': name, 'date': date})
        self.file_handler.save_data(self.data)

    def _get_next_birthday(self, date_str):
        """Returns the next occurrence of a birthday as a datetime.date."""
        today = datetime.date.today()
        month, day = int(date_str[5:7]), int(date_str[8:10])
        next_birthday = datetime.date(today.year, month, day)
        if next_birthday < today:
            next_birthday = datetime.date(today.year + 1, month, day)
        return next_birthday

    # POLYMORPHISM: notifier can be any Notification subclass
    def check_reminders(self, username, notifier: Notification):
        today = datetime.date.today()
        in_3_days = today + datetime.timedelta(days=3)

        for b in self.data.get(username, []):
            next_bday = self._get_next_birthday(b['date'])

            if next_bday == today:
                notifier.send(f"🎂 Today is {b['name']}'s birthday!")
            elif next_bday == in_3_days:
                notifier.send(f"⏰ {b['name']}'s birthday is in 3 days!")


if __name__ == "__main__":
    manager = BirthdayManager()
    user = os.getlogin()
    notifier = WindowsNotification()
    manager.check_reminders(user, notifier)