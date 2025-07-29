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

"""PyAMS_app_msc.feature.booking.zmi.dashboard module

"""

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Any, Eq
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Attribute, Interface, implementer
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_app_msc.feature.booking.interfaces import BOOKING_STATUS, BOOKING_STATUS_LABEL, IBookingInfo
from pyams_app_msc.feature.booking.zmi.interfaces import IBookingAcceptedStatusTable, IBookingDashboardMenu, \
    IBookingManagementMenu, IBookingStatusTable, IBookingWaitingStatusTable
from pyams_app_msc.feature.profile.interfaces import IUserProfile
from pyams_app_msc.interfaces import VIEW_BOOKING_PERMISSION
from pyams_app_msc.shared.catalog.interfaces import ICatalogEntry
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.room import ROOMS_SEATS_VOCABULARY, ICinemaRoomContainer
from pyams_catalog.query import CatalogResultSet
from pyams_content.shared.common.zmi.dashboard import BaseDashboardTable, BaseSharedToolDashboardView
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.utility import get_principal
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.date import SH_DATETIME_FORMAT, format_datetime, get_timestamp
from pyams_utils.dict import DotDict
from pyams_utils.factory import factory_config, get_interface_base_name
from pyams_utils.interfaces import ICacheKeyValue, MISSING_INFO
from pyams_utils.list import unique_iter
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.manager import viewletmanager_config
from pyams_workflow.interfaces import IWorkflowVersions
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IInnerTable, ITableElementEditor, ITableWithActions
from pyams_zmi.interfaces.viewlet import IMenuHeader, INavigationViewletManager
from pyams_zmi.table import I18nColumnMixin, IconColumn, MultipleTablesAdminView, TableElementEditor
from pyams_zmi.utils import get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenu, NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewletmanager_config(name='booking-manager.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=50,
                       provides=IBookingManagementMenu)
class BookingManagementMenu(NavigationMenu):
    """Booking management menu"""

    _header = _("Booking management")


@adapter_config(required=(IMovieTheater, IAdminLayer, Interface, IBookingManagementMenu),
                provides=IMenuHeader)
def movie_theater_booking_manager_menu_header(context, request, view, menu):
    """Movie theater booking manager menu header"""
    return request.localizer.translate(_("Booking management"))


@viewletmanager_config(name='booking-dashboard.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=IBookingManagementMenu, weight=5,
                       provides=IBookingDashboardMenu,
                       permission=VIEW_BOOKING_PERMISSION)
class BookingDashboardMenu(NavigationMenuItem):
    """Movie theater booking dashboard menu"""

    label = _("Dashboard")
    icon_class = 'fas fa-chart-line'
    href = '#booking-dashboard.html'


