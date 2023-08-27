# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class InlineObject1(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, login=None, password=None):  # noqa: E501
        """InlineObject1 - a model defined in OpenAPI

        :param login: The login of this InlineObject1.  # noqa: E501
        :type login: str
        :param password: The password of this InlineObject1.  # noqa: E501
        :type password: str
        """
        self.openapi_types = {
            'login': str,
            'password': str
        }

        self.attribute_map = {
            'login': 'login',
            'password': 'password'
        }

        self._login = login
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'InlineObject1':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_object_1 of this InlineObject1.  # noqa: E501
        :rtype: InlineObject1
        """
        return util.deserialize_model(dikt, cls)

    @property
    def login(self):
        """Gets the login of this InlineObject1.


        :return: The login of this InlineObject1.
        :rtype: str
        """
        return self._login

    @login.setter
    def login(self, login):
        """Sets the login of this InlineObject1.


        :param login: The login of this InlineObject1.
        :type login: str
        """

        self._login = login

    @property
    def password(self):
        """Gets the password of this InlineObject1.


        :return: The password of this InlineObject1.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this InlineObject1.


        :param password: The password of this InlineObject1.
        :type password: str
        """

        self._password = password