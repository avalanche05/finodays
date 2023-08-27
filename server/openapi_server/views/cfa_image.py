import models
import data.__all_models as db_models
from data import db_session
from views import cfa


def create_cfa_image(user_id: int, create_cfo_image_dto: models.CreateCfaImageDTO):
    cfa_image = db_models.cfa_image.CfaImage()
    cfa_image.user_id = user_id
    cfa_image.title = create_cfo_image_dto.title
    cfa_image.description = create_cfo_image_dto.description
    cfa_image.count = create_cfo_image_dto.count

    db_sess = db_session.create_session()
    db_sess.add(cfa_image)
    db_sess.commit()

    for _ in range(create_cfo_image_dto.count):
        cfa.create_cfa(user_id, cfa_image.id)
    return True
