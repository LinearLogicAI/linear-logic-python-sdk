from importlib import import_module
from linlog.importer.importer import ImportParser, import_tasks # noqa


def get_importer(format: str = 'linearlogic') -> ImportParser:
    module = import_module(f"linlog.importer.formats.{format}")
    return getattr(module, "parse_filepath")
