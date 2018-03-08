import logging
from sanic_scratch.app import app
from sanic_scratch.config import config

log = logging.getLogger(__name__)


def main():
    port = config.listener.port
    log.info(f"listening on port={port}")
    app.run(host='0.0.0.0', port=port, debug=True)


main()
