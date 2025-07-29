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

from collections import OrderedDict
from datetime import date, datetime, timedelta, timezone

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Ge, Lt
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds

from pyams_app_msc.feature.booking import IBookingContainer
from pyams_app_msc.feature.booking.interfaces import BOOKING_STATUS
from pyams_app_msc.feature.planning.interfaces import ISession, VERSION_INFO, VERSION_INFO_ABBR
from pyams_app_msc.feature.profile import IOperatorProfile
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_catalog.query import CatalogResultSet
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.viewlet.menu import DropdownMenu, MenuItem
from pyams_template.template import template_config
from pyams_utils.date import format_date, format_datetime, format_time
from pyams_utils.factory import get_interface_base_name
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import INavigationViewletManager, IToolbarViewletManager
from pyams_zmi.view import InnerAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='today-program.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=INavigationViewletManager, weight=10,
                permission=VIEW_SYSTEM_PERMISSION)
class TodayProgramMenu(NavigationMenuItem):
    """Today program menu"""

    label = _("Today program")
    icon_class = 'fas fa-tasks'
    href = '#today-program.html'


@pagelet_config(name='today-program.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
@template_config(template='templates/today-program.pt',
                 layer=IAdminLayer)
class TodayProgramView(InnerAdminView):
    """Today program view"""

    @property
    def title(self):
        profile = IOperatorProfile(self.request)
        if profile.today_program_length == 1:
           return _("Sessions planned for today")
        translate = self.request.localizer.translate
        return translate(_("Sessions planned for the next {count} days")).format(
            count=profile.today_program_length)

    def get_sessions(self):
        """Today sessions getter"""
        profile = IOperatorProfile(self.request)
        now = tztime(datetime.now(timezone.utc))
        today_start = tztime(datetime.combine(date.today(), datetime.min.time()))
        today_end = today_start + timedelta(days=profile.today_program_length)
        catalog = get_utility(ICatalog)
        intids = get_utility(IIntIds)
        params = And(Eq(catalog['object_types'], get_interface_base_name(ISession)),
                     Eq(catalog['parents'], intids.register(self.context)),
                     Lt(catalog['planning_start_date'], today_end),
                     Ge(catalog['planning_end_date'], now))
        sessions = OrderedDict()
        for session in CatalogResultSet(CatalogQuery(catalog).query(params,
                                                            sort_index='planning_start_date')):
            sessions.setdefault(session.start_date.date(), []).append(session)
        yield from sessions.items()

    @staticmethod
    def get_bookings(session):
        """Session bookings getter"""
        yield from filter(lambda x: x.status == BOOKING_STATUS.ACCEPTED.value,
                          IBookingContainer(session).values())

    def get_groups(self, booking):
        """Booking groups getter"""
        translate = self.request.localizer.translate
        if booking.nb_groups > 1:
            return translate(_("{} groups")).format(booking.nb_groups)
        return translate(_("1 group"))

    def format_date(self, session_date):
        """Session date formatter"""
        request = self.request
        translate = request.localizer.translate
        today = date.today()
        if session_date == today:
            return translate(_("Today"))
        return format_date(session_date,
                           format_string=translate(_("on %A %d, %B")),
                           request=request)

    def format_time(self, session_date):
        """Session time formatter"""
        request = self.request
        translate = request.localizer.translate
        return format_time(session_date,
                           format_string=translate(_("at %H:%M")),
                           request=request)

    def get_version(self, session):
        """Session version getter"""
        if not session.version:
            return None
        translate = self.request.localizer.translate
        return translate(VERSION_INFO_ABBR.get(VERSION_INFO(session.version)))


@viewlet_config(name='program-length.menu',
                context=IMovieTheater, layer=IAdminLayer, view=TodayProgramView,
                manager=IToolbarViewletManager, weight=1,
                permission=VIEW_SYSTEM_PERMISSION)
class ProgramLengthMenu(DropdownMenu):
    """Program length menu"""

    @property
    def label(self):
        profile = IOperatorProfile(self.request)
        translate = self.request.localizer.translate
        return translate(_("Program length: {count} day{plural}")).format(
            count=profile.today_program_length,
            plural=translate(_('plural-string', default="s")) if profile.today_program_length > 1 else ""
        )

    status = 'secondary'
    css_class = 'btn-sm'

    def _get_viewlets(self):
        translate = self.request.localizer.translate
        for index in range(1, 8):
            item = MenuItem(self.context, self.request, self.view, self)
            item.label = translate(_("Program length: {count} day{plural}")).format(
                count=index,
                plural=translate(_('plural-string', default="s")) if index > 1 else ""
            )
            item.click_handler = 'MyAMS.msc.session.setProgramLength'
            item.object_data = {
                'msc-length': index
            }
            alsoProvides(item, IObjectData)
            yield f'length_{index}', item


@view_config(name='set-my-program-length.json',
             request_type=IPyAMSLayer,
             request_method='POST', renderer='json', xhr=True)
def set_operator_program_length(request):
    """Set current request operator profile length"""
    profile = IOperatorProfile(request, None)
    if profile is None:
        raise HTTPNotFound()
    length = request.params.get('length')
    if not length:
        raise HTTPBadRequest()
    profile.today_program_length = int(length)
    return {
        'status': 'reload'
    }
