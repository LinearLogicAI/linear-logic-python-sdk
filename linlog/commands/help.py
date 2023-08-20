import argparse
from typing import Optional


def run(
    parser: argparse.ArgumentParser,
    subparser: Optional[str] = None
) -> None:
    """
    Prints the help text for the given command.

    Parameters
    ----------
    parser: argparse.ArgumentParser
        The parser used to read input from the user.
    subparser: Optional[str]
        Actions from the parser to be processed. Defaults to None.
    """

    def get_parser(key: str):
        return next(
            action.choices[key]
            for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
            and key in action.choices.keys()
        )

    if subparser:
        parser = get_parser(subparser)

    actions = [
        action for action in parser._actions if
        isinstance(action, argparse._SubParsersAction)
    ]

    print("\nCommands:")
    for action in actions:
        # get all subparsers and print help
        for choice in sorted(action._choices_actions, key=lambda x: x.dest):
            _parser = get_parser(choice.dest)
            store_action_dict = vars(_parser)['_option_string_actions']
            print("    {:<23} {}".format(choice.dest, choice.help))
            for i in range(0, len(store_action_dict.keys()), 2):
                action_key = list(store_action_dict.keys())[i]
                action_key_alt = list(store_action_dict.keys())[i+1]

                if action_key in ['-h', '--help']:
                    continue

                print("        {:<21} {}".format(', '.join([
                    action_key, action_key_alt
                ]), store_action_dict[action_key].help))
    print()
