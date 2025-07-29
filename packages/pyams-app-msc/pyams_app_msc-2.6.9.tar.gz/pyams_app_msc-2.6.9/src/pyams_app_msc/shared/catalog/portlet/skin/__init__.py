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
from datetime import datetime, timedelta, timezone

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Ge, Le, Or
from pyramid.decorator import reify
from zope.interface import Interface, implementer
from zope.intid.interfaces import IIntIds
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.feature.booking.interfaces import IBookingContainer
from pyams_app_msc.feature.planning.interfaces import IPlanning, ISession, VERSION_INFO, VERSION_INFO_ABBR
from pyams_app_msc.shared.catalog.interfaces import ICatalogEntry, ICatalogEntryInfo, IWfCatalogEntry
from pyams_app_msc.shared.catalog.portlet.skin.interfaces import ICatalogViewItemsPortletCalendarRendererSettings, \
    ICatalogViewItemsPortletPanelsRendererSettings
from pyams_app_msc.shared.theater.audience import get_audience_contact
from pyams_app_msc.shared.theater.interfaces import IMovieTheater, IMovieTheaterSettings, SESSION_REQUEST_MODE
from pyams_catalog.query import CatalogResultSet, IsNone
from pyams_content.feature.filter.container import FilterContainer
from pyams_content.feature.filter.interfaces import IAggregatedPortletRendererSettings
from pyams_content.shared.view.portlet.interfaces import IViewItemsPortletSettings
from pyams_content.shared.view.portlet.skin import ViewItemsPortletPanelsRenderer, \
    ViewItemsPortletPanelsRendererSettings, WfSharedContentViewItemRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer, IPyAMSUserLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_template.template import override_template, template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config, get_interface_base_name
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import canonical_url, relative_url

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


#
# Catalog view items portlet calendar renderer
#

@factory_config(ICatalogViewItemsPortletCalendarRendererSettings)
@implementer(IAggregatedPortletRendererSettings)
class CatalogViewItemsPortletCalendarRendererSettings(FilterContainer):
    """Catalog view items portlet calendar renderer settings"""

    filters_css_class = FieldProperty(ICatalogViewItemsPortletCalendarRendererSettings['filters_css_class'])
    calendar_css_class = FieldProperty(ICatalogViewItemsPortletCalendarRendererSettings['calendar_css_class'])
    sessions_weeks = FieldProperty(ICatalogViewItemsPortletCalendarRendererSettings['sessions_weeks'])


