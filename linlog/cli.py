import sys
from argparse import ArgumentParser, Namespace
from linlog import LinLogClient
from linlog.commands import (
    help,
    authenticate,
    dataset_info,
    datasets,
    pull_dataset,
)
from typing import Tuple


class Options:
    """
    Has functions to parse CLI options given by the user.
    """

    def __init__(self) -> None:
        self.parser: ArgumentParser = ArgumentParser(
            description="Command line tool to interact with " +
                "Linear Logic workspaces."
        )

        subparsers = self.parser.add_subparsers(dest="command")
        subparsers.add_parser("help", help="Show this help message and exit.")

        subparsers.add_parser("authenticate", help="Authenticate the user. ")

        datasets_parser = subparsers.add_parser(
            "datasets",
            help="Download a version of a dataset."
        )

        datasets_parser.add_argument(
            "-json",
            "--json",
            default=False,
            action="store_true",
            help="Output JSON data",
        )

        datasets_info_parser = subparsers.add_parser(
            "dataset-info",
            help="Download a version of a dataset."
        )

        datasets_info_parser.add_argument(
            "id",
            help="ID of the dataset",
        )

        datasets_info_parser.add_argument(
            "-json", "--json",
            default=False,
            action="store_true",
            help="Output JSON data",
        )

        pull_datasets_parser = subparsers.add_parser(
            "pull-dataset",
            help="Pull dataset items to your local machine."
        )

        pull_datasets_parser.add_argument(
            "id",
            help="ID of the dataset",
        )

        pull_datasets_parser.add_argument(
            "-f", "--format",
            default=None,
            help="Specify format {linearlogic,cvat,coco,pascal}",
        )

    def parse_args(self) -> Tuple[Namespace, ArgumentParser]:
        """
        Parses and validates the CLI options.

        Returns
        -------
        Tuple[Namespace, ArgumentParser]
            The tuple with the namespace and parser to use.
        """
        args = self.parser.parse_args()

        if not args.command:
            self.parser.print_help()
            sys.exit()

        return args, self.parser


def load_client():
    client = LinLogClient.local()
    return client


def main() -> None:

    args, parser = Options().parse_args()

    if args.command in ['help', '-h', '--help']:
        help.run(parser)
        return

    if args.command == "authenticate":
        authenticate.run()
    elif args.command == "datasets":
        datasets.run(output_json=args.json, client=load_client())
    elif args.command == "dataset-info":
        dataset_info.run(args.id, output_json=args.json, client=load_client())
    elif args.command == "pull-dataset":
        pull_dataset.run(
            dataset_id=args.id, format=args.format, client=load_client()
        )
    else:
        print("Command not found!")