@pagelet_config(name='booking-dashboard.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=VIEW_BOOKING_PERMISSION)
class BookingDashboardView(MultipleTablesAdminView):
    """Booking dashboard view"""

    header_label = _("Booking dashboard")
    table_label = _("Booking dashboard")


#
# Generic booking tables components
#

class IBookingElement(Interface):
    """Booking info interface"""
    booking = Attribute("Booking getter")
    session = Attribute("Session getter")
    entry = Attribute("Catalog entry getter")


@implementer(IBookingElement)
class BookingElement(DotDict):
    """Booking element class"""

    @property
    def __name__(self):
        return self.booking.__name__

    @property
    def __parent__(self):
        return self.booking.__parent__

    @property
    def __acl__(self):
        return self.booking.__acl__


def get_booking_element(booking):
    """Get booking element from booking input"""
    session = booking.session
    wf_entry = None
    entry = get_parent(session, ICatalogEntry)
    if entry is not None:
        wf_entry = IWorkflowVersions(entry).get_last_versions()[0]
    return BookingElement({
        'booking': booking,
        'session': session,
        'entry': wf_entry
    })


@adapter_config(required=IBookingElement,
                provides=ICacheKeyValue)
def booking_element_cache_key_value(context):
    """Booking element cache key value adapter"""
    return ICacheKeyValue(context.booking)


@adapter_config(required=IBookingElement,
                provides=IBookingInfo)
def booking_element_info(context):
    """Booking element info adapter"""
    return context.booking


@adapter_config(required=(IBookingElement, IAdminLayer, IBookingStatusTable),
                provides=ITableElementEditor)
class BookingElementEditor(TableElementEditor):
    """Booking element editor"""

    @property
    def href(self):
        return absolute_url(self.context.booking, self.request, 'properties.html')


@implementer(IBookingStatusTable, ITableWithActions)
class BookingStatusTable(BaseDashboardTable):
    """Movie theater booking status table"""

    @property
    def sort_index(self):
        return len(self.columns) - 3

    sort_order = 'asc'


@adapter_config(name='session',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusSessionColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status session column"""

    i18n_header = _("Session")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 10
    responsive_priority = 1

    def get_value(self, obj):
        if obj.entry is None:
            label = obj.session.label
            if label:
                label = f'({label})'
            else:
                label = self.request.localizer.translate(_("Out of catalog activity"))
            return label
        return get_object_label(obj.entry, self.request, self.table)


@adapter_config(name='room',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusRoomColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status room column"""

    i18n_header = _("Room")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 15

    def get_value(self, obj):
        room = ICinemaRoomContainer(self.context).get(obj.session.room)
        return get_object_label(room, self.request, self.table) if room is not None else MISSING_INFO


@adapter_config(name='date',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusDateColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status date column"""

    i18n_header = _("Date")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 20

    def get_value(self, obj):
        return format_datetime(obj.session.start_date, SH_DATETIME_FORMAT)


@adapter_config(name='creator',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusCreatorColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status creator column"""

    i18n_header = _("Creator")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 23

    def get_value(self, obj):
        return get_principal(self.request, obj.booking.creator).title


@adapter_config(name='recipient',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusRecipientColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status recipient column"""

    i18n_header = _("Recipient")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 25

    def get_value(self, obj):
        recipient = get_principal(self.request, obj.booking.recipient)
        result = recipient.title
        profile_info = IUserProfile(recipient, None)
        if (profile_info is None) or not profile_info.establishment:
            return result
        result = f'{result} ({profile_info.establishment})'
        if obj.booking.cultural_pass:
            label = self.request.localizer.translate(_("Cultural pass"))
            result += (f' <img title="{label}" alt="" '
                       f'      class="mx-1 mt-n1 hint" '
                       f'      src="/--static--/msc/img/pass-culture.webp" '
                       f'      width="24" height="24" />')
        return result


@adapter_config(name='seats',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusSeatsColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status seats column"""

    i18n_header = _("Seats")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 30

    def get_value(self, obj):
        return f'{obj.booking.nb_participants} + {obj.booking.nb_accompanists}'


@adapter_config(name='status',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusStatusColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status column"""

    i18n_header = _("Status")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 35

    def get_value(self, obj):
        translate = self.request.localizer.translate
        return translate(BOOKING_STATUS_LABEL.get(BOOKING_STATUS(obj.booking.status)))


@adapter_config(name='quotation',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusQuotationColumn(IconColumn):
    """Booking status quotation column"""

    icon_class = 'fas fa-file-pdf'
    hint = _("Quotation")
    weight = 40

    @staticmethod
    def checker(obj):
        return (obj.booking.status == BOOKING_STATUS.ACCEPTED.value) and obj.booking.quotation

    def render_cell(self, item):
        result = super().render_cell(item)
        if result:
            quotation = item.booking.quotation
            query = {'_': get_timestamp(quotation)}
            return f'<a href="{absolute_url(quotation, self.request, query=query)}" target="_blank">{result}</a>'
        return result


@adapter_config(name='timestamp',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusTimestampColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status timestamp column"""

    i18n_header = _("Last update")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 90

    def get_value(self, obj):
        booking_dc = IZopeDublinCore(obj.booking)
        return format_datetime(booking_dc.modified, SH_DATETIME_FORMAT)


@adapter_config(name='archived',
                required=(IMovieTheater, IAdminLayer, IBookingStatusTable),
                provides=IColumn)
class BookingStatusArchivedColumn(IconColumn):
    """Booking status archived column"""

    css_classes = {
        'th': 'action',
        'td': 'text-danger'
    }
    icon_class = 'fas fa-archive'
    hint = _("Archived")
    weight = 100

    @staticmethod
    def checker(obj):
        return obj.booking.archived


#
# Waiting bookings table
#

@factory_config(IBookingWaitingStatusTable)
class BookingWaitingStatusTable(BookingStatusTable):
    """Booking waiting status table"""

    prefix = 'waiting_table'


@adapter_config(required=(IMovieTheater, IAdminLayer, BookingWaitingStatusTable),
                provides=IValues)
class BookingWaitingStatusTableValues(ContextRequestViewAdapter):
    """Movie theater booking waiting status table values"""

    @property
    def values(self):
        """Table values getter"""
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, ROOMS_SEATS_VOCABULARY)
        params = And(Eq(catalog['object_types'], get_interface_base_name(IBookingInfo)),
                     Any(catalog['planning_room'], vocabulary.by_value.keys()),
                     Any(catalog['booking_status'],
                         {BOOKING_STATUS.OPTION.value, BOOKING_STATUS.WAITING.value}))
        yield from map(get_booking_element,
                       filter(lambda x: not x.archived,
                              unique_iter(CatalogResultSet(CatalogQuery(catalog).query(params)))))


@adapter_config(name='booking-waiting-status',
                required=(IMovieTheater, IAdminLayer, BookingDashboardView),
                provides=IInnerTable)
class BookingWaitingStatusView(BaseSharedToolDashboardView):
    """Movie theater booking waiting status view"""

    table_class = BookingWaitingStatusTable

    empty_label = _("MANAGER - No booking waiting for your action")
    single_label = _("MANAGER - 1 booking waiting for your action")
    plural_label = _("MANAGER - {} bookings waiting for your action")

    weight = 10


#
# Accepted bookings table
#

@factory_config(IBookingAcceptedStatusTable)
class BookingAcceptedStatusTable(BookingStatusTable):
    """Booking accepted status table"""

    prefix = 'accepted_table'


@adapter_config(required=(IMovieTheater, IAdminLayer, BookingAcceptedStatusTable),
                provides=IValues)
class BookingAcceptedStatusTableValues(ContextRequestViewAdapter):
    """Movie theater booking accepted status table values"""

    @property
    def values(self):
        """Table values getter"""
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, ROOMS_SEATS_VOCABULARY)
        params = And(Eq(catalog['object_types'], get_interface_base_name(IBookingInfo)),
                     Any(catalog['planning_room'], vocabulary.by_value.keys()),
                     Eq(catalog['booking_status'], BOOKING_STATUS.ACCEPTED.value))
        yield from map(get_booking_element,
                       filter(lambda x: not x.archived,
                              unique_iter(CatalogResultSet(CatalogQuery(catalog).query(params)))))


@adapter_config(name='booking-accepted-status',
                required=(IMovieTheater, IAdminLayer, BookingDashboardView),
                provides=IInnerTable)
class BookingAcceptedStatusView(BaseSharedToolDashboardView):
    """Movie theater booking accepted status view"""

    table_class = BookingAcceptedStatusTable

    empty_label = _("MANAGER - No booking accepted")
    single_label = _("MANAGER - 1 booking accepted")
    plural_label = _("MANAGER - {} bookings accepted")

    weight = 20