@adapter_config(name='catalog-calendar',
                required=(IPortalContext, IPyAMSLayer, Interface, IViewItemsPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/view-catalog-calendar.pt',
                 layer=IPyAMSLayer)
class CatalogViewItemsPortletCalendarRenderer(ViewItemsPortletPanelsRenderer):
    """Catalog view items portlet calendar renderer"""

    label = _("MSC: Catalog entries month calendar")
    weight = 110

    settings_interface = ICatalogViewItemsPortletCalendarRendererSettings
    use_authentication = True

    @reify
    def audience(self):
        """Audience getter"""
        return self.request.params.get('audience')

    def get_calendar_config(self, results):
        now = tztime(datetime.now(timezone.utc))
        end = now + timedelta(weeks=self.renderer_settings.sessions_weeks)
        theater = get_parent(self.context, IMovieTheater)
        translate = self.request.localizer.translate
        config = {
            'contentHeight': 'auto',
            'validRange': {
                'start': now.isoformat(),
                'end': end.isoformat()
            },
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
        events = []
        audience = self.audience
        for result in results:
            planning = IPlanning(result, None)
            if planning is None:
                continue
            for session in planning.values():
                if (not session.extern_bookable) or (session.start_date < now) or (session.start_date > end):
                    continue
                if audience:
                    audiences = session.audiences
                    if (not audiences) and IWfCatalogEntry.providedBy(result):
                        audiences = result.audiences or ()
                    if audience not in audiences:
                        continue
                events.append({
                    'title': II18n(result).query_attribute('title', request=self.request),
                    'href': relative_url(result, self.request,
                                         display_context=theater,
                                         view_name='booking-new.html',
                                         query={
                                             'session_id': ICacheKeyValue(session),
                                             'audience': audience
                                         }),
                    'start': session.start_date.isoformat(),
                    'end': session.end_date.isoformat()
                })
        config['events'] = events
        return json.dumps(config)

    def get_session_request_url(self, context):
        theater = get_parent(self.context, IMovieTheater)
        settings = IMovieTheaterSettings(theater)
        if not settings.allow_session_request:
            return None
        if settings.session_request_mode == SESSION_REQUEST_MODE.FORM.value:
            return canonical_url(context, self.request, 'session-request.html', {
                'audience': self.audience
            })
        contact_email = get_audience_contact(theater, self.audience)
        return f'mailto:{contact_email}'


#
# Catalog view items portlet panels renderer
#

@factory_config(ICatalogViewItemsPortletPanelsRendererSettings)
@implementer(IAggregatedPortletRendererSettings)
class CatalogViewItemsPortletPanelsRendererSettings(ViewItemsPortletPanelsRendererSettings):
    """Catalog view items portlet panels renderer settings"""

    first_panel_css_class = FieldProperty(ICatalogViewItemsPortletPanelsRendererSettings['first_panel_css_class'])
    panels_css_class = FieldProperty(ICatalogViewItemsPortletPanelsRendererSettings['panels_css_class'])
    display_sessions = FieldProperty(ICatalogViewItemsPortletPanelsRendererSettings['display_sessions'])
    sessions_weeks = FieldProperty(ICatalogViewItemsPortletPanelsRendererSettings['sessions_weeks'])
    display_free_seats = FieldProperty(ICatalogViewItemsPortletPanelsRendererSettings['display_free_seats'])

    def get_css_class(self):
        columns = self.columns_count
        return ' '.join((
            f'col-{12 // selection.cols}' if device == 'xs' else f'col-{device}-{12 // selection.cols}'
            for device, selection in columns.items()
        ))


@adapter_config(name='catalog-panels',
                required=(IPortalContext, IPyAMSLayer, Interface, IViewItemsPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/view-catalog-panels.pt',
                 layer=IPyAMSLayer)
class CatalogViewItemsPortletPanelsRenderer(ViewItemsPortletPanelsRenderer):
    """Catalog view items portlet catalog panels renderer"""

    label = _("MSC: Catalog entries with next planned sessions")
    weight = 120

    settings_interface = ICatalogViewItemsPortletPanelsRendererSettings
    use_authentication = True

    @reify
    def audience(self):
        """Audience getter"""
        return self.request.params.get('audience')

    @classmethod
    def get_next_booking_period(cls, item):
        """Catalog entry information getter"""
        if 'booking_period' not in (item.field_names or ()):
            return None
        return ICatalogEntryInfo(item).booking_period

    def get_sessions(self, wf_entry):
        """Display incoming sessions for provided catalog entry"""
        entry = get_parent(wf_entry, ICatalogEntry)
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

    def get_version(self, session):
        """Get displayed version of provided entry"""
        if not session.version:
            return ''
        translate = self.request.localizer.translate
        return translate(VERSION_INFO_ABBR.get(VERSION_INFO(session.version), _("(undefined)")))

    @staticmethod
    def get_free_seats(session):
        """Get free seats for provided session"""
        bookings = IBookingContainer(session, None)
        if bookings is None:
            return session.capacity, session.capacity
        return session.capacity - bookings.get_confirmed_seats(), session.capacity

    def get_session_request_url(self, context):
        theater = get_parent(context, IMovieTheater)
        settings = IMovieTheaterSettings(theater)
        if not settings.allow_session_request:
            return None
        if settings.session_request_mode == SESSION_REQUEST_MODE.FORM.value:
            return canonical_url(context, self.request, 'session-request.html', {
                'audience': self.audience
            })
        theater = get_parent(self.context, IMovieTheater)
        contact_email = get_audience_contact(theater, self.request.params.get('audience'))
        return f'mailto:{contact_email}'


override_template(WfSharedContentViewItemRenderer,
                  name='catalog-item-panel',
                  template='templates/view-catalog-item-panel.pt',
                  layer=IPyAMSUserLayer)
