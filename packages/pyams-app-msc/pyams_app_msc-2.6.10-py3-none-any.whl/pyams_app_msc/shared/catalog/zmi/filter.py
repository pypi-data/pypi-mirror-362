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

from pyams_app_msc.shared.catalog.interfaces import IAudienceFilter, IDurationFilter
from pyams_content.feature.filter.interfaces import IFiltersContainer
from pyams_content.feature.filter.zmi import FilterAddForm, FilterAddMenu, FilterEditForm, FiltersTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


#
# Activity audiences filter components
#

@viewlet_config(name='add-audience-filter.menu',
                context=IFiltersContainer, layer=IAdminLayer, view=FiltersTable,
                manager=IContextAddingsViewletManager, weight=100,
                permission=MANAGE_TEMPLATE_PERMISSION)
class AudienceFilterAddMenu(FilterAddMenu):
    """Audience filter add menu"""

    label = _("Audience filter")
    href = 'add-audience-filter.html'


@ajax_form_config(name='add-audience-filter.html',
                  context=IFiltersContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class AudienceFilterAddForm(FilterAddForm):
    """Audience filter add form"""

    content_factory = IAudienceFilter


@ajax_form_config(name='properties.html',
                  context=IAudienceFilter, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class AudienceFilterEditForm(FilterEditForm):
    """Audience filter edit form"""


#
# Activity duration filter components
#

@viewlet_config(name='add-duration-filter.menu',
                context=IFiltersContainer, layer=IAdminLayer, view=FiltersTable,
                manager=IContextAddingsViewletManager, weight=110,
                permission=MANAGE_TEMPLATE_PERMISSION)
class DurationFilterAddMenu(FilterAddMenu):
    """Duration filter add menu"""

    label = _("Duration filter")
    href = 'add-duration-filter.html'


@ajax_form_config(name='add-duration-filter.html',
                  context=IFiltersContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class DurationFilterAddForm(FilterAddForm):
    """Duration filter add form"""

    fields = Fields(IDurationFilter).omit('visible')
    content_factory = IDurationFilter


@ajax_form_config(name='properties.html',
                  context=IDurationFilter, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class DurationFilterEditForm(FilterEditForm):
    """Duration filter edit form"""

    fields = Fields(IDurationFilter).omit('visible')
