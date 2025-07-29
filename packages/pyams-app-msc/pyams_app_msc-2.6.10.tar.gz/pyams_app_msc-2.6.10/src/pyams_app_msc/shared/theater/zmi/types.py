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

from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.shared.common.interfaces.types import IDataType, ITypedSharedTool
from pyams_content.shared.common.zmi.types import DataTypeAddForm, DataTypeEditForm, DataTypeLabelsGroup, \
    DataTypePictogramsGroup, \
    DataTypesAddAction
from pyams_content.shared.common.zmi.types.container import SharedToolTypesMenu, SharedToolTypesView
from pyams_content.shared.common.zmi.types.interfaces import ISharedToolTypesTable
from pyams_form.ajax import ajax_form_config
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu, IToolbarViewletManager

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='data-types.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=405,
                permission=MANAGE_TOOL_PERMISSION)
class MovieTheaterSharedToolTypesMenu(SharedToolTypesMenu):
    """Shared tool data types menu"""

    label = _("Activity types")


@viewlet_config(name='add-data-type.action',
                context=IMovieTheater, layer=IAdminLayer, view=ISharedToolTypesTable,
                manager=IToolbarViewletManager, weight=20,
                permission=MANAGE_TOOL_PERMISSION)
class MovieTheaterDataTypesAddAction(DataTypesAddAction):
    """Data type add action"""

    label = _("Add activity type")


@ajax_form_config(name='add-data-type.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class MovieTheaterDataTypeAddForm(DataTypeAddForm):
    """Movie theater data type add form"""

    subtitle = _("New activity type")

    @property
    def fields(self):
        return super().fields.omit('source_folder', 'navigation_label',
                                   'facets_label', 'facets_type_label',
                                   'dashboard_label', 'color', 'pictogram')


@pagelet_config(name='data-types.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=MANAGE_TOOL_PERMISSION)
class MovieTheaterSharedToolTypesView(SharedToolTypesView):
    """Movie theater data types view"""

    title = _("Activities types")
    table_label = _("Movie theater activities types list")


@ajax_form_config(name='properties.html',
                  context=IDataType, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class MovieTheaterDataTypeEditForm(DataTypeEditForm):
    """Movie theater data type properties edit form"""

    @property
    def legend(self):
        manager = get_parent(self.context, IMovieTheater)
        if manager is not None:
            return _("Activity type properties")
        return super().legend

    @property
    def fields(self):
        fields = super().fields
        manager = get_parent(self.context, IMovieTheater)
        if manager is not None:
            fields = fields.omit('source_folder', 'navigation_label',
                                 'facets_label', 'facets_type_label', 'dashboard_label',
                                 'color', 'pictogram')
        return fields


@adapter_config(name='labels.group',
                required=(ITypedSharedTool, IAdminLayer, DataTypeAddForm),
                provides=IGroup)
@adapter_config(name='labels.group',
                required=(IDataType, IAdminLayer, DataTypeEditForm),
                provides=IGroup)
class MovieTheaterDataTypeLabelsGroup(DataTypeLabelsGroup):
    """Movie theater data type pictograms group"""

    def __new__(cls, context, request, view):
        manager = get_parent(context, IMovieTheater)
        if manager is not None:
            return None
        return DataTypeLabelsGroup.__new__(cls)


@adapter_config(name='pictograms.group',
                required=(ITypedSharedTool, IAdminLayer, DataTypeAddForm),
                provides=IGroup)
@adapter_config(name='pictograms.group',
                required=(IDataType, IAdminLayer, DataTypeEditForm),
                provides=IGroup)
class MovieTheaterDataTypePictogramsGroup(DataTypePictogramsGroup):
    """Movie theater data type pictograms group"""

    def __new__(cls, context, request, view):
        manager = get_parent(context, IMovieTheater)
        if manager is not None:
            return None
        return DataTypePictogramsGroup.__new__(cls)
