import connexion
import six

from openapi_server.models.register_user_dto import RegisterUserDTO  # noqa: E501
from openapi_server.models.inline_object1 import LoginUserDTO  # noqa: E501
from openapi_server.models.inline_object2 import CreateCfaImageDTO  # noqa: E501
from openapi_server.models.inline_object3 import InlineObject3  # noqa: E501
from openapi_server.models.inline_object4 import InlineObject4  # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.register_response200 import LoginResponse200  # noqa: E501
from openapi_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from openapi_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from openapi_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from openapi_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from openapi_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from openapi_server import util
from views import user
from views import cfa_image


def cfa_cfa_token_get(cfa_token):  # noqa: E501
    """Получить информацию о CFA по его токену

     # noqa: E501

    :param cfa_token: 
    :type cfa_token: str

    :rtype: InlineResponse2004
    """
    return 'do some magic!'


def cfa_history_cfa_token_get(cfa_token):  # noqa: E501
    """Получить историю сделок для CFA по его токену

     # noqa: E501

    :param cfa_token: 
    :type cfa_token: str

    :rtype: List[InlineResponse2005]
    """
    return 'do some magic!'


def cfa_image_create_post():  # noqa: E501
    """Создать новый CFA Image (Требуется Bearer-токен)

     # noqa: E501

    :param create_cfa_image:
    :type create_cfa_image: dict | bytes

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


    :rtype: List[InlineResponse2002]
    """
    return 'do some magic!'


def cfa_image_price_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить цену изображения CFA на основе рыночных предложений

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: InlineResponse2003
    """
    return 'do some magic!'


def cfa_list_cfa_image_id_get(cfa_image_id):  # noqa: E501
    """Получить список CFAs для изображения CFA

     # noqa: E501

    :param cfa_image_id: 
    :type cfa_image_id: int

    :rtype: List[InlineResponse2004]
    """
    return 'do some magic!'


def cfa_user_id_get(user_id):  # noqa: E501
    """Получить список CFA для пользователя

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: List[InlineResponse200]
    """
    return 'do some magic!'


def login_post():  # noqa: E501
    """Войти как пользователь

     # noqa: E501

    :param inline_object1: 
    :type inline_object1: dict | bytes

    :rtype: LoginResponse200
    """
    if connexion.request.is_json:
        login_user_dto = LoginUserDTO.from_dict(connexion.request.get_json())  # noqa: E501

        return user.login(login_user_dto)
    return None, 401


def offer_buy_offer_id_post(offer_id, inline_object4):  # noqa: E501
    """Купить предложение (Требуется Bearer-токен)

     # noqa: E501

    :param offer_id: 
    :type offer_id: int
    :param inline_object4: 
    :type inline_object4: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        inline_object4 = InlineObject4.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def offer_create_post(inline_object3):  # noqa: E501
    """Создать новое предложение (Требуется Bearer-токен)

     # noqa: E501

    :param inline_object3: 
    :type inline_object3: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        inline_object3 = InlineObject3.from_dict(connexion.request.get_json())  # noqa: E501
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

    return None, 400


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

    :rtype: InlineResponse2005
    """
    return 'do some magic!'
