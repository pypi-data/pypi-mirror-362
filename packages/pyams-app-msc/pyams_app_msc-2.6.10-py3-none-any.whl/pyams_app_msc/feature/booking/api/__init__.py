# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from ZODB.POSException import POSKeyError
from ZODB.utils import p64
from cornice import Service
from cornice.validators import colander_validator
from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Any, Eq, Or
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound, HTTPOk, HTTPUnauthorized
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema.interfaces import ValidationError

from pyams_app_msc.feature.booking import BOOKING_STATUS, IBookingInfo
from pyams_app_msc.feature.booking.api.interfaces import MSC_BOOKING_API_ROUTE, MSC_BOOKING_SEARCH_API_ROUTE, \
    MSC_BOOKING_VALIDATION_API_ROUTE
from pyams_app_msc.feature.booking.api.schema import BookingInfoRequest, BookingSearchRequest, BookingSearchResponse, \
    BookingValidationGetterResponse, BookingValidationPostRequest, BookingValidationPostResponse, \
    BookingValidationRequest, FullBookingInfoResponse
from pyams_app_msc.feature.booking.message import get_booking_message
from pyams_app_msc.feature.messaging import IMessagingSettings
from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.feature.profile import IOperatorProfile
from pyams_app_msc.interfaces import MANAGE_BOOKING_PERMISSION, VIEW_BOOKING_PERMISSION
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_catalog.query import CatalogResultSet
from pyams_content.feature.history import IHistoryContainer
from pyams_content_api.feature.json import IJSONExporter
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_security.rest import check_cors_origin, set_cors_headers
from pyams_utils.factory import get_interface_base_name
from pyams_utils.registry import get_utility
from pyams_utils.rest import STATUS, http_error, rest_responses

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


booking_search_service = Service(name=MSC_BOOKING_SEARCH_API_ROUTE,
                                 pyramid_route=MSC_BOOKING_SEARCH_API_ROUTE,
                                 description="Booking search service")


@booking_search_service.options(validators=(check_cors_origin, set_cors_headers))
def booking_search_options(request):
    """Booking search service options"""
    return ''


booking_search_responses = rest_responses.copy()
booking_search_responses[HTTPOk.code] = BookingSearchResponse(description="Booking search response")


@booking_search_service.get(schema=BookingSearchRequest(),
                            validators=(check_cors_origin, colander_validator, set_cors_headers),
                            response_schemas=booking_search_responses)
def get_bookings(request):
    """Get bookings list"""
    if not request.has_permission(USE_INTERNAL_API_PERMISSION, context=request.context):
        return http_error(request, HTTPUnauthorized)
    registry = request.registry
    profile = IOperatorProfile(request)
    catalog = get_utility(ICatalog)
    intids = get_utility(IIntIds)
    principal_id = request.principal.id
    params = And(Eq(catalog['object_types'], get_interface_base_name(IMovieTheater)),
                 Or(Eq(catalog['role:msc:manager'], principal_id),
                    Eq(catalog['role:msc:operator'], principal_id),
                    Eq(catalog['role:msc:contributor'], principal_id),
                    Eq(catalog['role:msc:reader'], principal_id)))
    bookings = []
    theaters = list(CatalogResultSet(CatalogQuery(catalog).query(params)))
    if not theaters:
        translate = request.localizer.translate
        return {
            'status': STATUS.SUCCESS.value,
            'message': translate(_("You are not assigned to any theater")),
            'results': bookings
        }
    append_booking = bookings.append
    params = And(Eq(catalog['object_types'], get_interface_base_name(IBookingInfo)),
                 Any(catalog['parents'], [intids.queryId(theater) for theater in theaters]),
                 Any(catalog['booking_status'], {
                     BOOKING_STATUS.OPTION.value,
                     BOOKING_STATUS.WAITING.value
                 }))
    request_params = request.validated.get('querystring', {})
    for booking in sorted(filter(lambda x: not x.archived,
                                 CatalogResultSet(CatalogQuery(catalog).query(params))),
                          key=lambda x: ISession(x).start_date):
        exporter = registry.queryMultiAdapter((booking, request), IJSONExporter,
                                              name='msc_mobile_api')
        if exporter is not None:
            append_booking(exporter.to_json(**request_params))
    return {
        'status': STATUS.SUCCESS.value,
        'results': bookings
    }


booking_info_service = Service(name=MSC_BOOKING_API_ROUTE,
                               pyramid_route=MSC_BOOKING_API_ROUTE,
                               description="Booking info service")


@booking_info_service.options(validators=(check_cors_origin, set_cors_headers))
def booking_info_options(request):
    """Booking info service options"""
    return ''


booking_info_responses = rest_responses.copy()
booking_info_responses[HTTPOk.code] = FullBookingInfoResponse(description="Booking info response")


@booking_info_service.get(schema=BookingInfoRequest(),
                          validators=(check_cors_origin, colander_validator, set_cors_headers),
                          response_schemas=booking_info_responses)
