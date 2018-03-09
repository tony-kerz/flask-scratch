import logging
from flask import Flask, jsonify, request

from .blueprints.people import bp as people_bp

log = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def index():
    log.info(f"request={request}")
    return jsonify({'hello': 'python'})

app.register_blueprint(people_bp, url_prefix='/people')
