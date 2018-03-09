import logging
from ..config import config

log = logging.getLogger(__name__)
maxLimit = config.db.maxLimit


def get_sort(value):
    # return {value[1:]: -1} if value.startswith('-')) else {value: 1}
    return (value[1:], -1) if value.startswith('-') else (value, 1)


def get_data(args, db, collection):
    query = {
        k: v
        for k, v in args.items()
        if k not in ['limit', 'skip', 'sort', 'includeCount']
    }

    limit = int(args.get('limit') or maxLimit)
    skip = int(args.get('skip') or 0)

    # https://stackoverflow.com/q/49123344/2371903
    # pipe = [{'$match': query}]

    sort = args.get('sort') or '_id'
    # if (sort):
    #    pipe.append({'$sort': get_sort(sort)})

    # pipe += [{'$skip': skip}, {'$limit': limit}]

    # log.info(f"pipe=\n{json.dumps(pipe, indent=2)}")
    # data = list(db[collection].aggregate(pipe, explain=True))
    data = list(db[collection].find(query).sort(*get_sort(sort)).skip(skip).limit(limit))
    count = None
    if args.get('includeCount') == 'true':
        count = db[collection].find(query).count()
    # would like to call data and count in parallel, but Flask doesn't lend itself to that like Sanic
    # so these calls are sequential which will hurt performance

    log.info(f"data[0]={len(data) and data[0]}, count={count}")
    return data, count