def get_booking_info(request):
    """Booking information getter"""
    if not request.has_permission(USE_INTERNAL_API_PERMISSION, context=request.context):
        return http_error(request, HTTPUnauthorized)
    booking_id = request.matchdict['booking_id']
    if not booking_id:
        return http_error(request, HTTPBadRequest, "Missing booking ID")
    try:
        booking = request.context._p_jar.get(p64(int(booking_id, 16)))
    except ValueError:
        return http_error(request, HTTPBadRequest, "Bad session ID")
    except POSKeyError:
        return http_error(request, HTTPNotFound)
    if not IBookingInfo.providedBy(booking):
        return http_error(request, HTTPBadRequest, "Bad session ID")
    if not request.has_permission(VIEW_BOOKING_PERMISSION, context=booking):
        return {
            'status': STATUS.SUCCESS.value,
            'message': _("You are not allowed to access this booking"),
            'booking': None
        }
    request_params = request.validated.get('querystring', {})
    exporter = request.registry.queryMultiAdapter((booking, request), IJSONExporter,
                                                  name='msc_mobile_api')
    if exporter is not None:
        return {
            'status': STATUS.SUCCESS.value,
            'booking': exporter.to_json(**request_params)
        }
    return http_error(request, HTTPNotFound)


#
# Booking validation API
#

booking_validation_service = Service(name=MSC_BOOKING_VALIDATION_API_ROUTE,
                                     pyramid_route=MSC_BOOKING_VALIDATION_API_ROUTE,
                                     description="Booking validation service")


@booking_validation_service.options(validators=(check_cors_origin, set_cors_headers))
def booking_validation_options(request):
    """Booking validation service options"""
    return ''


booking_validation_getter_responses = rest_responses.copy()
booking_validation_getter_responses[HTTPOk.code] = BookingValidationGetterResponse(
        description="Booking validation response")


@booking_validation_service.get(schema=BookingValidationRequest(),
                                validators=(check_cors_origin, colander_validator, set_cors_headers),
                                response_schemas=booking_validation_getter_responses)
def get_booking_validation_info(request):
    """Booking validation information getter"""
    if not request.has_permission(USE_INTERNAL_API_PERMISSION, context=request.context):
        return http_error(request, HTTPUnauthorized)
    booking_id = request.matchdict['booking_id']
    if not booking_id:
        return http_error(request, HTTPBadRequest, "Missing booking ID")
    try:
        booking = request.context._p_jar.get(p64(int(booking_id, 16)))
    except ValueError:
        return http_error(request, HTTPBadRequest, "Bad session ID")
    except POSKeyError:
        return http_error(request, HTTPNotFound)
    if not IBookingInfo.providedBy(booking):
        return http_error(request, HTTPBadRequest, "Bad session ID")
    if not request.has_permission(MANAGE_BOOKING_PERMISSION, context=booking):
        return {
            'status': STATUS.SUCCESS.value,
            'message': _("You are not allowed to manage this booking"),
            'booking': None
        }
    request_params = request.validated.get('querystring', {})
    exporter = request.registry.queryMultiAdapter((booking, request), IJSONExporter,
                                                  name='msc_mobile_validation_api')
    if exporter is not None:
        return {
            'status': STATUS.SUCCESS.value,
            'booking': exporter.to_json(**request_params)
        }
    return http_error(request, HTTPNotFound)


booking_validation_post_responses = rest_responses.copy()
booking_validation_post_responses[HTTPOk.code] = BookingValidationPostResponse(
        description="Booking validation setter response")


@booking_validation_service.post(content_type='application/json',
                                 schema=BookingValidationPostRequest(),
                                 validators=(check_cors_origin, colander_validator, set_cors_headers),
                                 require_csrf=False,
                                 response_schemas=booking_validation_post_responses)
def post_booking_validation_info(request):
    """Booking validation request"""
    if not request.has_permission(USE_INTERNAL_API_PERMISSION, context=request.context):
        return http_error(request, HTTPUnauthorized)
    booking_id = request.matchdict['booking_id']
    if not booking_id:
        return http_error(request, HTTPBadRequest, "Missing booking ID")
    try:
        booking = request.context._p_jar.get(p64(int(booking_id, 16)))
    except ValueError:
        return http_error(request, HTTPBadRequest, "Bad session ID")
    except POSKeyError:
        return http_error(request, HTTPNotFound)
    if not IBookingInfo.providedBy(booking):
        return http_error(request, HTTPBadRequest, "Bad session ID")
    if not request.has_permission(MANAGE_BOOKING_PERMISSION, context=booking):
        return http_error(request, HTTPForbidden)
    history = IHistoryContainer(booking, None)
    params = request.validated.get('body', {})
    try:
        notify_message = None
        if params.get('notify_recipient'):
            notify_message = params.get('notify_message')
            if not notify_message:
                return http_error(request, HTTPBadRequest, "Missing field: notify_message")
        if history is not None:
            history.add_history(booking,
                                comment=params.get('notepad'),
                                message=notify_message,
                                request=request)
        booking.status = params['status']
        booking.accompanying_ratio = params['accompanying_ratio']
        booking.price = params['price']
        booking.notepad = params.get('notepad')
        if params.get('send_reminder'):
            booking.reminder_subject = params.get('reminder_subject')
            booking.reminder_message = params.get('reminder_message')
        if params.get('notify_recipient'):
            if params.get('include_quotation'):
                message = params.get('quotation_message')
                if message:
                    booking.quotation_message = message
            settings = IMessagingSettings(request.root, None)
            if settings is not None:
                mailer = settings.get_mailer()
                if mailer is not None:
                    subject = _("Booking accepted") if booking.status == BOOKING_STATUS.ACCEPTED.value \
                        else _("Booking temporarily accepted")
                    html_message = get_booking_message(subject, params, booking, request, settings)
                    if html_message is not None:
                        mailer.send(html_message)
        request.registry.notify(ObjectModifiedEvent(booking))
        return {
            'status': STATUS.SUCCESS.value
        }
    except ValidationError as exc:
        return http_error(request, HTTPBadRequest, f"Invalid value for field: {exc.field.__name__}")
    