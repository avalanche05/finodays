# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

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
from openapi_server.test import BaseTestCase
from data import db_session
import models


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""
    correct_cfa_token = 'c6741b9aafff4c991c0658e03e730fb6d35b1812d939548e95aca9b7e5c9aaa1'
    incorrect_cfa_token = 'abcdefg'
    correct_bearer_token = 'SrcAdlIJlfsLYCOepIyO'
    incorrect_bearer_token = 'abcdefg'
    correct_cfa_image_id = 1
    incorrect_cfa_image_id = -1
    correct_offer_id = 1
    incorrect_offer_id = -1
    correct_user_id = 1
    incorrect_user_id = -1

    def setUp(self) -> None:
        db_session.global_init('../../db/db.db')

    def test_cfa_history_cfa_token_get(self):
        """Test case for cfa_history_cfa_token_get

        Получить историю сделок для CFA по его токену
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa/history/{cfa_token}'.format(cfa_token=self.correct_cfa_token),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/cfa/history/{cfa_token}'.format(cfa_token=self.incorrect_cfa_token),
            method='GET',
            headers=headers)
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cfa_list_cfa_image_id_get(self):
        """Test case for cfa_list_cfa_image_id_get

        Получить список CFAs для изображения CFA
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa/list/{cfa_image_id}'.format(cfa_image_id=self.correct_cfa_image_id),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        response = self.client.open(
            '/cfa/list/{cfa_image_id}'.format(cfa_image_id=self.incorrect_cfa_image_id),
            method='GET',
            headers=headers)
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cfa_cfa_token_get(self):
        """Test case for cfa_cfa_token_get

        Получить информацию о CFA по его токену
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cfa/{cfa_token}'.format(cfa_token=self.correct_cfa_token),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/cfa/history/{cfa_token}'.format(cfa_token=self.incorrect_cfa_token),
            method='GET',
            headers=headers)
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_offer_list_cfa_image_id_get(self):
        """Test case for offer_list_cfa_image_id_get

        Получить список предложений для изображения CFA
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/offer/list/{cfa_image_id}'.format(cfa_image_id=self.correct_cfa_image_id),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/offer/list/{cfa_image_id}'.format(cfa_image_id=self.incorrect_cfa_image_id),
            method='GET',
            headers=headers)
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_trade_list_get(self):
        """Test case for trade_list_get

        Получить список сделок
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trade/list',
            method='GET',
            headers=headers)
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

    def test_user_profile_get(self):
        """Test case for user_profile_get

        Получить информацию о своём пользователе
        """
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.correct_bearer_token}',
        }
        response = self.client.open(
            '/user/profile',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.incorrect_bearer_token}',
        }
        response = self.client.open(
            '/user/profile',
            method='GET',
            headers=headers)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_user_id_get(self):
        """Test case for user_user_id_get

        Получить информацию о профиле другого человека
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/user/{user_id}'.format(user_id=self.correct_user_id),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        response = self.client.open(
            '/user/{user_id}'.format(user_id=self.incorrect_user_id),
            method='GET',
            headers=headers)
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
