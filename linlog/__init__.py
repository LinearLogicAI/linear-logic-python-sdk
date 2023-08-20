import os
from linlog.client import LinLogClient  # noqa

if not os.path.exists(
    os.path.expanduser("~") + os.sep + ".linear-logic"
):
    os.mkdir(os.path.expanduser("~") + os.sep + ".linear-logic")
