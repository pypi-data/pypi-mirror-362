#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
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

__docformat__ = 'restructuredtext'

from datetime import datetime

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Ge, Le
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config

from pyams_app_msc.feature.booking.zmi.interfaces import IBookingManagementMenu
from pyams_app_msc.feature.planning.interfaces import IPlanning, ISession
from pyams_app_msc.feature.planning.zmi import PlanningMenu, PlanningView
from pyams_app_msc.interfaces import VIEW_CATALOG_PERMISSION
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.room import ICinemaRoomContainer
from pyams_catalog.query import CatalogResultSet
from pyams_content_api.feature.json import IJSONExporter
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_utils.factory import get_interface_base_name
from pyams_utils.registry import get_utility
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer


@viewlet_config(name='planning.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IBookingManagementMenu, weight=7,
                permission=VIEW_CATALOG_PERMISSION)
class MovieTheaterPlanningMenu(PlanningMenu):
    """Movie theater planning menu"""


@pagelet_config(name='planning.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=VIEW_CATALOG_PERMISSION)
class MovieTheaterCalendarView(PlanningView):
    """Movie theater planning view"""

    def get_context(self):
        """View context getter"""
        return self.context


@view_config(name='get-planning-events.json',
             context=IMovieTheater, request_type=IPyAMSLayer,
             permission=USE_INTERNAL_API_PERMISSION,
             renderer='json')
def get_planning_events(request):
    """Planning events getter"""
    params = request.params
    room = params.get('room')
    start = params.get('start')
    end = params.get('end')
    if not (room and start and end):
        raise HTTPBadRequest()
    theater = IMovieTheater(request.context, None)
    if theater is None:
        raise HTTPNotFound()
    container = ICinemaRoomContainer(theater, None)
    if (container is None) or (room not in container):
        raise HTTPNotFound()
    catalog = get_utility(ICatalog)
    query = And(Eq(catalog['object_types'], get_interface_base_name(ISession)),
                Eq(catalog['planning_room'], room),
                Le(catalog['planning_start_date'], datetime.fromisoformat(end)),
                Ge(catalog['planning_end_date'], datetime.fromisoformat(start)))
    events = []
    for session in CatalogResultSet(CatalogQuery(catalog).query(query)):
        exporter = request.registry.queryMultiAdapter((session, request), IJSONExporter)
        if exporter is not None:
            events.append(exporter.to_json(with_edit_info=True, edit_context=IPlanning(session)))
    return events
