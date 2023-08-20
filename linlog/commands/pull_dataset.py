from linlog import LinLogClient
from linlog.console import log_error
from linlog.dataset.remote_dataset import RemoteDataset
from linlog.exceptions import NotFound, NoAccess


def run(dataset_id: str, client: LinLogClient, format: str = None):
    try:
        rds = RemoteDataset(client, dataset_id)
        rds.export(format, pull=True)
    except NotFound:
        log_error(f"Unable to find dataset with id {dataset_id}")
    except NoAccess:
        log_error("You do not have permission to access this dataset")
