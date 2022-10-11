from .client import LinLogClient
from .model_trainer import ModelTrainer

import os

if not os.path.exists(
  os.path.expanduser("~") + os.sep + ".linear-logic"
):
  os.mkdir(os.path.expanduser("~") + os.sep + ".linear-logic")