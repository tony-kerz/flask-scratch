from sanic.response import json
from sanic import Blueprint
import logging
from .helper import get_data

log = logging.getLogger(__name__)


def mapper(elt):
    elt['_id'] = str(elt['_id'])
    return elt


def get_blueprint(app):
    bp = Blueprint(__name__)

    @bp.route('/')
    async def index(request):
        log.info(f"request={request}")
        data, count = await get_data(args=request.raw_args, db=app.db, collection='people')
        # data = await app.db.people.find({'address.zip': '87447'}).skip(0).limit(3).sort('name.last').to_list(3)
        data = map(mapper, data)
        headers = {'x-total-count': count} if count is not None else {}
        return json(data, headers=headers)

    return bp
