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

from pyams_app_msc.shared.theater import IMovieTheater
from pyams_app_msc.shared.theater.api.interfaces import MSC_PRICE_API_ROUTE
from pyams_app_msc.shared.theater.api.schema import PriceGetterRequest, PriceGetterResponse
from pyams_app_msc.shared.theater.interfaces.price import ICinemaPriceContainer
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_security.rest import check_cors_origin, set_cors_headers
from pyams_utils.registry import query_utility
from pyams_utils.rest import STATUS, http_error, rest_responses


price_service = Service(name=MSC_PRICE_API_ROUTE,
                        pyramid_route=MSC_PRICE_API_ROUTE,
                        description="Price getter service")


@price_service.options(validators=(check_cors_origin, set_cors_headers))
def price_options(request):
    """Price service options"""
    return ''


price_get_responses = rest_responses.copy()
price_get_responses[HTTPOk.code] = PriceGetterResponse(
    description="Price getter result")


@price_service.get(permission=USE_INTERNAL_API_PERMISSION,
                   schema=PriceGetterRequest(),
                   validators=(check_cors_origin, colander_validator, set_cors_headers),
                   response_schemas=price_get_responses)
def get_price(request):
    """Get price information"""
    theater_name = request.matchdict.get('theater_name')
    if not theater_name:
        return http_error(request, HTTPBadRequest)
    theater = query_utility(IMovieTheater, name=theater_name)
    if theater is None:
        return http_error(request, HTTPNotFound, "Unknown theater!")
    price_id = request.params.get('price_id')
    if not price_id:
        return http_error(request, HTTPBadRequest)
    price = ICinemaPriceContainer(theater).get(price_id)
    if price is None:
        return http_error(request, HTTPNotFound, "Price not found!")
    return {
        'status': STATUS.SUCCESS.value,
        'price': {
            'id': price.__name__,
            'active': price.active,
            'name': price.name,
            'participant_price': price.participant_price,
            'accompanying_price': price.accompanying_price,
            'accompanying_ratio': price.accompanying_ratio,
            'comment': price.comment
        }
    }
