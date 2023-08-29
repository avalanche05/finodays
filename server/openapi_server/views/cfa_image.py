from typing import List

import openapi_server.models as models
from openapi_server.models import PublicUser
import data.__all_models as db_models
from data import db_session
from openapi_server.views import cfa
from openapi_server.models.cfa_image import CfaImage
from utils import entities

# 
from ml.__main__ import predict_price


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

    db_sess.close()
    return cfa_image.id


def get_cfa_images_list() -> List[CfaImage]:
    db_sess = db_session.create_session()
    cfa_images = db_sess.query(db_models.cfa_image.CfaImage).all()

    result = []
    for cfa_image in cfa_images:
        user = entities.get_public_user(cfa_image.user_id)
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

    db_sess.close()
    return cheapest_order.price


def get_predicted_prices(cfa_image_id: int, n_days=3) -> list:
    '''
    Predict prices for cfa depend on last prices
    
    cfa_image_id: Cfa_id model will looking for
    n_days: Number of day, period. When n_days > 1 you can see dynamic
    
    return: n_days-lenght list of float
    '''
    db_sess = db_session.create_session()
    result = predict_price(cfa_image_id=cfa_image_id, is_refit=True, n_days=n_days, db_sess=db_sess)

    return result
