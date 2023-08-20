from linlog import LinLogClient


def run():
    client = LinLogClient.local()

    projects = client.get_projects()
    print()
    print(
        "{:<15} {:<20} {:<15} {:<10}"
            .format('ID', 'Name', 'Type', 'Created Date')
    )
    print("-" * 80)

    for project in projects:
        print("{:<15} {:<20} {:<15} {:<10}".format(
            project['id'],
            project['title'][:19],
            project['type'],
            project['created_date'][:10]))

    print()
