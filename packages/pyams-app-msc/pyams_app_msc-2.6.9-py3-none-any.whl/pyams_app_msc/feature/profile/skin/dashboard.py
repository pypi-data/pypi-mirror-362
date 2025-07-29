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

from datetime import datetime, timedelta, timezone

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq
from pyramid.decorator import reify
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import implementer

from pyams_app_msc.feature.booking.interfaces import BOOKING_STATUS, BOOKING_STATUS_LABEL, IBookingInfo
from pyams_app_msc.feature.booking.zmi import get_booking_element
from pyams_app_msc.feature.booking.zmi.dashboard import BookingStatusQuotationColumn, BookingStatusSeatsColumn
from pyams_app_msc.feature.navigation.interfaces import INavigationViewletManager
from pyams_app_msc.feature.profile.skin import ProfileContextIndexPage, UserMenu
from pyams_app_msc.feature.profile.skin.interfaces import IUserDashboardTable, IUserProfileView
from pyams_app_msc.shared.theater.interfaces import BOOKING_CANCEL_MODE, IMovieTheater, IMovieTheaterSettings
from pyams_app_msc.skin import IPyAMSMSCLayer
from pyams_catalog.query import CatalogResultSet
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_site.interfaces import ISiteRoot
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.date import SH_DATETIME_FORMAT, format_datetime
from pyams_utils.factory import get_interface_base_name
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.list import unique_iter
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.table import I18nColumnMixin, Table
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@implementer(IUserDashboardTable)
class BaseUserDashboardTable(Table):
    """Base user dashboard table"""

    object_data = {
        'responsive': True,
        'auto-width': False,
        'paging': False,
        'info': False,
        'row-group': {
            'dataSrc': 0
        },
        'column-defs': [{
            'targets': 0,
            'visible': False
        }],
        'order-fixed': [0, 'asc']
    }


#
# User dashboard
#

@viewlet_config(name='user-dashboard.menu',
                layer=IPyAMSMSCLayer, view=IUserProfileView,
                manager=INavigationViewletManager, weight=30)
class UserDashboardMenu(UserMenu):
    """User dashboard menu"""

    label = _("My bookings")
    href = 'my-dashboard.html'


class UserDashboardTable(BaseUserDashboardTable):
    """User dashboard table"""

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        attributes.setdefault('table', {}).update({
            'data-ams-order': '2,asc'
        })
        return attributes


@pagelet_config(name='my-dashboard.html',
                context=ISiteRoot, layer=IPyAMSLayer)
@implementer(IUserProfileView)
class UserDashboardView(ProfileContextIndexPage):
    """User dashboard view"""

    table = None

    def update(self):
        super().update()
        self.table = UserDashboardTable(self.context, self.request)
        self.table.update()

    def render(self):
        return self.table.render()


@adapter_config(required=(ISiteRoot, IPyAMSMSCLayer, UserDashboardTable),
                provides=IValues)
class UserDashboardTableValues(ContextRequestViewAdapter):
    """User dashboard table values"""

    @property
    def values(self):
        catalog = get_utility(ICatalog)
        params = And(Eq(catalog['object_types'], get_interface_base_name(IBookingInfo)),
                     Eq(catalog['booking_recipient'], self.request.principal.id))
        yield from map(get_booking_element,
                       filter(lambda x: not x.archived,
                              unique_iter(CatalogResultSet(CatalogQuery(catalog).query(params)))))


#
# User archives dashboard
#

@viewlet_config(name='user-archives.menu',
                layer=IPyAMSMSCLayer, view=IUserProfileView,
                manager=INavigationViewletManager, weight=40)
class UserArchivesMenu(UserMenu):
    """User archives dashboard menu"""

    label = _("My archives")
    href = 'my-archives.html'


class UserArchivesTable(BaseUserDashboardTable):
    """User archives table"""

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        attributes.setdefault('table', {}).update({
            'data-ams-order': '2,desc'
        })
        return attributes


@pagelet_config(name='my-archives.html',
                context=ISiteRoot, layer=IPyAMSLayer)
@implementer(IUserProfileView)
class UserArchivesView(ProfileContextIndexPage):
    """User archives view"""

    table = None

    def update(self):
        super().update()
        self.table = UserArchivesTable(self.context, self.request)
        self.table.update()

    def render(self):
        return self.table.render()


@adapter_config(required=(ISiteRoot, IPyAMSMSCLayer, UserArchivesTable),
                provides=IValues)
