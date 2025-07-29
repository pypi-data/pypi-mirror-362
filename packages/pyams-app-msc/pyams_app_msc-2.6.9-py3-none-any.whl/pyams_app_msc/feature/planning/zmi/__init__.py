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

import json
from datetime import datetime, timezone

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Ge, Le
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config
from zope.interface import implementer

from pyams_app_msc.feature.booking import IBookingContainer
from pyams_app_msc.feature.planning import IPlanning, IPlanningTarget, IWfPlanningTarget
from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.feature.planning.zmi.interfaces import IActivityArchivedSessionsTable, IActivityCurrentSessionsTable, \
    IActivitySessionsTable, IPlanningMenu
from pyams_app_msc.interfaces import MANAGE_PLANNING_PERMISSION, VIEW_BOOKING_PERMISSION, \
    VIEW_PLANNING_PERMISSION
from pyams_app_msc.shared.theater import IMovieTheaterSettings
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.room import ICinemaRoomContainer
from pyams_catalog.query import CatalogResultSet
from pyams_content_api.feature.json.interfaces import IJSONExporter
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_skin.viewlet.actions import ContextAction, JsContextAction
from pyams_table.column import GetAttrColumn, GetAttrFormatterColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config, get_interface_base_name
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import ViewContentProvider, viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IColumnSortData, IInnerTable, ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, ISecondaryActionsViewletManager, IViewWithoutToolbar
from pyams_zmi.table import I18nColumnMixin, IconColumn, InnerTableAdminView, MultipleTablesAdminView, \
    Table, TableElementEditor, get_table_id
from pyams_zmi.view import InnerAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewletmanager_config(name='planning.menu',
                       context=IWfPlanningTarget, layer=IAdminLayer,
                       manager=IContentManagementMenu, weight=20,
                       provides=IPlanningMenu,
                       permission=VIEW_PLANNING_PERMISSION)
class PlanningMenu(NavigationMenuItem):
    """Planning menu"""

    label = _("Planning")
    icon_class = 'fas fa-calendar-week'
    href = '#planning.html'


@pagelet_config(name='planning.html',
                context=IWfPlanningTarget, layer=IPyAMSLayer,
                permission=VIEW_PLANNING_PERMISSION)
@template_config(template='templates/planning.pt',
                 layer=IPyAMSLayer)
class PlanningView(InnerAdminView):
    """Planning view"""

    title = _("Sessions planning")

    @reify
    def theater(self):
        """Theater getter"""
        return get_parent(self.context, IMovieTheater)

    @property
    def rooms(self):
        """Theater rooms iterator getter"""
        theater = self.theater
        if theater is not None:
            yield from ICinemaRoomContainer(theater).get_active_items()

    def get_context(self):
        """View context getter"""
        return IPlanning(self.context)

    @property
    def can_view_bookings(self):
        """Bookings access checker"""
        return bool(self.request.has_permission(VIEW_BOOKING_PERMISSION, context=self.context))

    @property
    def can_edit_planning(self):
        """Calendar editor checker"""
        return bool(self.request.has_permission(MANAGE_PLANNING_PERMISSION, context=self.context))

    def get_calendar_options(self, room):
        """Calendar options getter"""
        context = self.get_context()
        request = self.request
        settings = IMovieTheaterSettings(self.theater)
        can_edit = request.has_permission(MANAGE_PLANNING_PERMISSION, context=context)
        translate = request.localizer.translate
        options = {
            'editable': can_edit,
            'droppable': can_edit,
            'eventSources': [{
                'url': absolute_url(context, request, 'get-planning-events.json'),
                'extraParams': {
                    'room': room.__name__
                }
            }],
            'height': '100%',
            'firstDay': settings.calendar_first_day,
            'dateClick': 'MyAMS.msc.calendar.addEvent',
            'initialView': 'timeGridWeek',
            'headerToolbar': {
                'center': 'today',
                'right': 'prev,next dayGridMonth,timeGridWeek,timeGridDay,listMonth'
            },
            'allDaySlot': False,
            'slotDuration': f'00:{settings.calendar_slot_duration:#02}:00',
            'slotMinTime': room.start_time.isoformat(),
            'slotMaxTime': room.end_time.isoformat(),
            'buttonText': {
                'today': translate(_("Today")),
                'month': translate(_("Month")),
                'week': translate(_("Week")),
                'day': translate(_("Day")),
                'list': translate(_("List")),
                'all-day': translate(_("All-day")),
                'prev': " « ",
                'next': " » "
            }
        }
        return json.dumps(options)


