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

"""PyAMS_app_msc.feature.tmdb.api.schema module

This module defines the schema definition for TMDB API service.
"""

from colander import MappingSchema, SchemaNode, String

from pyams_utils.rest import BaseResponseSchema

__docformat__ = 'restructuredtext'


class MovieSearchQuery(MappingSchema):
    """Movie search schema"""
    term = SchemaNode(String(),
                      description="Query string")


class MovieSearchRequest(MappingSchema):
    """Movie search request schema"""
    querystring = MovieSearchQuery()


class MovieItem(MappingSchema):
    """Movie item schema"""
    id = SchemaNode(String(),
                    description="Movie ID")
    text = SchemaNode(String(),
                      description="Movie title and year")


class MovieList(BaseResponseSchema):
    """Movies list schema"""
    result = MovieItem()


class MovieSearchResponse(MappingSchema):
    """Movie search response"""
    body = MovieList()
