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

from datetime import datetime

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Any, Eq, Ge, Le
from zope.interface import Interface, implementer
from zope.schema import Bool, Choice, List, TextLine
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_app_msc.feature.booking import IBookingInfo
from pyams_app_msc.feature.booking.interfaces import BOOKING_STATUS, BOOKING_STATUS_VOCABULARY
from pyams_app_msc.feature.booking.zmi.dashboard import BookingStatusTable, get_booking_element
from pyams_app_msc.feature.booking.zmi.interfaces import IBookingDashboardMenu
from pyams_app_msc.feature.profile import IUserProfile
from pyams_app_msc.interfaces import VIEW_BOOKING_PERMISSION
from pyams_app_msc.reference.structure import STRUCTURE_TYPES_VOCABULARY
from pyams_app_msc.shared.catalog import ICatalogEntry, IWfCatalogEntry
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.room import ROOMS_SEATS_VOCABULARY
from pyams_app_msc.shared.theater.interfaces.session import IMovieTheaterSession
from pyams_catalog.query import CatalogResultSet
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.schema import PrincipalsSetField
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_sequence.schema import InternalReferencesListField
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import get_interface_base_name
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.list import unique_iter
from pyams_utils.registry import get_utility
from pyams_utils.schema import DatesRangeField
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import EmptyViewlet, viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.search import SearchForm, SearchResultsView, SearchView
from pyams_zmi.table import I18nColumnMixin
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='advanced-booking-search.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IBookingDashboardMenu, weight=40,
                permission=VIEW_BOOKING_PERMISSION)
class BookingAdvancedSearchMenu(NavigationMenuItem):
    """Booking advanced search menu"""

    label = _("Advanced search")
    href = '#booking-advanced-search.html'


class IBookingAdvancedSearchQuery(Interface):
    """Booking advanced search query interface"""

    recipients = PrincipalsSetField(title=_("Recipients"),
                                    required=False)

    activities = InternalReferencesListField(title=_("Activities"),
                                             required=False)

    establishment = TextLine(title=_("Establishment"),
                             required=False)

    city = TextLine(title=_("City"),
                    required=False)

    structure_types = List(title=_("Structures types"),
                           value_type=Choice(vocabulary=STRUCTURE_TYPES_VOCABULARY),
                           required=False)

    status = List(title=_("Status"),
                  value_type=Choice(vocabulary=BOOKING_STATUS_VOCABULARY),
                  required=False)

    include_archives = Bool(title=_("Include archives"),
                            required=False,
                            default=False)

    session = DatesRangeField(title=_("Session date"),
                              required=False)

    created = DatesRangeField(title=_("Creation date"),
                              required=False)

    modified = DatesRangeField(title=_("Modification date"),
                               required=False)


class BookingAdvancedSearchForm(SearchForm):
    """Booking advanced search form"""

    title = _("Bookings search form")

    ajax_form_handler = 'booking-advanced-search-results.html'
    _edit_permission = VIEW_BOOKING_PERMISSION


@adapter_config(required=(Interface, IAdminLayer, BookingAdvancedSearchForm),
                provides=IFormFields)
def booking_advanced_search_form_fields(context, request, form):
    """Booking advanced search form fields"""
    return Fields(IBookingAdvancedSearchQuery)


