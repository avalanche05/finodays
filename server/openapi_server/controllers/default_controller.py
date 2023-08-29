import connexion
import six

from openapi_server.models.register_user_dto import RegisterUserDTO  # noqa: E501
from openapi_server.models.login_user_dto import LoginUserDTO  # noqa: E501
from openapi_server.models.create_cfa_image_dto import CreateCfaImageDTO  # noqa: E501
from openapi_server.models.create_offer_dto import CreateOfferDTO  # noqa: E501
from openapi_server.models.accept_offer_dto import AcceptOfferDTO  # noqa: E501
from openapi_server.models.user_cfa_dto import UserCfaDTO  # noqa: E501
from openapi_server.models.login_response_200 import LoginResponse200  # noqa: E501
from openapi_server.models.cfa_image_dto import CfaImageDTO  # noqa: E501
from openapi_server.models.cfa_price_dto import CfaPriceDTO  # noqa: E501
from openapi_server.models.cfa_image_id_dto import CfaImageIdDTO  # noqa: E501
from openapi_server.models.cfa_dto import CfaDTO  # noqa: E501
from openapi_server.models.trade_dto import TradeDTO  # noqa: E501
from openapi_server.models.offer_dto import OfferDTO  # noqa: E501
from openapi_server.models.accept_desire_dto import AcceptDesireDTO  # noqa: E501
from openapi_server.models.desire_dto import DesireDTO  # noqa: E501
from openapi_server.models.create_desire_dto import CreateDesireDTO  # noqa: E501
from openapi_server.models.create_deal_dto import CreateDealDTO  # noqa: E501
from openapi_server.models.user import User
from openapi_server.models.public_user import PublicUser
from openapi_server.models.deposit_value_dto import DepositValueDTO
from openapi_server.models.withdraw_value_dto import WithdrawValueDTO
from openapi_server import util
from openapi_server.views import user
from openapi_server.views import cfa
from openapi_server.views import cfa_image
from openapi_server.views import offer
from openapi_server.views import desire
from openapi_server.views import trade
from openapi_server.views import deal
from utils import entities


def cfa_cfa_token_get(cfa_token):  # noqa: E501
    """Получить информацию о CFA по его токену

     # noqa: E501

    :param cfa_token: 
    :type cfa_token: str

    :rtype: CfaDTO
    """
    try:
        return cfa.get_cfa(cfa_token), 200
    except Exception as e:
        return str(e), 404


def cfa_history_cfa_token_get(cfa_token):  # noqa: E501
    """Получить историю сделок для CFA по его токену

     # noqa: E501

    :param cfa_token: 
    :type cfa_token: str

    :rtype: List[TradeDTO]
    """
    return cfa.get_cfa_history(cfa_token)


def cfa_image_create_post():  # noqa: E501
    """Создать новый CFA Image (Требуется Bearer-токен)

     # noqa: E501

    :rtype: CfaImageIdDTO
    """
    if connexion.request.is_json:
        create_cfa_image = CreateCfaImageDTO.from_dict(connexion.request.get_json())  # noqa: E501
        try:
            token = connexion.request.headers.get('Authorization').split()[1]
            user_id = entities.get_user_by_token(token).id
        except Exception as e:
            return f"Bearer token is invalid", 401

        try:
            cfa_image_id = cfa_image.create_cfa_image(user_id, create_cfa_image)
            return CfaImageIdDTO(cfa_image_id), 200
        except Exception as e:
            return str(e), 401

    return "Request has no data", 401


def cfa_image_list_get():  # noqa: E501
    """Получить список изображений CFA

     # noqa: E501


    :rtype: List[CfaImageDTO]
    """

    cfa_images = cfa_image.get_cfa_images_list()
    return cfa_images, 200


def cfa_image_price_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить цену изображения CFA на основе рыночных предложений

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: CfaPriceDTO
    """

    try:
        price = cfa_image.get_lower_price(cfa_image_id)
    except Exception as e:
        return str(e), 404

    return CfaPriceDTO(price=price)


def cfa_list_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить список CFAs для изображения CFA

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: List[CfaDTO]
    """

    try:
        cfa_list = cfa.get_cfa_list(cfa_image_id)
        return cfa_list, 200
    except Exception as e:
        return str(e), 404


def user_cfa_user_id_get(user_id):  # noqa: E501
    """Получить список CFA для пользователя

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: List[UserCfaDTO]
    """

    try:
        user_cfas = user.get_cfa_list(user_id)
        return user_cfas, 200
    except Exception as e:
        return str(e), 404


