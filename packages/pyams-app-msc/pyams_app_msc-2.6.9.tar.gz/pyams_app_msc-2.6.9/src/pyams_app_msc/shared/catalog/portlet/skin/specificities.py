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
from hypatia.query import And, Eq, Ge, Le, Or
from persistent import Persistent
from pyramid.decorator import reify
from zope.container.contained import Contained
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.feature.booking import IBookingContainer
from pyams_app_msc.feature.planning.interfaces import ISession, VERSION_INFO, VERSION_INFO_ABBR
from pyams_app_msc.shared.catalog import ICatalogEntry, ICatalogEntryInfo, IWfCatalogEntry
from pyams_app_msc.shared.catalog.portlet.skin.interfaces import ICatalogEntrySpecificitiesPortletRendererSettings
from pyams_app_msc.shared.theater import IMovieTheater, IMovieTheaterSettings
from pyams_app_msc.shared.theater.audience import get_audience_contact
from pyams_app_msc.shared.theater.interfaces import SESSION_REQUEST_MODE
from pyams_catalog.query import CatalogResultSet, IsNone
from pyams_content.shared.common.portlet.interfaces import ISharedContentSpecificitiesPortletSettings
from pyams_i18n.language import BASE_LANGUAGES
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config, get_interface_base_name
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import canonical_url

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@factory_config(ICatalogEntrySpecificitiesPortletRendererSettings)
class CatalogEntrySpecificitiesPortletRendererSettings(Persistent, Contained):
    """Catalog entry specificities portlet renderer settings"""

    display_sessions = FieldProperty(ICatalogEntrySpecificitiesPortletRendererSettings['display_sessions'])
    sessions_weeks = FieldProperty(ICatalogEntrySpecificitiesPortletRendererSettings['sessions_weeks'])
    display_free_seats = FieldProperty(ICatalogEntrySpecificitiesPortletRendererSettings['display_free_seats'])


@adapter_config(name='msc:catalog_entry',
                required=(IPortalContext, IPyAMSLayer, Interface, ISharedContentSpecificitiesPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/specificities.pt',
                 layer=IPyAMSLayer)
class CatalogEntrySpecificitiesPortletRenderer(PortletRenderer):
    """Catalog entry specificities portlet renderer"""

    label = _("MSC: catalog entry specificities with sessions")
    weight = 100

    settings_interface = ICatalogEntrySpecificitiesPortletRendererSettings

    use_authentication = True
    entry_info = None

    def update(self):
        super().update()
        self.entry_info = ICatalogEntryInfo(self.context, None)

    def render(self, template_name=''):
        if self.entry_info is None:
            return ''
        return super().render(template_name)

    @reify
    def audience(self):
        """Audience getter"""
        return self.request.params.get('audience')

    def get_language(self, value):
        translate = self.request.localizer.translate
        return translate(BASE_LANGUAGES.get(value, _("(unknown)")))

    def get_version(self, session):
        if not session.version:
            return None
        translate = self.request.localizer.translate
        return translate(VERSION_INFO_ABBR.get(VERSION_INFO(session.version), _("(undefined)")))

    def get_duration(self, value):
        translate = self.request.localizer.translate
        hours = value // 60
        minutes = value % 60
        if hours == 0:
            return translate(_("{} minutes")).format(minutes)
        return translate(_("{}h {}min")).format(hours, minutes)

    def get_sessions(self):
        """Display incoming sessions for provided catalog entry"""
        entry = get_parent(self.context, ICatalogEntry)
        catalog = get_utility(ICatalog)
        intids = get_utility(IIntIds)
        now = tztime(datetime.now(timezone.utc))
        params = [
            Eq(catalog['object_types'], get_interface_base_name(ISession)),
            Eq(catalog['parents'], intids.queryId(entry)),
            Ge(catalog['planning_start_date'], now),
            Le(catalog['planning_end_date'], now + timedelta(weeks=self.renderer_settings.sessions_weeks))
        ]
        if self.audience:
            params.append(Or(Eq(catalog['planning_audience'], self.audience),
                             IsNone(catalog['planning_audience'])))
        query = And(*params)
        yield from sorted(filter(lambda x: x.extern_bookable,
                                 CatalogResultSet(CatalogQuery(catalog).query(query))),
                          key=lambda x: x.start_date)

    @staticmethod
    def get_free_seats(session):
        """Get free seats for provided session"""
        bookings = IBookingContainer(session, None)
        if bookings is None:
            return session.capacity, session.capacity
        return session.capacity - bookings.get_confirmed_seats(), session.capacity

    def get_next_booking_period(self):
        """Catalog entry information getter"""
        if 'booking_period' not in (self.context.field_names or ()):
            return None
        return ICatalogEntryInfo(self.context).booking_period

    def get_session_request_url(self, context):
        """Get URL for a new session request view"""
        if not IWfCatalogEntry(context).can_request_session():
            return None
        theater = get_parent(context, IMovieTheater)
        settings = IMovieTheaterSettings(theater)
        if settings.session_request_mode == SESSION_REQUEST_MODE.FORM.value:
            params = {}
            audiences = IWfCatalogEntry(self.context).audiences
            if len(audiences or ()) == 1:
                params['audience'] = audiences[0]
            elif self.audience:
                params['audience'] = self.audience
            return canonical_url(context, self.request, 'session-request.html', params)
        contact_email = None
        theater = get_parent(self.context, IMovieTheater)
        for audience_id in self.context.audiences:
            contact_email = get_audience_contact(theater, audience_id)
            if contact_email is not None:
                break
        return f'mailto:{contact_email}' if contact_email else None
