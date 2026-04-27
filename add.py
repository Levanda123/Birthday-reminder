from main import BirthdayManager
import os

manager = BirthdayManager()
user = os.getlogin()

name = input("Enter name: ")
date = input("Enter date (YYYY-MM-DD): ")

manager.add_birthday(user, name, date)
print(f"Added {name}'s birthday on {date}!")