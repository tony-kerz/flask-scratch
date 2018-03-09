import logging
from pymongo import MongoClient
from .config import config

log = logging.getLogger(__name__)

url = f"mongodb://{config.db.host}"
log.info(f"url={url}, name={config.db.name}")
db = MongoClient(url)[config.db.name]
