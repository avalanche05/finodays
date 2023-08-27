# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class InlineResponse200(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, cfa_image_id=None, count=None):  # noqa: E501
        """InlineResponse200 - a model defined in OpenAPI

        :param cfa_image_id: The cfa_image_id of this InlineResponse200.  # noqa: E501
        :type cfa_image_id: int
        :param count: The count of this InlineResponse200.  # noqa: E501
        :type count: int
        """
        self.openapi_types = {
            'cfa_image_id': int,
            'count': int
        }

        self.attribute_map = {
            'cfa_image_id': 'cfa_image_id',
            'count': 'count'
        }

        self._cfa_image_id = cfa_image_id
        self._count = count

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse200':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200 of this InlineResponse200.  # noqa: E501
        :rtype: InlineResponse200
        """
        return util.deserialize_model(dikt, cls)

    @property
    def cfa_image_id(self):
        """Gets the cfa_image_id of this InlineResponse200.


        :return: The cfa_image_id of this InlineResponse200.
        :rtype: int
        """
        return self._cfa_image_id

    @cfa_image_id.setter
    def cfa_image_id(self, cfa_image_id):
        """Sets the cfa_image_id of this InlineResponse200.


        :param cfa_image_id: The cfa_image_id of this InlineResponse200.
        :type cfa_image_id: int
        """

        self._cfa_image_id = cfa_image_id

    @property
    def count(self):
        """Gets the count of this InlineResponse200.


        :return: The count of this InlineResponse200.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this InlineResponse200.


        :param count: The count of this InlineResponse200.
        :type count: int
        """

        self._count = count