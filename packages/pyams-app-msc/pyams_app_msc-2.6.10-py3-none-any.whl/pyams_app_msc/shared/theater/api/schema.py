#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

from colander import Boolean, Float, Int, MappingSchema, SchemaNode, String, drop

from pyams_utils.rest import BaseResponseSchema


class PriceGetterQuery(MappingSchema):
    """Price getter query schema"""
    price_id = SchemaNode(String(),
                          description="Price ID")


class PriceGetterRequest(MappingSchema):
    """Price getter request"""
    querystring = PriceGetterQuery()


class PriceInfo(MappingSchema):
    """Price info schema"""
    id = SchemaNode(String(),
                    description="Price ID")
    active = SchemaNode(Boolean(),
                        description="Active price flag")
    name = SchemaNode(String(),
                      description="Price name")
    participant_price = SchemaNode(Float(),
                                   description="Participant price")
    accompanying_price = SchemaNode(Float(),
                                    description="Accompanying price")
    accompanying_ratio = SchemaNode(Int(),
                                    description="Accompanying ratio")
    comment = SchemaNode(String(),
                         description="Comments",
                         missing=drop)


class PriceGetterResult(BaseResponseSchema):
    """Price getter result schema"""
    price = PriceInfo()


class PriceGetterResponse(MappingSchema):
    """Price getter response"""
    body = PriceGetterResult()


class RoomInfo(MappingSchema):
    """Room info schema"""
    id = SchemaNode(String(),
                    description="Room ID")
    name = SchemaNode(String(),
                      description="Room name")
    capacity = SchemaNode(Int(),
                          description="Room capacity")


class RoomGetterResult(BaseResponseSchema):
    """Room getter result schema"""
    room = RoomInfo()


class RoomGetterResponse(MappingSchema):
    """Room getter response"""
    body = RoomGetterResult()
