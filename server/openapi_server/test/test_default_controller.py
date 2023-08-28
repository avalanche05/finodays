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


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""
    correct_cfa_token = 'cd33b12ca181fe2d1e60029ecb9689f19690d7d71cc6d8d1a62b1130d40f9593'
    incorrect_cfa_token = 'abcdefg'
    correct_bearer_token = 'CGvVeabRxhUmdlRReIJF'
    incorrect_bearer_token = 'abcdefg'
    correct_cfa_image_id = 1
    incorrect_cfa_image_id = -1

    def setUp(self) -> None:
        db_session.global_init('../db/db.db')




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


if __name__ == '__main__':
    unittest.main()
