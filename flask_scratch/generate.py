import logging
from faker import Faker
from flask_scratch import db
# from pymongo import MongoClient
from .config import config
import json

log = logging.getLogger(__name__)
fake = Faker()


# pylint: disable=no-member


def generate():
    # url = f"mongodb://{config.db.host}"
    # log.info(f"url={url}, name={config.db.name}")
    # client = MongoClient(url)
    # db = client[config.db.name]
    collect = db.people
    total = config.generate.total
    thresh = config.generate.thresh
    log.info(f"total={total}, thresh={thresh}")
    for i in range(int(total)):
        doc = {
            'name': {
                'first': fake.first_name(),
                'last': fake.last_name()
            },
            'address': {
                'street': f"{fake.building_number()} {fake.street_name()} {fake.street_suffix()}",
                'line_2': fake.secondary_address(),
                'city': fake.city(),
                'state': fake.state_abbr(),
                'zip': fake.postalcode()
            },
            'phone': fake.phone_number(),
            'ssn': fake.ssn()
        }
        collect.insert_one(doc)
        if i % thresh == 0:
            i and log.info(f"completed insert batch, total={i}")

generate()
