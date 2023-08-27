# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class InlineObject4(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, count=None):  # noqa: E501
        """InlineObject4 - a model defined in OpenAPI

        :param count: The count of this InlineObject4.  # noqa: E501
        :type count: int
        """
        self.openapi_types = {
            'count': int
        }

        self.attribute_map = {
            'count': 'count'
        }

        self._count = count

    @classmethod
    def from_dict(cls, dikt) -> 'InlineObject4':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_object_4 of this InlineObject4.  # noqa: E501
        :rtype: InlineObject4
        """
        return util.deserialize_model(dikt, cls)

    @property
    def count(self):
        """Gets the count of this InlineObject4.


        :return: The count of this InlineObject4.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this InlineObject4.


        :param count: The count of this InlineObject4.
        :type count: int
        """

        self._count = count
