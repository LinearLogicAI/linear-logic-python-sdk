import json
from linlog.client import LinLogClient
from linlog.console import console, log_error
from rich import print, print_json
from linlog.exceptions import NoAccess, NotFound
from linlog.schemas import Dataset


def run(dataset_id: str, client: LinLogClient, output_json=False) -> None:

    try:
        dataset: Dataset = Dataset.get_by_id(client, dataset_id)
        created_date = dataset.created_date.strftime('%d %B, %Y at %H:%M:%S')

        if output_json:
            print_json(json.dumps(dataset.to_dict()))
            return

        head_length = round((60 - len(dataset.name + "  ")) / 2)
        header = ("=" * head_length) + " " + dataset.name.upper() + " " + \
            ("=" * head_length)

        console.print()
        console.print(header)
        console.print(f"Dataset: [bold]{dataset.name}", highlight=False)
        console.print("Dataset type:", dataset.type)
        console.print("=" * len(header))
        console.print()
        console.print(f"Created at: { created_date }", highlight=False)
        console.print(f"Item count: { dataset.item_count }", highlight=False)
        console.print(
            f"Object count: { dataset.object_count }", highlight=False
        )
        console.print(f"Labels: { len(dataset.labels) }", highlight=False)

        for i, row in enumerate(dataset.labels):
            console.print(
                f"  {i}: {row.label} [italic]{row.type}[/italic]",
                highlight=False
            )

        console.print("")
        link = f"https://dashboard.linearlogic.ai/datasets/{dataset_id}"
        print(f"Workspace: [link={link}]{link}[/link].")
        console.print("")

    except NotFound:
        log_error(f"Unable to find dataset with id {dataset_id}")
    except NoAccess:
        log_error("You do not have permission to access this dataset")
