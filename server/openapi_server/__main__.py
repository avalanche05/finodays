#!/usr/bin/env python3

import connexion


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.add_api('openapi.yaml',
                arguments={'title': 'CFA API'},
                pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
