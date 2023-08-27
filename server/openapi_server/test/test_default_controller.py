# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.register_user_dto import RegisterUserDTO  # noqa: E501
from openapi_server.models.inline_object1 import InlineObject1  # noqa: E501
from openapi_server.models.inline_object2 import InlineObject2  # noqa: E501
from openapi_server.models.inline_object3 import InlineObject3  # noqa: E501
from openapi_server.models.inline_object4 import InlineObject4  # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.register_response200 import RegisterResponse200  # noqa: E501
from openapi_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from openapi_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from openapi_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from openapi_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from openapi_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_cfa_cfa_token_get(self):
        """Test case for cfa_cfa_token_get

        Получить информацию о CFA по его токену
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa/{cfa_token}'.format(cfa_token='cfa_token_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cfa_history_cfa_token_get(self):
        """Test case for cfa_history_cfa_token_get

        Получить историю сделок для CFA по его токену
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa/history/{cfa_token}'.format(cfa_token='cfa_token_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cfa_image_create_post(self):
        """Test case for cfa_image_create_post

        Создать новый CFA Image (Требуется Bearer-токен)
        """
        inline_object2 = {}
        headers = { 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/cfa-image/create',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object2),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cfa_image_list_get(self):
        """Test case for cfa_image_list_get

        Получить список изображений CFA
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa-image/list',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cfa_image_price_cfa_image_id_get(self):
        """Test case for cfa_image_price_cfa_image_id_get

        Получить цену изображения CFA на основе рыночных предложений
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa-image/price/{cfa_image_id}'.format(cfa_image_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cfa_list_cfa_image_id_get(self):
        """Test case for cfa_list_cfa_image_id_get

        Получить список CFAs для изображения CFA
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa/list/{cfa_image_id}'.format(cfa_image_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cfa_user_id_get(self):
        """Test case for cfa_user_id_get

        Получить список CFA для пользователя
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa/{user_id}'.format(user_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_post(self):
        """Test case for login_post

        Войти как пользователь
        """
        inline_object1 = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/login',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object1),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_offer_buy_offer_id_post(self):
        """Test case for offer_buy_offer_id_post

        Купить предложение (Требуется Bearer-токен)
        """
        inline_object4 = {}
        headers = { 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/offer/buy/{offer_id}'.format(offer_id=56),
            method='POST',
            headers=headers,
            data=json.dumps(inline_object4),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_offer_create_post(self):
        """Test case for offer_create_post

        Создать новое предложение (Требуется Bearer-токен)
        """
        inline_object3 = {}
        headers = { 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/offer/create',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object3),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_offer_list_cfa_image_id_get(self):
        """Test case for offer_list_cfa_image_id_get

        Получить список предложений для изображения CFA
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/offer/list/{cfa_image_id}'.format(cfa_image_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_post(self):
        """Test case for register_post

        Зарегистрировать нового пользователя
        """
        inline_object = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/register',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_trade_list_get(self):
        """Test case for trade_list_get

        Получить список сделок
        """
        query_string = [('cfa-token', 'cfa_token_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trade/list',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_trade_trade_id_get(self):
        """Test case for trade_trade_id_get

        Получить информацию о сделке по ее ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trade/{trade_id}'.format(trade_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
