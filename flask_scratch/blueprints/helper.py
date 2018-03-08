import logging
import asyncio
from ..config import config

log = logging.getLogger(__name__)
maxLimit = config.db.maxLimit


def get_sort(value):
    # return {value[1:]: -1} if value.startswith('-')) else {value: 1}
    return (value[1:], -1) if value.startswith('-') else (value, 1)


async def get_data(args, db, collection):
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
    # data = await db[collection].aggregate(pipe, explain=True).to_list(length=limit)
    data = db[collection].find(query).sort(*get_sort(sort)).skip(skip).limit(limit).to_list(length=limit)
    tasks = [data]
    if args.get('includeCount') == 'true':
        tasks.append(db[collection].find(query).count())
    results = await asyncio.gather(*tasks)
    _data = results[0]
    _count = results[1] if len(results) == 2 else None
    log.info(f"data[0]={len(_data) and _data[0]}, count={_count}")
    return _data, _count
