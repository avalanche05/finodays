# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class User(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, email=None, username=None, name=None, balance=None, **_):  # noqa: E501
        """User - a model defined in OpenAPI

        :param id: The id of this User.  # noqa: E501
        :type id: int
        :param email: The email of this User.  # noqa: E501
        :type email: str
        :param username: The username of this User.  # noqa: E501
        :type username: str
        :param name: The name of this User.  # noqa: E501
        :type name: str
        :param balance: The balance of this User.  # noqa: E501
        :type balance: int
        """
        self.openapi_types = {
            'id': int,
            'email': str,
            'username': str,
            'name': str,
            'balance': float
        }

        self.attribute_map = {
            'id': 'id',
            'email': 'email',
            'username': 'username',
            'name': 'name',
            'balance': 'balance'
        }

        self._id = id
        self._email = email
        self._username = username
        self._name = name
        self._balance = balance

    @classmethod
    def from_dict(cls, dikt) -> 'User':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this User.


        :return: The id of this User.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this User.


        :param id: The id of this User.
        :type id: int
        """

        self._id = id

    @property
    def email(self):
        """Gets the email of this User.


        :return: The email of this User.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this User.


        :param email: The email of this User.
        :type email: str
        """

        self._email = email

    @property
    def username(self):
        """Gets the username of this User.


        :return: The username of this User.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this User.


        :param username: The username of this User.
        :type username: str
        """

        self._username = username

    @property
    def name(self):
        """Gets the name of this User.


        :return: The name of this User.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this User.


        :param name: The name of this User.
        :type name: str
        """

        self._name = name

    @property
    def balance(self):
        """Gets the balance of this User.


        :return: The balance of this User.
        :rtype: int
        """
        return self._balance

    @balance.setter
    def balance(self, balance):
        """Sets the balance of this User.


        :param balance: The balance of this User.
        :type balance: int
        """

        self._balance = balance