@pagelet_config(name='booking-advanced-search.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=VIEW_BOOKING_PERMISSION)
class BookingAdvancedSearchView(SearchView):
    """Booking advanced search view"""

    title = _("Bookings search form")
    header_label = _("Advanced search")
    search_form = BookingAdvancedSearchForm


@implementer(IObjectData)
class BookingAdvancedSearchResultsTable(BookingStatusTable):
    """Booking advanced search form results table"""

    object_data = {
        'buttons': ['colvis', 'copy', 'csv', 'excel', 'print'],
        'ams-buttons-classname': 'btn btn-sm btn-secondary'
    }


@adapter_config(name='establishment',
                required=(IMovieTheater, IAdminLayer, BookingAdvancedSearchResultsTable),
                provides=IColumn)
@implementer(IObjectData)
class BookingStatusEstablishmentColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status establishment column"""

    i18n_header = _("Establishment")
    object_data = {
        'visible': False
    }
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 26

    def get_value(self, obj):
        profile = IUserProfile(obj.booking, None)
        if profile is not None:
            return profile.establishment
        return MISSING_INFO


@adapter_config(name='structure_type',
                required=(IMovieTheater, IAdminLayer, BookingAdvancedSearchResultsTable),
                provides=IColumn)
@implementer(IObjectData)
class BookingStatusStructureTypeColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status structure type column"""

    i18n_header = _("Structure type")
    object_data = {
        'visible': False
    }
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 27

    def get_value(self, obj):
        profile = IUserProfile(obj.booking, None)
        return profile.get_structure_type() if profile is not None else MISSING_INFO


@adapter_config(name='city',
                required=(IMovieTheater, IAdminLayer, BookingAdvancedSearchResultsTable),
                provides=IColumn)
@implementer(IObjectData)
class BookingStatusCityColumn(I18nColumnMixin, GetAttrColumn):
    """Booking status city column"""

    i18n_header = _("City")
    object_data = {
        'visible': False
    }
    css_classes = {
        'td': 'text-nowrap'
    }
    weight = 28

    def get_value(self, obj):
        profile = IUserProfile(obj.booking, None)
        if profile is not None:
            address = profile.establishment_address
            return address.city if address is not None else MISSING_INFO
        return MISSING_INFO


@adapter_config(required=(IMovieTheater, IPyAMSLayer, BookingAdvancedSearchResultsTable),
                provides=IValues)
class BookingAdvancedSearchResultsValues(ContextRequestViewAdapter):
    """Booking advanced search results values"""

    def get_params(self, data):
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, ROOMS_SEATS_VOCABULARY)
        params = And(Eq(catalog['object_types'], get_interface_base_name(IBookingInfo)),
                     Any(catalog['planning_room'], vocabulary.by_value.keys()),
                     Eq(catalog['booking_status'], [status.value for status in BOOKING_STATUS]))
        if data.get('recipients'):
            params &= Any(catalog['booking_recipient'], data['recipients'])
        if data.get('status'):
            params &= Any(catalog['booking_status'], data['status'])
        session_after, session_before = data.get('session', (None, None))
        if session_after:
            params &= Ge(catalog['planning_start_date'],
                         tztime(datetime.fromisoformat(session_after.isoformat())))
        if session_before:
            params &= Le(catalog['planning_end_date'],
                         tztime(datetime.fromisoformat(session_before.isoformat())))
        created_after, created_before = data.get('created', (None, None))
        if created_after:
            params &= Ge(catalog['created_date'],
                         tztime(datetime.fromisoformat(created_after.isoformat())))
        if created_before:
            params &= Le(catalog['created_date'],
                         tztime(datetime.fromisoformat(created_before.isoformat())))
        modified_after, modified_before = data.get('modified', (None, None))
        if modified_after:
            params &= Ge(catalog['modified_date'],
                         tztime(datetime.fromisoformat(modified_after.isoformat())))
        if modified_before:
            params &= Le(catalog['modified_date'],
                         tztime(datetime.fromisoformat(modified_before.isoformat())))
        return params

    @property
    def values(self):
        """Booking advanced search results values getter"""

        def booking_filter(item):
            booking = item.booking
            if booking.archived and (not data.get('include_archives')):
                return False
            session = item.session
            oids = data.get('activities')
            if oids:
                if IMovieTheaterSession.providedBy(session):
                    catalog_entry = IWfCatalogEntry(session, None)
                else:
                    catalog_entry = get_parent(session, ICatalogEntry)
                if catalog_entry is None:
                    return False
                if ISequentialIdInfo(catalog_entry).hex_oid not in oids:
                    return False
            profile = IUserProfile(booking, None)
            if profile is None:
                return False
            establishment = data.get('establishment')
            if establishment and (
                    (not profile.establishment) or
                    (establishment.lower() not in profile.establishment.lower())):
                return False
            city = data.get('city')
            if city:
                if not profile.establishment_address:
                    return False
                if city.lower() not in profile.establishment_address.city.lower():
                    return False
            structure_types = data.get('structure_types')
            if structure_types and (profile.structure_type not in structure_types):
                return False
            return True

        form = BookingAdvancedSearchForm(self.context, self.request)
        form.update()
        data, _errors = form.extract_data()
        params = self.get_params(data)
        catalog = get_utility(ICatalog)
        yield from filter(booking_filter,
                          map(get_booking_element,
                              unique_iter(CatalogResultSet(CatalogQuery(catalog).query(params)))))


@pagelet_config(name='booking-advanced-search-results.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=VIEW_BOOKING_PERMISSION, xhr=True)
class BookingAdvancedSearchResultsView(SearchResultsView):
    """Booking advanced search results view"""

    table_label = _("Search results")
    table_class = BookingAdvancedSearchResultsTable


@viewlet_config(name='pyams.content_header',
                layer=IAdminLayer, view=BookingAdvancedSearchResultsView,
                manager=IHeaderViewletManager, weight=10)
class BookingAdvancedSearchResultsViewHeaderViewlet(EmptyViewlet):
    """Booking advanced search results view header viewlet"""

    def render(self):
        return '<h1 class="mt-3"></h1>'
