# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class CreateDealDTO(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, initiator_items=None, host_items=None):  # noqa: E501
        """CreateDealDTO - a model defined in OpenAPI

        :param initiator_items: The initiator_items of this CreateDealDTO.  # noqa: E501
        :type initiator_items: list
        :param host_items: The host_items of this CreateDealDTO.  # noqa: E501
        :type host_items: list
        """
        self.openapi_types = {
            'initiator_items': list,
            'host_items': list
        }

        self.attribute_map = {
            'initiator_items': 'initiator_items',
            'host_items': 'host_items'
        }

        self._initiator_items = initiator_items
        self._host_items = host_items

    @classmethod
    def from_dict(cls, dikt) -> 'CreateDealDTO':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The create_Desire_dto of this CreateDealDTO.  # noqa: E501
        :rtype: CreateDealDTO
        """
        return util.deserialize_model(dikt, cls)

    @property
    def initiator_items(self):
        """Gets the initiator_items of this CreateDealDTO.


        :return: The initiator_items of this CreateDealDTO.
        :rtype: list
        """
        return self._initiator_items

    @initiator_items.setter
    def initiator_items(self, initiator_items):
        """Sets the initiator_items of this CreateDealDTO.


        :param initiator_items: The initiator_items of this CreateDealDTO.
        :type initiator_items: list
        """

        self._initiator_items = initiator_items

    @property
    def host_items(self):
        """Gets the host_items of this CreateDealDTO.


        :return: The host_items of this CreateDealDTO.
        :rtype: list
        """
        return self._host_items

    @host_items.setter
    def host_items(self, host_items):
        """Sets the host_items of this CreateDealDTO.


        :param host_items: The host_items of this CreateDealDTO.
        :type host_items: list
        """

        self._host_items = host_items

    @property
    def price(self):
        """Gets the price of this CreateDealDTO.


        :return: The price of this CreateDealDTO.
        :rtype: int
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this CreateDealDTO.


        :param price: The price of this CreateDealDTO.
        :type price: int
        """

        self._price = price