def login_post():  # noqa: E501
    """Войти как пользователь

     # noqa: E501

    :rtype: LoginResponse200
    """
    if connexion.request.is_json:
        login_user_dto = LoginUserDTO.from_dict(connexion.request.get_json())  # noqa: E501

        return user.login(login_user_dto)
    return "Invalid credentials", 401


def offer_buy_offer_id_post(offer_id):  # noqa: E501
    """Купить предложение (Требуется Bearer-токен)

     # noqa: E501

    :param offer_id: 
    :type offer_id: int
    :param accept_offer_dto:
    :type accept_offer_dto: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        accept_offer_dto = AcceptOfferDTO.from_dict(connexion.request.get_json())

        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id

        try:
            offer.buy(offer_id=offer_id,
                      user_id=user_id,
                      count=accept_offer_dto.count)
            return "Offer buy success", 201
        except Exception as e:
            return str(e), 400

    return 'invalid data in request', 400


def offer_create_post():  # noqa: E501
    """Создать новое предложение (Требуется Bearer-токен)

     # noqa: E501

    :rtype: None
    """
    if connexion.request.is_json:
        create_offer_dto = CreateOfferDTO.from_dict(connexion.request.get_json())  # noqa: E501
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id

        try:
            offer_id = offer.create(user_id, create_offer_dto)
            return {"id": offer_id}, 201
        except Exception as e:
            return str(e), 400

    return 'invalid data in request', 400


def offer_list_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить список предложений для изображения CFA

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: List[OfferDTO]
    """

    try:
        offers = offer.get_all_by_cfa_image_id(cfa_image_id)
        return offers, 200
    except Exception as e:
        return str(e), 400


def register_post():  # noqa: E501
    """Зарегистрировать нового пользователя

     # noqa: E501

    :rtype: LoginResponse200
    """
    if connexion.request.is_json:
        register_user_dto = RegisterUserDTO.from_dict(connexion.request.get_json())  # noqa: E501

        return user.register(register_user_dto)

    return "Invalid request", 400


def trade_list_get():  # noqa: E501
    """Получить список сделок

     # noqa: E501

    :rtype: List[TradeDTO]
    """

    trades = trade.get_all()
    return trades, 200


def trade_trade_id_get(trade_id):  # noqa: E501
    """Получить информацию о сделке по ее ID

     # noqa: E501

    :param trade_id: 
    :type trade_id: int

    :rtype: TradeDTO
    """
    result = trade.get_by_id(trade_id)
    return result, 200


def profile_get():
    """Получить информацию о своём профиле

    # noqa: E501

    :rtype: User
    """

    token = connexion.request.headers.get('Authorization').split()[1]

    try:
        return entities.get_user_by_token(token), 200
    except Exception as e:
        return str(e), 401


def user_user_id_get(user_id):
    """Получить информацию о профиле другого пользователя

    # noqa: E501

    :param user_id:
    :type user_id: int

    :rtype: PublicUser
    """
    try:
        return user.get_user(user_id), 200
    except Exception as e:
        return str(e), 404


def user_deposit_post():
    """Получить информацию о профиле другого пользователя

    # noqa: E501

    :rtype: None
    """
    if connexion.request.is_json:
        token = connexion.request.headers.get('Authorization').split()[1]
        deposit_value_dto = DepositValueDTO.from_dict(connexion.request.get_json())  # noqa: E501

        try:
            user.deposit_money(deposit_value_dto, token)
            return None, 200
        except Exception as e:
            return str(e), 401

    return "Invalid credentials", 401


def user_withdraw_post():
    """Получить информацию о профиле другого пользователя

    # noqa: E501

    :rtype: None
    """
    if connexion.request.is_json:
        token = connexion.request.headers.get('Authorization').split()[1]
        withdraw_value_dto = WithdrawValueDTO.from_dict(connexion.request.get_json())  # noqa: E501

        try:
            user.withdraw_money(withdraw_value_dto, token)
            return None, 200
        except Exception as e:
            return str(e), 401

    return "Invalid credentials", 401


def user_offer_user_id_get(user_id: int):
    """Получить список всех своих предложений

    # noqa: E501

    :rtype: List[OfferDTO]
    """
    try:
        offers = user.get_offer_list(user_id)
        return offers, 201
    except Exception as e:
        return str(e), 400


