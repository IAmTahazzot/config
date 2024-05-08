import os
import click
import questionary
import datetime
from prettytable import PrettyTable
from sqlalchemy import asc, case
from rich import print
from colorama import Fore, init
from dotenv import load_dotenv
from db.schema import Session, Project, clt_sequnce, oss_sequnce, exp_sequnce
from lib.utils import display_title, validate_project_name, display_project, days_passed
from lib.constants import PROJECT_TYPES, PROJECT_STATUSES

load_dotenv()

init(autoreset=True)

# Constants
BASE_DIRECTORY = os.getenv("BASE_PATH")


@click.group()
def project():
    pass


def creation_process(
    project_name,
    project_type,
    client_name=None,
    priority="NORMAL",
    status="ACTIVE",
    description=None,
    due_at=None,
):
    """
    Create a new project.

    This command will prompt the user for a project name and type.
    It'll generate a new directory in the base path with the project name.

    Example:

    project dir name: [TYPE][TYPE_ID]_[NAME]
                      CLT1_EMPLOYEE_MANAGEMENT_SYSTEM
    """
    print(f"\nCreating project '{project_name}' of type '{project_type}'.")
    new_project_name = str(project_name).upper()
    project_id = None
    project_type_id = None

    session = Session()

    # Map project PROJECT_TYPES to their respective sequences
    sequences = {"CLT": clt_sequnce, "OSS": oss_sequnce, "EXP": exp_sequnce}

    try:
        project = Project(
            name=new_project_name,
            type=project_type,
            client_name=client_name,
            project_type_id=sequences[project_type].next_value(),
            status=status,
            priority=priority,
            description=description,
            created_at=datetime.datetime.now(),
            due_at=due_at,
        )

        session.add(project)
        session.commit()

        # Get the project id
        project_id = project.id
        project_type_id = project.project_type_id

        # clear the terminal
        os.system("cls" if os.name == "nt" else "clear")
        print(
            display_title(
                f"Project '{project.name}' created successfully with the following details:"
            )
        )
        # Define the table
        table = PrettyTable()

        # Add columns
        table.field_names = ["Attribute", "Value"]

        # Align
        table.align = "l"

        # Add rows
        table.add_row(["ID", project.id])
        table.add_row(["Name", project.name])
        table.add_row(["Type", project.type])
        table.add_row(["Client Name", project.client_name])
        table.add_row(["Priority", project.priority])
        table.add_row(["Status", project.status])
        table.add_row(["Created At", project.created_at.strftime("%b %d, %Y")])
        table.add_row(["Due At", project.due_at.strftime("%b %d, %Y")])

        # Print the table
        print(table)
    except Exception as e:
        print(f"An error occurred while creating the project: {e}")
    finally:
        session.close()

    try:
        BASE_DIRECTORY = os.getenv("BASE_DIRECTORY")
        project_dir_name = (
            f"{project_type}{project_type_id}_{project_id}_{new_project_name}"
        )
        os.makedirs(os.path.join(BASE_DIRECTORY, project_dir_name))
    except Exception as e:
        print(f"Unable to create project directory, operation aborted!\n")
        print(Fore.LIGHTBLACK_EX + f"Error: {e}")
        exit(1)


@project.command()
def create():
    """
    Create a new project.

    This command will prompt the user for a project name and type.
    It'll generate a new directory in the base path with the project name.

    for example:
    """
    os.system("cls" if os.name == "nt" else "clear")
    print(display_title("New project"))
    project_name = click.prompt(Fore.GREEN + "Name")
    project_name = validate_project_name(project_name)

    project_type = questionary.select(
        "Select a project type:",
        choices=PROJECT_TYPES,
    ).ask()

    client_name = None
    if project_type == "Client Project (CLT)":
        client_name = click.prompt(Fore.GREEN + "Define client name")

    due_year = questionary.select(
        "Select due year:",
        choices=[str(year) for year in range(2024, 2027)],
    ).ask()

    months = {
        "January": "1",
        "February": "2",
        "March": "3",
        "April": "4",
        "May": "5",
        "June": "6",
        "July": "7",
        "August": "8",
        "September": "9",
        "October": "10",
        "November": "11",
        "December": "12",
    }
    due_month = questionary.select(
        "Select due month:",
        choices=months,
    ).ask()

    due_day = questionary.select(
        "Select due day:",
        choices=[str(day) for day in range(1, 32)],
    ).ask()

    due_at = datetime.datetime(int(due_year), int(months[due_month]), int(due_day))

    priority = questionary.select(
        "Select priority:",
        choices=["WEAK", "NORMAL", "HIGH", "CODE RED"],
    ).ask()

    status = questionary.select(
        "Select status:",
        choices=PROJECT_STATUSES,
    ).ask()

    description = click.prompt(Fore.LIGHTBLACK_EX + "Description \n")

    try:
        creation_process(
            project_name=project_name,
            project_type=PROJECT_TYPES[project_type],
            client_name=client_name,
            priority=priority,
            status=status,
            description=description,
            due_at=due_at,
        )
    except Exception as e:
        print(f"Freezing the assistant!")


