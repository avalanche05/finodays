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
from openapi_server.models.user import User
from openapi_server.models.public_user import PublicUser
from openapi_server.models.deposit_value_dto import DepositValueDTO
from openapi_server.models.withdraw_value_dto import WithdrawValueDTO
from openapi_server import util
from openapi_server.views import user
from openapi_server.views import cfa
from openapi_server.views import cfa_image
from openapi_server.views import offer
from openapi_server.views import trade


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
            token = connexion.request.headers.get('Authorization').split()[1]
            user_id = user.get_profile(token).id
        except Exception as e:
            return f"Bearer token is invalid", 401

        try:
            cfa_image.create_cfa_image(user_id, create_cfa_image)
            return None, 200
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


def cfa_user_id_get(user_id):  # noqa: E501
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
        user_id = user.get_profile(token).id

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
        user_id = user.get_profile(token).id

        try:
            offer.create(user_id, create_offer_dto)
            return "Offer create success", 201
        except Exception as e:
            return str(e), 400

    return 'invalid data in request', 400


def offer_list_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить список предложений для изображения CFA

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: List[InlineResponse2006]
    """

    try:
        offers = offer.get_all_by_cfa_image_id(cfa_image_id)
        return offers, 200
    except Exception as e:
        return str(e), 400

    return "Invalid request", 400


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
        return user.get_profile(token), 200
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
