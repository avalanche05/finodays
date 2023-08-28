from typing import List

import openapi_server.models as models
from openapi_server.models import PublicUser
import data.__all_models as db_models
from data import db_session
from openapi_server.views import cfa
from openapi_server.models.cfa_image import CfaImage


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
    return cfa_image.id


def get_cfa_images_list() -> List[CfaImage]:
    db_sess = db_session.create_session()
    cfa_images = db_sess.query(db_models.cfa_image.CfaImage).all()

    result = []
    for cfa_image in cfa_images:
        db_user = db_sess.query(db_models.user.User).get(cfa_image.user_id)
        user = PublicUser()
        user.id = db_user.id
        user.login = db_user.login
        user.username = db_user.username
        user.name = db_user.name
        result.append(
            CfaImage(
                id=cfa_image.id,
                title=cfa_image.title,
                count=cfa_image.count,
                description=cfa_image.description,
                user=user
            )
        )

    db_sess.close()

    return result


def get_lower_price(cfa_image_id: int):
    db_sess = db_session.create_session()

    cheapest_order = db_sess.query(db_models.offer.Offer).filter(
        db_models.offer.Offer.cfa_image_id == cfa_image_id).order_by(db_models.offer.Offer.price).first()

    return cheapest_order.price