def offer_cancel_offer_id_post(offer_id: int):  # noqa: E501
    """Удалить предложение (Требуется Bearer-токен)

     # noqa: E501

    :rtype: None
    """
    try:
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id
        offer.cancel_offer(user_id=user_id, offer_id=offer_id)
        return "Delete offer success", 201
    except Exception as e:
        return str(e), 400


def desire_sell_desire_id_post(desire_id):  # noqa: E501
    """Продать cfa (Требуется Bearer-токен)

     # noqa: E501

    :param desire_id:
    :type desire_id: int
    :param accept_desire_dto:
    :type accept_desire_dto: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        accept_desire_dto = AcceptDesireDTO.from_dict(connexion.request.get_json())

        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id

        try:
            desire.sell(desire_id=desire_id,
                        user_id=user_id,
                        count=accept_desire_dto.count)
            return "desire buy success", 201
        except Exception as e:
            return str(e), 400

    return 'invalid data in request', 400


def desire_create_post():  # noqa: E501
    """Создать новое предложение (Требуется Bearer-токен)

     # noqa: E501

    :rtype: None
    """
    if connexion.request.is_json:
        create_desire_dto = CreateDesireDTO.from_dict(connexion.request.get_json())  # noqa: E501
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id

        try:
            desire_id = desire.create(user_id, create_desire_dto)
            return {"id": desire_id}, 201
        except Exception as e:
            return str(e), 400

    return 'invalid data in request', 400


def desire_list_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить список желаний для изображения CFA

     # noqa: E501

    :param cfa_image_id:
    :type cfa_image_id: int

    :rtype: List[DesireDTO]
    """

    try:
        desires = desire.get_all_by_cfa_image_id(cfa_image_id)
        return desires, 200
    except Exception as e:
        return str(e), 400


def user_desire_user_id_get(user_id: int):
    """Получить список всех своих предложений

    # noqa: E501

    :rtype: List[DesireDTO]
    """
    try:
        desires = user.get_desire_list(user_id)
        return desires, 201
    except Exception as e:
        return str(e), 400


def desire_cancel_desire_id_post(desire_id):  # noqa: E501
    """Удалить предложение (Требуется Bearer-токен)

     # noqa: E501

    :rtype: None
    """
    try:
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id
        desire.cancel(user_id=user_id, desire_id=desire_id)
        return "Delete desire success", 201
    except Exception as e:
        return str(e), 400


def deal_accept_deal_id_post(deal_id):  # noqa: E501
    """Согласиться на обмен (Требуется Bearer-токен)

     # noqa: E501

    :param deal_id:
    :type deal_id: int

    :rtype: None
    """
    try:
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id
        deal.accept(user_id=user_id, deal_id=deal_id)
        return None, 200
    except Exception as e:
        return str(e), 401


def deal_create_post():  # noqa: E501
    """Создать новый обмен (Требуется Bearer-токен)

     # noqa: E501

    :rtype: None
    """
    try:
        create_deal_dto = CreateDealDTO.from_dict(connexion.request.get_json())# noqa: E501
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id
        deal.create(initiator_id=user_id, create_deal=create_deal_dto)
        return None, 200
    except Exception as e:
        return str(e), 401


def user_deal_in_get():
    """Получить список всех обменов, направленных пользователю

    # noqa: E501

    :rtype: List[DealDTO]
    """
    try:
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id
        deals = deal.get_all_in_deals(user_id=user_id)
        return deals, 200
    except Exception as e:
        return str(e), 401


def user_deal_out_get():
    """Получить список всех обменов, созданных пользователем

    # noqa: E501

    :rtype: List[DealDTO]
    """
    try:
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id
        deals = deal.get_all_out_deals(user_id=user_id)
        return deals, 200
    except Exception as e:
        return str(e), 401


def deal_cancel_deal_id_post(deal_id):  # noqa: E501
    """Удалить обмен (Требуется Bearer-токен)

     # noqa: E501

    :rtype: None
    """
    try:
        token = connexion.request.headers.get('Authorization').split()[1]
        user_id = entities.get_user_by_token(token).id
        deal.cancel(user_id=user_id, deal_id=deal_id)
        return None, 200
    except Exception as e:
        return str(e), 401


def cfa_image_predict_price(cfa_image_id: int):
    """Получить список предполагаемых цен CfaImage на ближайшие 3 дня

         # noqa: E501

        :rtype: List[int]
        """
    return [103, 91, 112], 200
