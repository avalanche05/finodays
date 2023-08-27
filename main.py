from flask import Flask
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = '[eq'


def main():
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    main()
