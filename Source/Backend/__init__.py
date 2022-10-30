from .Config import load, create_logger
from .Server import create
from .Workers import Workers

config = load()
logger = create_logger()
workers = Workers(config, logger)
app = create(config, workers)
