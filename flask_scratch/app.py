import logging
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import SanicException
from motor.motor_asyncio import AsyncIOMotorClient
from .config import config
from .blueprints.people import get_blueprint as get_people_bp

log = logging.getLogger(__name__)

app = Sanic()


@app.listener('before_server_start')
async def init_db(app, loop):
    url = f"mongodb://{config.db.host}"
    log.info(f"url={url}, name={config.db.name}")
    app.db = AsyncIOMotorClient(url, io_loop=loop)[config.db.name]
    app.config = config


@app.route('/')
async def test(request):
    return json({'hello': 'python'})


app.blueprint(get_people_bp(app), url_prefix='/people')


@app.exception(SanicException)
def doh(request, exception):
    log(f"doh: request={request}, exception={exception}")
    raise exception
