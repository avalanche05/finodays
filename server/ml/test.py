from data import trade, db_session

db_session.global_init("../db/db.db")
db_sess = db_session.create_session()
trades = db_sess.query(trade.Trade).all()

pass
