from flask import Blueprint, jsonify, request
import logging
from .helper import get_data
from flask_scratch import db

log = logging.getLogger(__name__)


def mapper(elt):
    elt['_id'] = str(elt['_id'])
    return elt


bp = Blueprint(__name__, __name__)


@bp.route('/')
def index():
    log.info(f"request={request}")
    data, count = get_data(args=request.args, db=db, collection='people')
    data = list(map(mapper, data))
    log.info(f"data={data}")
    res = jsonify(data)
    res.headers = {'x-total-count': count} if count is not None else {}
    return res
