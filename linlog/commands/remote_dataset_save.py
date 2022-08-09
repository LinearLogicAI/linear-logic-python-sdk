import colored
from colored import stylize, fg, attr
from linlog import LinLogClient
from linlog.dataset import RemoteDataset


def run(id: str):
    client = LinLogClient.local()

    print("Starting dataset export." + attr("reset"))
    ds = RemoteDataset(client, id)
    saved_path = ds.export()

    print()
    print(fg("green") + attr("bold") + "Completed dataset export!" + attr("reset"))
    print("Dataset location:", saved_path)