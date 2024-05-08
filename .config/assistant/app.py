import os
import click
from scripts.project import project
from scripts.weather import weather

@click.group()
def assistant():
    pass


assistant.add_command(project)
assistant.add_command(weather)
assistant.add_command(weather, name='w')

if __name__ == "__main__":
    try:
        assistant()
    except Exception:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Assistant is freezing!")
