# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import List, Dict  # noqa: F401

from openapi_server import util
from openapi_server.models.base_model_ import Model


class CfaImageDTO(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, title=None, count=None, description=None):  # noqa: E501
        """CfaImageDTO - a model defined in OpenAPI

        :param id: The id of this CfaImageDTO.  # noqa: E501
        :type id: int
        :param title: The title of this CfaImageDTO.  # noqa: E501
        :type title: str
        :param count: The count of this CfaImageDTO.  # noqa: E501
        :type count: int
        :param description: The description of this CfaImageDTO.  # noqa: E501
        :type description: str
        """
        self.openapi_types = {
            'id': int,
            'title': str,
            'count': int,
            'description': str
        }

        self.attribute_map = {
            'id': 'id',
            'title': 'title',
            'count': 'count',
            'description': 'description'
        }

        self._id = id
        self._title = title
        self._count = count
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'CfaImageDTO':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The cfa_image_dto of this CfaImageDTO.  # noqa: E501
        :rtype: CfaImageDTO
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this CfaImageDTO.


        :return: The id of this CfaImageDTO.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CfaImageDTO.


        :param id: The id of this CfaImageDTO.
        :type id: int
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this CfaImageDTO.


        :return: The title of this CfaImageDTO.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this CfaImageDTO.


        :param title: The title of this CfaImageDTO.
        :type title: str
        """

        self._title = title

    @property
    def count(self):
        """Gets the count of this CfaImageDTO.


        :return: The count of this CfaImageDTO.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this CfaImageDTO.


        :param count: The count of this CfaImageDTO.
        :type count: int
        """

        self._count = count

    @property
    def description(self):
        """Gets the description of this CfaImageDTO.


        :return: The description of this CfaImageDTO.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CfaImageDTO.


        :param description: The description of this CfaImageDTO.
        :type description: str
        """

        self._description = description
