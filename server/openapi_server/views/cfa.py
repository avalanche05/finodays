from data import db_session
from utils import generator
import data.__all_models as db_models


def create_cfa(user_id: int, cfa_image_id: int):
    token = generator.generate_cfa_token()

    cfa = db_models.cfa.Cfa()
    cfa.user_id = user_id
    cfa.cfa_image_id = cfa_image_id
    cfa.token = token

    db_sess = db_session.create_session()
    db_sess.add(cfa)
    db_sess.commit()
