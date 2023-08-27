#!/usr/bin/env python3

import connexion

from openapi_server import encoder
from data import db_session
from flask_cors import CORS


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'CFA API'},
                pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    db_session.global_init("../db/db.db")
    main()
