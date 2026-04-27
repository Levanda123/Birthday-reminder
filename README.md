# Birthday Reminder — Coursework Report

---

## 1. Introduction

### What is the application?

Birthday Reminder is a Python command-line application that tracks birthdays and sends Windows desktop notifications. It notifies the user on the day of a birthday and 3 days in advance, so no important date is ever missed. Birthdays are stored persistently in a CSV file and are tied to the logged-in Windows user.

### How to run the program?

1. Make sure Python 3 is installed.
2. Install the required dependency:
   ```
   py -m pip install plyer
   ```
3. Run the main script:
   ```
   py main.py
   ```

### How to use the program?

To add birthdays, use the included helper script:

```
py add.py
```

You will be prompted to enter a name and a date in `YYYY-MM-DD` format. Once added, run `main.py` each day (or set it up as a scheduled task) to receive notifications when a birthday is today or 3 days away.

---

## 2. Body / Analysis

### OOP Pillars

#### Encapsulation

`BirthdayManager` encapsulates all birthday data and logic. The internal `self.data` dictionary and `self.file_handler` are managed only through the class methods `add_birthday()` and `check_reminders()`. External code never directly manipulates the data.

```python
class BirthdayManager:
    def __init__(self, filename="birthdays.csv"):
        self.file_handler = FileHandler(filename=filename)
        self.data = self.file_handler.load_data()
```

#### Abstraction

The abstract base class `Notification` defines a common interface (`send()`) without implementing it. This hides the complexity of how a notification is delivered from the rest of the program.

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message): pass
```

#### Inheritance

`WindowsNotification` inherits from `Notification` and provides the concrete implementation using the `plyer` library.

```python
class WindowsNotification(Notification):
    def send(self, message):
        notification.notify(
            title="Birthday Reminder",
            message=message,
            app_name="Birthday Reminder",
            timeout=10
        )
```

#### Polymorphism

The `check_reminders()` method accepts any object of type `Notification`. This means it works with `WindowsNotification` in production and with a `MockNotifier` during unit tests — without changing the method itself.

```python
def check_reminders(self, username, notifier: Notification):
    ...
    notifier.send(f"🎂 Today is {b['name']}'s birthday!")
```

---

### Design Pattern: Singleton

`FileHandler` uses the Singleton pattern to ensure only one instance manages the CSV file throughout the program. This prevents conflicting file reads/writes.

```python
class FileHandler:
    _instance = None

    def __new__(cls, filename="birthdays.csv"):
        if cls._instance is None:
            cls._instance = super(FileHandler, cls).__new__(cls)
            cls._instance.filename = filename
        return cls._instance
```

The Singleton pattern is the most suitable here because the application always reads from and writes to a single file. Having multiple `FileHandler` instances could cause data inconsistency. Compared to Factory Method or Builder, Singleton directly addresses the requirement of a single, shared resource manager.

---

### Composition and Aggregation

**Composition** is used in `BirthdayManager`, which owns a `FileHandler` instance. The `FileHandler` is created inside `__init__` and does not exist independently of the manager.

```python
self.file_handler = FileHandler(filename=filename)
```

**Aggregation** is demonstrated through the `notifier` parameter in `check_reminders()`. The `BirthdayManager` uses a `Notification` object but does not own or create it — it is passed in from outside, meaning both can exist independently.

```python
def check_reminders(self, username, notifier: Notification):
```

---

### Functional Requirements Coverage

| Requirement | Implementation |
|---|---|
| Store birthdays | `FileHandler.save_data()` writes to `birthdays.csv` |
| Load birthdays | `FileHandler.load_data()` reads CSV on startup |
| Today's reminder | `check_reminders()` compares `next_bday == today` |
| 3-day reminder | `check_reminders()` compares `next_bday == today + 3 days` |
| Windows notification | `WindowsNotification.send()` via `plyer` |
| Multi-user support | Data is keyed by `os.getlogin()` username |

---

### Testing

Unit tests are written using Python's built-in `unittest` framework. The Singleton is reset between tests to ensure isolation. A `MockNotifier` class is used to test notifications without triggering real Windows popups.

Run tests with:
```
py -m unittest test_birthdays.py
```

Tests covered:

- `test_add_birthday` — verifies a birthday is correctly added to `self.data`
- `test_file_persistence` — verifies data survives a reload from CSV
- `test_3day_reminder` — verifies the 3-day early reminder fires correctly using a mock notifier

---

## 3. Results and Summary

### Results

- The application successfully detects and notifies the user of birthdays on the day and 3 days in advance.
- The Singleton pattern ensured consistent file access throughout all test and runtime scenarios.
- Date format flexibility was added to handle both `YYYY-MM-DD` and `M/D/YYYY` formats gracefully.
- All 3 unit tests pass successfully with proper test isolation using Singleton reset and temporary CSV files.

### Conclusions

The Birthday Reminder application meets all defined functional and technical requirements. It demonstrates all four OOP pillars, applies the Singleton design pattern appropriately, and uses both composition and aggregation. The program is easily extendable — for example, it could be extended with a GUI (e.g. using `tkinter`), support for email notifications via a new `Notification` subclass, or integration with a database instead of CSV for larger datasets. Scheduling via Windows Task Scheduler would also make daily reminders fully automatic without manual execution.

---

## 4. Resources

- [Python `abc` module documentation](https://docs.python.org/3/library/abc.html)
- [Python `unittest` framework](https://docs.python.org/3/library/unittest.html)
- [plyer library](https://plyer.readthedocs.io/en/latest/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Singleton Design Pattern](https://refactoring.guru/design-patterns/singleton)
- [OOP Principles](https://realpython.com/python3-object-oriented-programming/)
