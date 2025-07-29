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

from cornice import Service
from cornice.validators import colander_validator
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPOk

from pyams_app_msc.shared.theater import ICinemaRoomContainer, IMovieTheater
from pyams_app_msc.shared.theater.api.interfaces import MSC_ROOM_API_ROUTE
from pyams_app_msc.shared.theater.api.schema import RoomGetterResponse
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_security.rest import check_cors_origin, set_cors_headers
from pyams_utils.registry import query_utility
from pyams_utils.rest import STATUS, http_error, rest_responses

__docformat__ = 'restructuredtext'


room_service = Service(name=MSC_ROOM_API_ROUTE,
                       pyramid_route=MSC_ROOM_API_ROUTE,
                       description="Room getter service")


@room_service.options(validators=(check_cors_origin, set_cors_headers))
def room_options(request):
    """Room service options"""
    return ''


room_get_responses = rest_responses.copy()
room_get_responses[HTTPOk.code] = RoomGetterResponse(
    description='Room getter result')


@room_service.get(permission=USE_INTERNAL_API_PERMISSION,
                  validators=(check_cors_origin, colander_validator, set_cors_headers),
                  response_schemas=room_get_responses)
def get_room(request):
    """Get room information"""
    theater_name = request.matchdict.get('theater_name')
    if not theater_name:
        return http_error(request, HTTPBadRequest)
    theater = query_utility(IMovieTheater, name=theater_name)
    if theater is None:
        return http_error(request, HTTPNotFound, "Unknown theater!")
    room_id = request.matchdict.get('room_id')
    if not room_id:
        return http_error(request, HTTPBadRequest)
    room = ICinemaRoomContainer(theater).get(room_id)
    if room is None:
        return http_error(request, HTTPNotFound, "Room not found!")
    return {
        'status': STATUS.SUCCESS.value,
        'room': {
            'id': room.__name__,
            'name': room.name,
            'capacity': room.capacity
        }
    }
