from linlog.client import LinLogClient
from linlog.console import console, log_error
from linlog.exceptions import NoAccess, NotFound
from linlog.schemas import Project


def run(project_id: str, client: LinLogClient) -> None:

    try:
        project: Project = Project.get_by_id(client, project_id)
        created_at = project.created_date.strftime('%d %B, %Y at %H:%M:%S')

        head_length = round((60 - len(project.title + "  ")) / 2)
        header = ("=" * head_length) + " " + project.title.upper() + " " + \
            ("=" * head_length)

        console.print()
        console.print(header)
        console.print(f"Project: [bold]{project.title}")
        console.print("Project type:", project.type)
        console.print("=" * len(header))
        console.print()
        console.print(
            f"Created at: [black]{ created_at }[/black]")
        console.print("")

    except NotFound:
        log_error(f"Unable to find project with id {project_id}")
    except NoAccess:
        log_error("You do not have permission to access this project")
