import context
import logging
import json
import pytest
from pymongo import MongoClient
from flask_scratch.config import config

log = logging.getLogger(__name__)

coll_name = 'scratch'
url = f"mongodb://{config.db.host}"
log.info(f"_db: url={url}, db={config.db.name}")


@pytest.fixture(autouse=True)
def init(db):
    log.info(f"clean: autouse ftw!, db={db}")
    result = db.drop_collection(coll_name)
    log.info(f"clean: result={result}")
    result = db[coll_name].insert_one({
        'name': {
            'first': 'tony',
            'last': 'kerz'
        },
        'address': {
            'street': '333 E 69th ST',
            'line_2': 'Apt. 9E',
            'city': 'New York',
            'state': 'NY',
            'zip': '10021'
        },
        'phone': '212-861-0610',
        'ssn': '123-45-6789'
    })
    log.info(f"insert-one: result={result}")


@pytest.fixture
def db():
    client = MongoClient(url)
    return client[config.db.name]


def test_find(db):
    coll = db[coll_name]
    log.info(coll)
    data = list(coll.find().sort('_id'))
    log.info(f"data[0]={len(data) and data[0]}")
    assert data


def test_pipe(db):
    coll = db[coll_name]
    max_limit = 200
    args = {'name.first': 'tony', 'sort': 'name.last'}

    query = {
        k: v
        for k, v in args.items() if k not in ['limit', 'skip', 'sort']
    }

    limit = int(args.get('limit') or max_limit)
    skip = int(args.get('skip') or 0)

    pipe = [{'$match': query}]

    if args['sort']:
        pipe.append({'$sort': {args['sort']: 1}})

    pipe += [{'$skip': skip}, {'$limit': limit}]

    log.info(f"pipe=\n{json.dumps(pipe, indent=2)}")
    data = list(coll.aggregate(pipe))
    log.info(data)
    assert data
