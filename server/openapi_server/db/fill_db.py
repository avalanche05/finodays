from data import db_session
from models import CreateCfaImageDTO, CreateOfferDTO, DepositValueDTO, CreateDesireDTO
from openapi_server.views import cfa_image
from openapi_server.views import user, cfa_image, offer, trade, cfa, desire
from openapi_server import models

if __name__ == '__main__':
    db_session.global_init("./db.db")

    user1 = user.register(models.register_user_dto.RegisterUserDTO("m@m.m", "skewb", "mihail", "qwerty"))
    user2 = user.register(models.register_user_dto.RegisterUserDTO("i@i.i", "buran", "ivan", "qwerty"))

    cfa_image.create_cfa_image(user1.user.id, CreateCfaImageDTO('coin1', 15, 'coin number 1'))
    cfa_image.create_cfa_image(user2.user.id, CreateCfaImageDTO('coin2', 15, 'coin number 2'))
    cfa_image.create_cfa_image(user2.user.id, CreateCfaImageDTO('coin3', 15, 'coin number 3'))