@view_config(name='get-planning-events.json',
             context=IPlanning, request_type=IPyAMSLayer,
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
    theater = get_parent(request.context, IMovieTheater)
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
            events.append(exporter.to_json(with_edit_info=True, edit_context=request.context))
    return events


@viewlet_config(name='planning.transpose',
                layer=IAdminLayer, view=PlanningView,
                manager=ISecondaryActionsViewletManager, weight=10)
class PlanningTransposeAction(JsContextAction):
    """Planning transpose action"""

    icon_class = 'fas fa-recycle'
    hint = _("Transpose calendars")
    hint_placement = 'bottom'

    href = 'MyAMS.msc.calendar.transpose'


@viewlet_config(name='planning.synchronize',
                layer=IAdminLayer, view=PlanningView,
                manager=ISecondaryActionsViewletManager, weight=20)
class PlanningSynchronizeAction(JsContextAction):
    """Planning synchronize action"""

    icon_class = 'fas fa-sync-alt'
    hint = _("Synchronize calendars views")
    hint_placement = 'bottom'

    href = 'MyAMS.msc.calendar.synchronize'


@viewlet_config(name='planning.scroll',
                layer=IAdminLayer, view=PlanningView,
                manager=ISecondaryActionsViewletManager, weight=30)
class PlanningScrollAction(JsContextAction):
    """Planning scrolling action"""

    icon_class = 'fas fa-arrows-alt-v'
    hint = _("Synchronize calendars scrolling")
    hint_placement = 'bottom'

    href = 'MyAMS.msc.calendar.scroll'


@viewlet_config(name='planning-legend.action',
                layer=IAdminLayer, view=PlanningView,
                manager=ISecondaryActionsViewletManager, weight=40)
@template_config(template='templates/planning-legend.pt',
                 layer=IAdminLayer)
class PlanningLegendAction(ContextAction):
    """Planning legend action"""
    
    icon_class = 'fas fa-question-circle text-info'
    hint = _("Planning legend")
    hint_placement = 'top'


#
# Sessions view
#

@viewlet_config(name='activity-sessions.menu',
                context=IWfPlanningTarget, layer=IAdminLayer,
                manager=IPlanningMenu, weight=10,
                permission=VIEW_PLANNING_PERMISSION)
class ActivitySessionsMenu(NavigationMenuItem):
    """Activity sessions menu"""

    label = _("Planned sessions")
    href = '#activity-sessions.html'


@pagelet_config(name='activity-sessions.html',
                context=IWfPlanningTarget, layer=IPyAMSLayer,
                permission=VIEW_PLANNING_PERMISSION)
class ActivitySessionsView(MultipleTablesAdminView):
    """Activity sessions view"""

    table_label = _("Activity planned sessions")


class ActivitySessionsBaseTableView(InnerTableAdminView, ViewContentProvider):
    """Activity base sessions view"""
    
    hide_section = True

    
@implementer(IViewWithoutToolbar, IObjectData)
class ActivitySessionsBaseTable(Table):
    """Activity base sessions table"""

    sort_index = 1

    @reify
    def id(self):  # pylint: disable=invalid-name
        """Table ID getter"""
        planning = IPlanning(self.context)
        return get_table_id(self, planning)

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        attributes.setdefault('table', {}).update({
            'data-ams-order': f'{self.sort_index},{self.sort_order}'
        })
        return attributes

    object_data = {
        'buttons': ['copy', 'csv', 'excel', 'print'],
        'ams-buttons-classname': 'btn btn-sm btn-secondary'
    }

    @property
    def css_classes(self):
        classes = super().css_classes.copy()
        classes['tr.selected'] = self.get_tr_class
        return classes

    def get_tr_class(self, item, column, index):
        now = tztime(datetime.now(timezone.utc))
        if item.start_date < now:
            return 'bg-warning'
        return None


@adapter_config(name='current-sessions',
                required=(IWfPlanningTarget, IAdminLayer, ActivitySessionsView),
                provides=IInnerTable)
class ActivityCurrentSessionsTableView(ActivitySessionsBaseTableView):
    """Activity current sessions view"""

    weight = 10

    table_class = IActivityCurrentSessionsTable
    table_label = _("Incoming sessions")


@factory_config(IActivityCurrentSessionsTable)
class ActivityCurrentSessionsTable(ActivitySessionsBaseTable):
    """Activity current sessions table"""

    prefix = 'current_sessions_table'
    sort_order = 'asc'


@adapter_config(required=(IPlanningTarget, IAdminLayer, IActivityCurrentSessionsTable),
                provides=IValues)
@adapter_config(required=(IWfPlanningTarget, IAdminLayer, IActivityCurrentSessionsTable),
                provides=IValues)
class ActivityCurrentSessionsTableValues(ContextRequestViewAdapter):
    """Activity current sessions table values adapter"""

    @property
    def values(self):
        now = tztime(datetime.now(timezone.utc))
        yield from (
            session
            for session in IPlanning(self.context).values()
            if session.start_date >= now
        )


@adapter_config(name='archived-sessions',
                required=(IWfPlanningTarget, IAdminLayer, ActivitySessionsView),
                provides=IInnerTable)
class ActivityArchivedSessionsTableView(ActivitySessionsBaseTableView):
    """Activity archived sessions view"""

    weight = 20

    table_class = IActivityArchivedSessionsTable
    table_label = _("Archived sessions")


@factory_config(IActivityArchivedSessionsTable)
class ActivityArchivedSessionsTable(ActivitySessionsBaseTable):
    """Activity archived sessions table"""

    prefix = 'archived_sessions_table'
    sort_order = 'desc'

    
@adapter_config(required=(IPlanningTarget, IAdminLayer, IActivityArchivedSessionsTable),
                provides=IValues)
@adapter_config(required=(IWfPlanningTarget, IAdminLayer, IActivityArchivedSessionsTable),
                provides=IValues)
class ActivityArchivedSessionsTableValues(ContextRequestViewAdapter):
    """Activity archived sessions table values adapter"""

    @property
    def values(self):
        now = tztime(datetime.now(timezone.utc))
        yield from (
            session
            for session in IPlanning(self.context).values()
            if session.start_date < now
        )


@adapter_config(name='archived',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
class ActivitySessionsTableArchivedColumn(IconColumn):
    """Activity sessions table archived column"""
    
    css_classes = {
        'th': 'action',
        'td': 'text-danger'
    }
    icon_class = 'fas fa-archive'
    hint = _("Archived")

    weight = 5

    def checker(self, item):
        now = tztime(datetime.now(timezone.utc))
        return item.start_date < now


@adapter_config(name='start_date',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
@implementer(IColumnSortData)
class ActivitySessionsTableStartDateColumn(I18nColumnMixin, GetAttrFormatterColumn):
    """Activity sessions table start date column"""

    i18n_header = _("Start date")
    attr_name = 'start_date'
    
    @property
    def format_string(self):
        translate = self.request.localizer.translate
        return translate(_("%a %d/%m/%Y at %H:%M"))

    weight = 10
    
    @staticmethod
    def get_sort_value(value):
        return value.start_date.isoformat()


@adapter_config(name='room',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
class ActivitySessionsTableRoomColumn(I18nColumnMixin, GetAttrColumn):
    """Activity sessions table room column"""

    i18n_header = _("Room")
    attr_name = 'room'

    weight = 20

    def get_value(self, obj):
        room = obj.get_room()
        return room.name if room is not None else MISSING_INFO


@adapter_config(name='capacity',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
class ActivitySessionsTableCapacityColumn(I18nColumnMixin, GetAttrColumn):
    """Activity sessions table capacity column"""

    i18n_header = _("Session capacity")
    attr_name = 'capacity'

    weight = 30


@adapter_config(name='bookings',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
class ActivitySessionsTableBookingsColumn(I18nColumnMixin, GetAttrColumn):
    """Activity sessions table bookings column"""

    i18n_header = _("Reserved")
    attr_name = 'bookings'

    weight = 40

    def get_value(self, obj):
        return IBookingContainer(obj).get_requested_seats()


@adapter_config(name='free_seats',
                required=(IWfPlanningTarget, IAdminLayer, IActivityCurrentSessionsTable),
                provides=IColumn)
class ActivitySessionsTableFreeSeatsColumn(I18nColumnMixin, GetAttrColumn):
    """Activity sessions table free seats column"""

    i18n_header = _("Free seats")
    attr_name = 'free_seats'

    weight = 50

    def get_value(self, obj):
        return IBookingContainer(obj).free_seats


@adapter_config(name='confirmed',
                required=(IWfPlanningTarget, IAdminLayer, IActivityArchivedSessionsTable),
                provides=IColumn)
class ActivitySessionsTableConfirmedColumn(I18nColumnMixin, GetAttrColumn):
    """Activity sessions table confirmed column"""

    i18n_header = _("Confirmed")
    attr_name = 'confirmed'

    weight = 50

    def get_value(self, obj):
        return IBookingContainer(obj).get_confirmed_seats()


@adapter_config(name='temporary',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
class ActivitySessionsTableWaitingColumn(IconColumn):
    """Activity sessions table waiting column"""

    icon_class = 'fas fa-hourglass'
    hint = _("Temporary session")

    weight = 60

    def checker(self, item):
        return item.temporary


@adapter_config(name='bookable',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
class ActivitySessionsTableBookableColumn(IconColumn):
    """Activity sessions table bookable column"""

    icon_class = 'far fa-calendar'
    hint = _("Open for internal booking")

    weight = 70

    def checker(self, item):
        return item.bookable


@adapter_config(name='extern-bookable',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
class ActivitySessionsTableExternBookableColumn(IconColumn):
    """Activity sessions table external bookable column"""

    icon_class = 'far fa-calendar-alt'
    hint = _("Open for external booking")

    weight = 80

    def checker(self, item):
        return item.extern_bookable


@adapter_config(name='public',
                required=(IWfPlanningTarget, IAdminLayer, IActivitySessionsTable),
                provides=IColumn)
class ActivitySessionsTablePublicColumn(IconColumn):
    """Activity sessions table public column"""

    icon_class = 'fas fa-users'
    hint = _("Public session")

    weight = 90

    def checker(self, item):
        return item.public_session


@adapter_config(required=(ISession, IAdminLayer, IActivitySessionsTable),
                provides=ITableElementEditor)
class SessionTableElementEditor(TableElementEditor):
    """Session table element editor"""
