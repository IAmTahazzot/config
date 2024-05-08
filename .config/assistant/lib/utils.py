import re
from datetime import datetime
from rich.panel import Panel
from rich.text import Text
from rich.box import SQUARE
from colorama import Fore, init

init(autoreset=True)


def validate_project_name(value):
    if not re.match("^[A-Za-z0-9_]*$", value):
        print(Fore.RED + f"Invalid project name: {value}!\n")
        print(
            Fore.LIGHTBLACK_EX
            + "Project name must only contain letters, numbers, and underscores."
        )
        exit(1)

    return value


def display_title(title):
    print("\n")
    TextInstance = Text(title, style="bold black", justify="center")
    return Panel(TextInstance, box=SQUARE)


def display_project(id, name, type, priority, status, due_date):
    print("\n")
    TextInstance = Text(
        f"Project ID: {id}\nName: {name}\nType: {type}\nPriority: {priority}\nStatus: {status}\nDue Date: {due_date}",
        style="bold black",
    )
    return Panel(TextInstance, box=SQUARE)


def days_passed(due_date):
    # Calculate the difference between the due date and the current date
    delta = due_date - datetime.now()

    # Get the total number of days
    total_days = delta.days

    if total_days < 0:
        return 0

    # Determine the time frame
    if total_days >= 365:
        years = total_days // 365
        return f"{years} year{'s' if years > 1 else ''}"
    elif total_days >= 30:
        months = total_days // 30
        days = total_days % 30
        return f"{months} month{'s' if months > 1 else ''} {days} day{'s' if days > 1 else ''}"
    elif total_days >= 7:
        weeks = total_days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''}"
    else:
        return f"{total_days} day{'s' if total_days > 1 else ''}"