class UserArchivesTableValues(ContextRequestViewAdapter):
    """User archives table values"""

    @property
    def values(self):
        catalog = get_utility(ICatalog)
        params = And(Eq(catalog['object_types'], get_interface_base_name(IBookingInfo)),
                     Eq(catalog['booking_recipient'], self.request.principal.id))
        yield from map(get_booking_element,
                       filter(lambda x: x.archived,
                              unique_iter(CatalogResultSet(CatalogQuery(catalog).query(params)))))


#
# Dashboard columns
#

@adapter_config(name='theater',
                required=(ISiteRoot, IPyAMSMSCLayer, IUserDashboardTable),
                provides=IColumn)
class UserDashboardTheaterColumn(I18nColumnMixin, GetAttrColumn):
    """User dashboard theater column"""

    i18n_header = _("Theater")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 5

    def get_value(self, obj):
        theater = get_parent(obj.booking, IMovieTheater)
        return get_object_label(theater, self.request)


@adapter_config(name='session-label',
                required=(ISiteRoot, IPyAMSMSCLayer, IUserDashboardTable),
                provides=IColumn)
class UserDashboardSessionLabelColumn(I18nColumnMixin, GetAttrColumn):
    """User dashboard session label column"""

    i18n_header = _("Session")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 10
    responsive_priority = 1

    def get_value(self, obj):
        if obj.entry is None:
            label = obj.session.label
            if not label:
                label = self.request.localizer.translate(_("Out of catalog activity"))
            return label
        return get_object_label(obj.entry, self.request, self.table)


@adapter_config(name='session-date',
                required=(ISiteRoot, IPyAMSMSCLayer, IUserDashboardTable),
                provides=IColumn)
class UserDashboardSessionDateColumn(I18nColumnMixin, GetAttrColumn):
    """User dashboard session date column"""

    i18n_header = _("Date")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 20

    def get_value(self, obj):
        session = obj.session
        return format_datetime(session.start_date, format_string=SH_DATETIME_FORMAT)


@adapter_config(name='status',
                required=(ISiteRoot, IPyAMSMSCLayer, IUserDashboardTable),
                provides=IColumn)
class UserDashboardStatusColumn(I18nColumnMixin, GetAttrColumn):
    """USer dashboard status column"""

    i18n_header = _("Status")
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 30

    def get_value(self, obj):
        status = obj.booking.status
        try:
            label = BOOKING_STATUS_LABEL.get(BOOKING_STATUS(status))
        except ValueError:
            label = _("(unknown status)")
        return self.request.localizer.translate(label)


@adapter_config(name='seats',
                required=(ISiteRoot, IPyAMSMSCLayer, IUserDashboardTable),
                provides=IColumn)
class UserDashboardSeatsColumn(BookingStatusSeatsColumn):
    """User dashboard seats column"""

    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 35


@adapter_config(name='quotation',
                required=(ISiteRoot, IPyAMSMSCLayer, IUserDashboardTable),
                provides=IColumn)
class UserDashboardQuotationColumn(BookingStatusQuotationColumn):
    """User dashboard quotation column"""


@adapter_config(name='cancel',
                required=(ISiteRoot, IPyAMSMSCLayer, UserDashboardTable),
                provides=IColumn)
class UserDashboardCancelColumn(GetAttrColumn):
    """User dashboard cancel column"""

    css_classes = {
        'td': 'text-nowrap'
    }
    sortable = 'false'
    weight = 50
    # responsive_priority = 100

    def get_value(self, obj):
        booking = obj.booking
        if booking.status == BOOKING_STATUS.CANCELLED.value:
            return ''
        session = obj.session
        theater = get_parent(session, IMovieTheater)
        settings = IMovieTheaterSettings(theater)
        if settings.booking_cancel_mode == BOOKING_CANCEL_MODE.FORBIDDEN.value:
            return ''
        if settings.booking_cancel_mode == BOOKING_CANCEL_MODE.MAX_DELAY.value:
            dc = IZopeDublinCore(booking)
            last_date = tztime(dc.created) + timedelta(hours=settings.booking_cancel_max_delay)
            if tztime(datetime.now(timezone.utc)) > last_date:
                return ''
        elif settings.booking_cancel_mode == BOOKING_CANCEL_MODE.NOTICE_PERIOD.value:
            last_date = tztime(session.start_date) - timedelta(hours=settings.booking_cancel_notice_period)
            if tztime(datetime.now(timezone.utc)) > last_date:
                return ''
        label = self.request.localizer.translate(_("Cancel..."))
        return f'''<a class="btn btn-sm btn-primary py-0" ''' + \
               f'''   href="{absolute_url(self.context, self.request, 
                                          'cancel-booking.html', 
                                          {'booking_id': ICacheKeyValue(booking)})}">{label}</a>'''
