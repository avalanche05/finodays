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
from openapi_server.models.cfa_dto import CfaDTO  # noqa: E501
from openapi_server.models.trade_dto import TradeDTO  # noqa: E501
from openapi_server.models.offer_dto import OfferDTO  # noqa: E501
from openapi_server import util
from openapi_server.views import user
from openapi_server.views import cfa
from openapi_server.views import cfa_image


def cfa_cfa_token_get(cfa_token):  # noqa: E501
    """Получить информацию о CFA по его токену

     # noqa: E501

    :param cfa_token: 
    :type cfa_token: str

    :rtype: CfaDTO
    """

    return cfa.get_cfa(cfa_token)


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

    :rtype: None
    """
    if connexion.request.is_json:
        create_cfa_image = CreateCfaImageDTO.from_dict(connexion.request.get_json())  # noqa: E501

        try:
            cfa_image.create_cfa_image(1, create_cfa_image)
            return None, 200
        except Exception as e:
            return str(e), 401

    return "Request has no data", 401


def cfa_image_list_get():  # noqa: E501
    """Получить список изображений CFA

     # noqa: E501


    :rtype: List[CfaImageDTO]
    """
    return 'do some magic!'


def cfa_image_price_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить цену изображения CFA на основе рыночных предложений

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: CfaPriceDTO
    """
    return 'do some magic!'


def cfa_list_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить список CFAs для изображения CFA

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: List[CfaDTO]
    """
    return 'do some magic!'


def cfa_user_id_get(user_id):  # noqa: E501
    """Получить список CFA для пользователя

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: List[UserCfaDTO]
    """
    return 'do some magic!'


def login_post():  # noqa: E501
    """Войти как пользователь

     # noqa: E501

    :rtype: LoginResponse200
    """
    if connexion.request.is_json:
        login_user_dto = LoginUserDTO.from_dict(connexion.request.get_json())  # noqa: E501

        return user.login(login_user_dto)
    return "Invalid credentials", 401


def offer_buy_offer_id_post(offer_id, accept_offer_dto):  # noqa: E501
    """Купить предложение (Требуется Bearer-токен)

     # noqa: E501

    :param offer_id: 
    :type offer_id: int
    :param accept_offer_dto:
    :type accept_offer_dto: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        accept_offer_dto = AcceptOfferDTO.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def offer_create_post():  # noqa: E501
    """Создать новое предложение (Требуется Bearer-токен)

     # noqa: E501

    :rtype: None
    """
    if connexion.request.is_json:
        create_offer_dto = CreateOfferDTO.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def offer_list_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить список предложений для изображения CFA

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: List[InlineResponse2006]
    """
    return 'do some magic!'


def register_post():  # noqa: E501
    """Зарегистрировать нового пользователя

     # noqa: E501

    :rtype: LoginResponse200
    """
    if connexion.request.is_json:
        register_user_dto = RegisterUserDTO.from_dict(connexion.request.get_json())  # noqa: E501

        return user.register(register_user_dto)

    return "Invalid request", 400


def trade_list_get(cfa_token=None):  # noqa: E501
    """Получить список сделок

     # noqa: E501

    :param cfa_token: 
    :type cfa_token: str

    :rtype: List[InlineResponse2005]
    """
    return 'do some magic!'


def trade_trade_id_get(trade_id):  # noqa: E501
    """Получить информацию о сделке по ее ID

     # noqa: E501

    :param trade_id: 
    :type trade_id: int

    :rtype: TradeDTO
    """
    return 'do some magic!'

def profile_get():
    """Получить информацию о своём профиле

     # noqa: E501

    :rtype: TradeDTO
    """
    return 'do some magic!'