# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class RegisterUserDTO(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, login=None, username=None, name=None, password=None):  # noqa: E501
        """RegisterUserDTO - a model defined in OpenAPI

        :param login: The login of this RegisterUserDTO.  # noqa: E501
        :type login: str
        :param username: The username of this RegisterUserDTO.  # noqa: E501
        :type username: str
        :param name: The name of this RegisterUserDTO.  # noqa: E501
        :type name: str
        :param password: The password of this RegisterUserDTO.  # noqa: E501
        :type password: str
        """
        self.openapi_types = {
            'login': str,
            'username': str,
            'name': str,
            'password': str
        }

        self.attribute_map = {
            'login': 'login',
            'username': 'username',
            'name': 'name',
            'password': 'password'
        }

        self._login = login
        self._username = username
        self._name = name
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'RegisterUserDTO':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The register_user_dto of this RegisterUserDTO.  # noqa: E501
        :rtype: RegisterUserDTO
        """
        return util.deserialize_model(dikt, cls)

    @property
    def login(self):
        """Gets the login of this RegisterUserDTO.


        :return: The login of this RegisterUserDTO.
        :rtype: str
        """
        return self._login

    @login.setter
    def login(self, login):
        """Sets the login of this RegisterUserDTO.


        :param login: The login of this RegisterUserDTO.
        :type login: str
        """

        self._login = login

    @property
    def username(self):
        """Gets the username of this RegisterUserDTO.


        :return: The username of this RegisterUserDTO.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this RegisterUserDTO.


        :param username: The username of this RegisterUserDTO.
        :type username: str
        """

        self._username = username

    @property
    def name(self):
        """Gets the name of this RegisterUserDTO.


        :return: The name of this RegisterUserDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RegisterUserDTO.


        :param name: The name of this RegisterUserDTO.
        :type name: str
        """

        self._name = name

    @property
    def password(self):
        """Gets the password of this RegisterUserDTO.


        :return: The password of this RegisterUserDTO.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this RegisterUserDTO.


        :param password: The password of this RegisterUserDTO.
        :type password: str
        """

        self._password = password