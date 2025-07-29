# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from datetime import date, datetime, timedelta, timezone

from ZODB.POSException import POSKeyError
from ZODB.utils import p64
from cornice import Service
from cornice.validators import colander_validator
from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Any, Eq, Ge, Lt, Or
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPOk, HTTPUnauthorized
from zope.intid.interfaces import IIntIds

from pyams_app_msc.feature.planning.api.interfaces import MSC_PLANNING_API_ROUTE, MSC_SESSION_API_ROUTE
from pyams_app_msc.feature.planning.api.schema import PlanningGetterResponse, SessionGetterResponse
from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.feature.profile.interfaces import IOperatorProfile
from pyams_app_msc.interfaces import VIEW_PLANNING_PERMISSION
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_catalog.query import CatalogResultSet
from pyams_content_api.feature.json.interfaces import IJSONExporter
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_security.rest import check_cors_origin, set_cors_headers
from pyams_utils.factory import get_interface_base_name
from pyams_utils.registry import get_utility
from pyams_utils.rest import STATUS, http_error, rest_responses
from pyams_utils.timezone import tztime

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


planning_service = Service(name=MSC_PLANNING_API_ROUTE,
                           pyramid_route=MSC_PLANNING_API_ROUTE,
                           description="Planning getter service")


@planning_service.options(validators=(check_cors_origin, set_cors_headers))
def planning_options(request):
    """Planning service options"""
    return ''


planning_get_responses = rest_responses.copy()
planning_get_responses[HTTPOk.code] = PlanningGetterResponse(description="Planning getter response")


@planning_service.get(validators=(check_cors_origin, colander_validator, set_cors_headers),
                      response_schemas=planning_get_responses)
def get_planning(request):
    """Get planning information"""
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
    sessions = []
    theaters = list(CatalogResultSet(CatalogQuery(catalog).query(params)))
    if not theaters:
        translate = request.localizer.translate
        return {
            'status': STATUS.SUCCESS.value,
            'message': translate(_("You are not assigned to any theater")),
            'results': sessions
        }
    append_session = sessions.append
    now = tztime(datetime.now(timezone.utc))
    today_start = tztime(datetime.combine(date.today(), datetime.min.time()))
    today_end = today_start + timedelta(days=profile.today_program_length)
    params = And(Eq(catalog['object_types'], get_interface_base_name(ISession)),
                 Any(catalog['parents'], [intids.register(theater) for theater in theaters]),
                 Lt(catalog['planning_start_date'], today_end),
                 Ge(catalog['planning_end_date'], now))
    for session in CatalogResultSet(CatalogQuery(catalog).query(params,
                                                                sort_index='planning_start_date')):
        exporter = registry.queryMultiAdapter((session, request), IJSONExporter,
                                              name='msc_mobile_api')
        if exporter is not None:
            append_session(exporter.to_json())
    return {
        'status': STATUS.SUCCESS.value,
        'results': sessions
    }
    
    
session_service = Service(name=MSC_SESSION_API_ROUTE,
                          pyramid_route=MSC_SESSION_API_ROUTE,
                          description="Session getter service")


@session_service.options(validators=(check_cors_origin, set_cors_headers))
def session_options(request):
    """Session service options"""
    return ''


session_get_responses = rest_responses.copy()
session_get_responses[HTTPOk.code] = SessionGetterResponse(description="Session getter response")


@session_service.get(permission=USE_INTERNAL_API_PERMISSION,
                     validators=(check_cors_origin, colander_validator, set_cors_headers),
                     response_schemas=session_get_responses)
def get_session(request):
    """Get session information"""
    if not request.has_permission(USE_INTERNAL_API_PERMISSION, context=request.context):
        return http_error(request, HTTPUnauthorized)
    session_id = request.matchdict['session_id']
    if not session_id:
        return http_error(request, HTTPBadRequest, "Missing session ID")
    try:
        session = request.context._p_jar.get(p64(int(session_id, 16)))
    except POSKeyError:
        return http_error(request, HTTPNotFound)
    if not ISession.providedBy(session):
        return http_error(request, HTTPBadRequest, "Bad session ID")
    if not request.has_permission(VIEW_PLANNING_PERMISSION, context=session):
        return {
            'status': STATUS.SUCCESS.value,
            'message': _("You are not allowed to access this session"),
            'session': None
        }
    exporter = request.registry.queryMultiAdapter((session, request), IJSONExporter,
                                                  name='msc_mobile_session_api')
    if exporter is not None:
        return {
            'status': STATUS.SUCCESS.value,
            'session': exporter.to_json()
    }
    return http_error(request, HTTPNotFound)
