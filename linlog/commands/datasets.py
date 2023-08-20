from colored import attr
from linlog import LinLogClient


def run(client: LinLogClient, output_json=False):
    datasets = client.get_datasets()

    print()
    print(
        attr("bold") +
        "{:<15} {:<20} {:<15} {:<10}"
            .format('ID', 'Name', 'Type', 'Created Date') +
        attr("reset")
    )
    print("-" * 80)

    for dataset in datasets:
        print("{:<15} {:<20} {:<15} {:<10}".format(
            dataset['id'],
            dataset['name'][:19],
            dataset['type'],
            dataset['created_date'][:10]))

    print()
