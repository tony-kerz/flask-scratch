import logging
from flask_scratch.app import app
from flask_scratch.config import config

log = logging.getLogger(__name__)


def main():
    port = config.listener.port
    log.info(f"listening on port={port}")
    app.run(host='0.0.0.0', port=port, debug=True)


main()
