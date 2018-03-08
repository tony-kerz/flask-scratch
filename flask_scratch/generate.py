import asyncio
import logging
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from .config import config

log = logging.getLogger(__name__)
fake = Faker()

# pylint: disable=no-member


async def generate():
    url = f"mongodb://{config.db.host}"
    log.info(f"url={url}, name={config.db.name}")
    client = AsyncIOMotorClient(url)
    db = client[config.db.name]
    collect = db.people
    thresh = config.generate.thresh
    for i in range(int(config.generate.total)):
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
        result = await collect.insert_one(doc)
        if i and i % thresh == 0:
            log.info(f"completed insert batch, total={i}")
        # log.info(f"result={result}")

loop = asyncio.get_event_loop()
loop.run_until_complete(generate())
