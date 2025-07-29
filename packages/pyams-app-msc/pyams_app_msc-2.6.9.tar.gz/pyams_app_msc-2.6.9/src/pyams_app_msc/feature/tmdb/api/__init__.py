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

"""PyAMS_app_msc.feature.tmdb.api module

This module provides an endpoint for querying the TMDB service.
"""

from cornice import Service
from cornice.validators import colander_validator
from pyramid.httpexceptions import HTTPOk

from pyams_app_msc.feature.tmdb import ITMDBService
from pyams_app_msc.feature.tmdb.api.schema import MovieSearchRequest, MovieSearchResponse
from pyams_app_msc.feature.tmdb.interfaces import TMDB_SEARCH_ROUTE
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_security.rest import check_cors_origin, set_cors_headers
from pyams_utils.factory import create_object
from pyams_utils.rest import STATUS, rest_responses

__docformat__ = 'restructuredtext'


tmdb_service = Service(name=TMDB_SEARCH_ROUTE,
                       pyramid_route=TMDB_SEARCH_ROUTE,
                       description="TMDB search service")


@tmdb_service.options(validators=(check_cors_origin, set_cors_headers))
def tmdb_service_options(request):
    """TMDB search service options handler"""


tmdb_service_get_responses = rest_responses.copy()
tmdb_service_get_responses[HTTPOk.code] = MovieSearchResponse(description="TMDB search response")


@tmdb_service.get(permission=USE_INTERNAL_API_PERMISSION,
                  schema=MovieSearchRequest(),
                  validators=(check_cors_origin, colander_validator, set_cors_headers),
                  response_schemas=tmdb_service_get_responses)
def find_movies(request):
    """TMDB movies finder"""
    params = request.validated.get('querystring', {})
    query = params.get('term')
    if not query:
        return {
            'status': STATUS.ERROR.value,
            'message': "Missing arguments",
            'results': []
        }
    service = create_object(ITMDBService)
    if (service is None) or (service.configuration is None):
        return {
            'status': STATUS.ERROR.value,
            'message': "Service unavailable",
            'results': []
        }
    return {
        'status': STATUS.SUCCESS.value,
        'results': sorted([
            {
                'id': f"movie_id::{movie['movie_id']}",
                'text': f"{movie['title']} ({movie['release_year']})" if ('release_year' in movie) else movie['title']
            }
            for movie in service.find_movies(query)
        ], key=lambda x: x['text'])
    }
