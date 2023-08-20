from importlib import import_module
from linlog.exceptions import ExporterNotFound
from linlog.exporter.exporter import ExportParser


def get_exporter(format: str) -> ExportParser:
    try:
        format = format.replace(".", "_")
        module = import_module(f"linlog.exporter.formats.{format}")
        return getattr(module, "export")
    except ModuleNotFoundError:
        raise ExporterNotFound