@project.command()
@click.option("--pretty", "-p", is_flag=True, help="Prettier output")
def list(pretty):
    os.system("cls" if os.name == "nt" else "clear")
    print(display_title("Projects list"))

    TYPES = {
        "All Projects": "all",
        "Client Projects": "CLT",
        "Open Source Projects": "OSS",
        "Experimental Projects": "EXP",
    }

    # Select a type of project
    project_type = questionary.select(
        "TYPE: ",
        choices=TYPES,
    ).ask()

    session = Session()

    try:
        projects = []

        status_order = case(
            (Project.status == "REVISION", 0),
            (Project.status == "ACTIVE", 1),
            (Project.status == "FROZEN", 2),
            (Project.status == "COMPLETED", 3),
            (Project.status == "CANCELLED", 4),
            else_=5,
        )

        if TYPES[project_type] == "all":
            projects = (
                session.query(Project).order_by(status_order, asc(Project.due_at)).all()
            )
        else:
            projects = (
                session.query(Project)
                .filter(Project.type == TYPES[project_type])
                .order_by(status_order, asc(Project.due_at))
                .all()
            )

        if len(projects) == 0:
            print("No projects found.")
            return

        print("\n")
        print(
            f"{'ID':<10}"
            f"{'Project Name':<20}"
            f"{'Client Name':<20}"
            f"{'Type':<15}"
            f"{'Priority':<15}"
            f"{'Status':<16}"
            f"{'Created At':<20}"
            f"{'Due At':<20}"
        )

        for project in projects:
            client_name = project.client_name if project.client_name else "N/A"
            days_left = (project.due_at - datetime.datetime.now()).days

            due_at = days_passed(project.due_at)

            if due_at == 0 and project.status == "COMPLETED":
                due_at = "Archived"
            elif due_at == 0:
                due_at = "Overdue"

            status_emojis = {
                "ACTIVE": "🟢",
                "COMPLETED": "✅",
                "REVISION": "🚩",
                "FROZEN": "❄️ ",
                "CANCELLED": "🔴",
            }

            status = status_emojis[project.status] + " " + project.status
            priority = project.priority if project.priority else "UNDEFINED"

            print(
                f"{project.id:<10}"
                f"{project.name[0].upper() + project.name[1:].lower():<20}"
                f"{client_name:<20}"
                f"{project.type:<15}"
                f"{priority:<15}"
                f"{status:<15}"
                f"{project.created_at.strftime('%b %d, %y'):<20}"
                f"{due_at:<20}"
            )

    except Exception as e:
        print(f"Unable to list projects: {e}")


@project.command()
def overview():
    # TODO:
    #  - Show all CODE_RED projects
    #  - Count unfinished projects in a circle
    #  - Display projects order by due date close to far (ex: Jan 1, Jan 20, Feb 10 etc.)
    #  - (use layout by detecting terminal width in px)
    pass


@project.command()
def freeze():
    # assistant project freeze
    pass


@project.command()
@click.option("--project_id", "-pid", help="Project ID to delete")
def update(project_id=None) -> None:
    # select a project to perfom any action (try searching system on project)
    # use selection to get user decision wether to update 'status' or 'priority' or 'due_date' or 'freeze'
    init(autoreset=True)

    session = Session()
    try:
        project = None

        if project_id:
            project = session.query(Project).filter(Project.id == project_id).first()
        else:
            projects = session.query(Project).all()

            project_names = [
                project.type + str(project.project_type_id) + "_" + project.name
                for project in projects
            ]

            project_name = questionary.select(
                "Select a project to update:",
                choices=project_names,
            ).ask()

            extracted_project_name = "_".join(project_name.split("_")[1:])

            project = (
                session.query(Project)
                .filter(Project.name == extracted_project_name)
                .first()
            )

        if not project:
            print(f"Project '{project.name}' not found.")
            return

        os.system("cls" if os.name == "nt" else "clear")
        print(display_title(f"Updating '{project.name}'"))

        days_left = (project.due_at - datetime.datetime.now()).days
        due_at = (
            str(days_left // 30) + " Months " + str(days_left % 30) + " Days left"
            if days_left > 30
            else (
                str(days_left) + " Days left" if days_left > 0 else "You're dead mate!"
            )
        )

        print(
            display_project(
                project.id,
                project.name,
                project.type,
                project.priority,
                project.status,
                due_at,
            )
        )

        action = questionary.select(
            "Select an action to perform:",
            choices=["Update status", "Update priority", "Update due date", "Freeze"],
        ).ask()

        if action == "Update status":
            status = questionary.select(
                "Select status:",
                choices=PROJECT_STATUSES,
            ).ask()
            project.status = status
        elif action == "Update priority":
            priority = questionary.select(
                "Select priority:",
                choices=["WEAK", "NORMAL", "HIGH", "CODE RED"],
            ).ask()
            project.priority = priority
        elif action == "Update due date":
            due_year = questionary.select(
                "Select due year:",
                choices=[str(year) for year in range(2024, 2027)],
            ).ask()

            months = {
                "January": "1",
                "February": "2",
                "March": "3",
                "April": "4",
                "May": "5",
                "June": "6",
                "July": "7",
                "August": "8",
                "September": "9",
                "October": "10",
                "November": "11",
                "December": "12",
            }
            due_month = questionary.select(
                "Select due month:",
                choices=months,
            ).ask()

            due_day = questionary.select(
                "Select due day:",
                choices=[str(day) for day in range(1, 32)],
            ).ask()

            due_at = datetime.datetime(
                int(due_year), int(months[due_month]), int(due_day)
            )
            project.due_at = due_at
        elif action == "Freeze":
            project.status = "FROZEN"

        session.commit()
        print(f"Project '{project.name}' updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating the project: {e}")
    pass
