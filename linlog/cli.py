import argparse
from linlog.commands import (
    authenticate, 
    projects, 
    datasets, 
    remote_dataset_save
)


def main():
    parser = argparse.ArgumentParser(description='Enter string')
    parser.add_argument('command', type=str, help='Enter word or words', nargs='+')
    args = parser.parse_args()
    
    if len(args.command) < 1:
        print("linlog <command>")
        return
    
    if args.command[0] == "authenticate":
        authenticate.run()
    elif args.command[0] == "projects":
        projects.run()
    elif args.command[0] == "datasets":
        datasets.run()
    elif args.command[0] == "remote-dataset":
        if len(args.command) > 1:
            if args.command[1] == "save":
                remote_dataset_save.run(args.command[2])
        else:
            datasets.run()
    else:
        print("Command not found!")



