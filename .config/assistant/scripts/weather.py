import os
import click
import requests
import tqdm
import time
from colorama import Fore, init

init(autoreset=True)


@click.command()
def weather():
    for _ in tqdm.tqdm(range(100), desc="Initializing Weather Assistant"):
        time.sleep(0.02)

    response = requests.get("https://wttr.in")
    os.system("cls" if os.name == "nt" else "clear")
    print(response.text)
    pass
