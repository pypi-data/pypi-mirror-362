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

from zope.interface import Interface

from pyams_app_msc.shared.catalog.portlet.skin.interfaces import ICatalogViewItemsPortletCalendarRendererSettings, \
    ICatalogViewItemsPortletPanelsRendererSettings
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_portal.zmi.interfaces import IPortletRendererSettingsEditForm
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupChecker, FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


#
# Catalog view items portlet calendar renderer settings edit form
#

@adapter_config(required=(ICatalogViewItemsPortletCalendarRendererSettings, IAdminLayer,
                          IPortletRendererSettingsEditForm),
                provides=IFormFields)
def catalog_view_items_calendar_renderer_settings_fields(context, request, form):
    return Fields(Interface)


@adapter_config(name='css-classes',
                required=(ICatalogViewItemsPortletCalendarRendererSettings, IAdminLayer,
                          IPortletRendererSettingsEditForm),
                provides=IGroup)
class CatalogViewItemsPortletCalendarRendererClassesSettingsGroup(FormGroupSwitcher):
    """Catalog view items portlet calendar renderer CSS classes settings group"""

    legend = _("CSS classes")

    fields = Fields(ICatalogViewItemsPortletCalendarRendererSettings).select('filters_css_class',
                                                                             'calendar_css_class')
    weight = 5


@adapter_config(name='base',
                required=(ICatalogViewItemsPortletCalendarRendererSettings, IAdminLayer,
                          IPortletRendererSettingsEditForm),
                provides=IGroup)
class CatalogViewItemsPortletCalendarRendererBaseSettingsGroup(Group):
    """Catalog view items portlet calendar renderer settings group"""

    legend = _("Sessions display")

    fields = Fields(ICatalogViewItemsPortletCalendarRendererSettings).select('sessions_weeks')
    weight = 10


#
# Catalog view items portlet panels renderer settings edit form
#

@adapter_config(name='css-classes',
                required=(ICatalogViewItemsPortletPanelsRendererSettings, IAdminLayer,
                          IPortletRendererSettingsEditForm),
                provides=IGroup)
class CatalogViewItemsPortletPanelsRendererClassesSettingsGroup(FormGroupSwitcher):
    """Catalog view items portlet panels renderer CSS classes settings group"""

    legend = _("CSS classes")

    fields = Fields(ICatalogViewItemsPortletPanelsRendererSettings).select('filters_css_class',
                                                                           'results_css_class',
                                                                           'first_panel_css_class',
                                                                           'panels_css_class')
    weight = 5


@adapter_config(name='properties',
                required=(ICatalogViewItemsPortletPanelsRendererSettings, IAdminLayer,
                          IPortletRendererSettingsEditForm),
                provides=IGroup)
class CatalogViewItemsPortletPanelsRendererSettingsPropertiesGroup(FormGroupChecker):
    """Catalog view items portlet panels renderer settings group"""

    fields = Fields(ICatalogViewItemsPortletPanelsRendererSettings).select('display_sessions', 'sessions_weeks',
                                                                           'display_free_seats')
    weight = 25
