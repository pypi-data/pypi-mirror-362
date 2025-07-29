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

from zope.interface import Interface, implementer
from zope.schema import Choice, Set, TextLine

from pyams_app_msc.feature.profile import IUserProfile
from pyams_app_msc.feature.profile.zmi.interfaces import IUserProfilesSearchResultsTable
from pyams_app_msc.interfaces import MANAGE_BOOKING_PERMISSION
from pyams_app_msc.reference.structure import STRUCTURE_TYPES_VOCABULARY
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces import ISecurityManager
from pyams_security_views.zmi.interfaces import IObjectSecurityMenu
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.registry import get_utility
from pyams_utils.schema import MailAddressField
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import EmptyViewlet, viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.search import SearchForm, SearchResultsView, SearchView
from pyams_zmi.table import I18nColumnMixin, Table, TableElementEditor
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='user-profiles-search.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IObjectSecurityMenu, weight=500,
                permission=MANAGE_BOOKING_PERMISSION)
class UserProfilesSearchMenu(NavigationMenuItem):
    """User profiles search menu"""

    label = _("User profiles")
    href = '#user-profiles-search.html'


class IUserProfilesSearchQuery(Interface):
    """User profiles search query"""

    name = TextLine(title=_("First or last name"),
                    required=False)
    
    email = MailAddressField(title=_("Email address"),
                             required=False)
    
    city = TextLine(title=_("City"),
                    required=False)
    
    structures_types = Set(title=_("Structures types"),
                           value_type=Choice(vocabulary=STRUCTURE_TYPES_VOCABULARY),
                           required=False)


class UserProfilesSearchForm(SearchForm):
    """User profiles search form"""

    title = _("User profiles search form")

    ajax_form_handler = 'user-profiles-search-results.html'
    _edit_permission = MANAGE_BOOKING_PERMISSION


@adapter_config(required=(Interface, IAdminLayer, UserProfilesSearchForm),
                provides=IFormFields)
def user_profiles_search_form_fields(context, request, form):
    """User profiles search form fields getter"""
    return Fields(IUserProfilesSearchQuery)


@pagelet_config(name='user-profiles-search.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=MANAGE_BOOKING_PERMISSION)
class UserProfilesSearchView(SearchView):
    """User profiles search view"""

    title = _("User profiles search form")
    header_label = _("Advanced search")
    search_form = UserProfilesSearchForm


@factory_config(IUserProfilesSearchResultsTable)
@implementer(IObjectData)
class UserProfilesSearchResultsTable(Table):
    """User profiles search results table"""

    object_data = {
        'buttons': ['copy', 'csv', 'excel', 'print'],
        'ams-buttons-classname': 'btn btn-sm btn-secondary'
    }


@adapter_config(required=(IMovieTheater, IPyAMSLayer, IUserProfilesSearchResultsTable),
                provides=IValues)
class UserProfilesSearchResultsValues(ContextRequestViewAdapter):
    """User profiles search results values"""

    @property
    def values(self):
        form = UserProfilesSearchForm(self.context, self.request)
        form.update()
        data, _errors = form.extract_data()
        name = (data.get('name') or '').strip().lower()
        email = data.get('email')
        city = data.get('city')
        structures_types = data.get('structures_types')
        manager = get_utility(ISecurityManager)
        for principal in manager.find_principals('@'):
            profile = IUserProfile(principal)
            if self.context.__name__ not in (profile.local_theaters or ()):
                continue
            if name and (name not in profile.firstname.lower()) and (name not in profile.lastname.lower()):
                continue
            if email and (email != profile.email):
                continue
            if (city and profile.establishment_address and
                    (city.lower() not in profile.establishment_address.city.lower())):
                continue
            if structures_types and (profile.structure_type not in structures_types):
                continue
            yield profile


@adapter_config(name='firstname',
                required=(IMovieTheater, IAdminLayer, IUserProfilesSearchResultsTable),
                provides=IColumn)
class UserProfilesSearchResultsFirstnameColumn(I18nColumnMixin, GetAttrColumn):
    """User profiles firstname column"""

    i18n_header = _("First name")
    attr_name = 'firstname'

    weight = 10


@adapter_config(name='lastname',
                required=(IMovieTheater, IAdminLayer, IUserProfilesSearchResultsTable),
                provides=IColumn)
class UserProfilesSearchResultsLastnameColumn(I18nColumnMixin, GetAttrColumn):
    """User profiles lastname column"""

    i18n_header = _("Last name")
    attr_name = 'lastname'

    weight = 20


@adapter_config(name='email',
                required=(IMovieTheater, IAdminLayer, IUserProfilesSearchResultsTable),
                provides=IColumn)
class UserProfilesSearchResultsEmailColumn(I18nColumnMixin, GetAttrColumn):
    """User profiles mail column"""

    i18n_header = _("Mail address")
    attr_name = 'email'

    weight = 30


@adapter_config(name='phone_number',
                required=(IMovieTheater, IAdminLayer, IUserProfilesSearchResultsTable),
                provides=IColumn)
class UserProfilesSearchResultsPhoneColumn(I18nColumnMixin, GetAttrColumn):
    """User profiles phone number column"""

    i18n_header = _("Phone number")
    attr_name = 'phone_number'

    weight = 40


@adapter_config(name='establishment',
                required=(IMovieTheater, IAdminLayer, IUserProfilesSearchResultsTable),
                provides=IColumn)
class UserProfilesSearchResultsEstablishmentColumn(I18nColumnMixin, GetAttrColumn):
    """User profiles establishment column"""

    i18n_header = _("Establishment")
    attr_name = 'establishment'

    weight = 50


@adapter_config(name='structure_type',
                required=(IMovieTheater, IAdminLayer, IUserProfilesSearchResultsTable),
                provides=IColumn)
class UserProfilesSearchResultsStructureTypeColumn(I18nColumnMixin, GetAttrColumn):
    """User profiles structure type column"""

    i18n_header = _("Structure type")
    attr_name = 'structure_type'

    weight = 60

    def get_value(self, obj):
        return obj.get_structure_type()


@adapter_config(name='city',
                required=(IMovieTheater, IAdminLayer, IUserProfilesSearchResultsTable),
                provides=IColumn)
class UserProfilesSearchResultsCityColumn(I18nColumnMixin, GetAttrColumn):
    """User profiles city column"""

    i18n_header = _("City")
    attr_name = 'city'

    weight = 70
    
    def get_value(self, obj):
        return super().get_value(obj.establishment_address)


@pagelet_config(name='user-profiles-search-results.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=MANAGE_BOOKING_PERMISSION, xhr=True)
class UserProfilesSearchResultsView(SearchResultsView):
    """User profiles search results view"""

    table_label = _("User profiles search results")
    table_class = IUserProfilesSearchResultsTable


@viewlet_config(name='pyams.content_header',
                layer=IAdminLayer, view=UserProfilesSearchResultsView,
                manager=IHeaderViewletManager, weight=10)
class UserProfilesSearchResultsViewHeaderViewlet(EmptyViewlet):
    """User profiles search results view header viewlet"""

    def render(self):
        return '<h1 class="mt-3"></h1>'


@adapter_config(required=(IUserProfile, IAdminLayer, IUserProfilesSearchResultsTable),
                provides=ITableElementEditor)
class UserProfileTableElementEditor(TableElementEditor):
    """User profile table element editor"""
    
    view_name = 'edit-user-profile.html'
    
    @property
    def href(self):
        return absolute_url(self.view.context, self.request, self.view_name,
                            {'principal_id': self.context.principal_id})
    