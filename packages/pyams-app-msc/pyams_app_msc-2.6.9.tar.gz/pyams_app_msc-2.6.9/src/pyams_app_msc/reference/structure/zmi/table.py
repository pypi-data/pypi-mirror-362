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

from pyramid.decorator import reify
from zope.interface import Interface

from pyams_app_msc.reference.structure import IStructureTypeTable
from pyams_content.reference.zmi.table import ReferenceTableContainerTable
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_zmi.interfaces.viewlet import IPropertiesMenu, ISiteManagementMenu
from pyams_zmi.table import TableAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


STRUCTURES_TYPES_TABLE_LABEL = _("Structures types")


@adapter_config(required=(IStructureTypeTable, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def structure_type_table_label(context, request, view):
    """Structures types table label"""
    return request.localizer.translate(STRUCTURES_TYPES_TABLE_LABEL)


@viewletmanager_config(name='contents.menu',
                       context=IStructureTypeTable, layer=IAdminLayer,
                       manager=ISiteManagementMenu, weight=10,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IPropertiesMenu)
class StructureTypeTableContentsMenu(NavigationMenuItem):
    """Structures types table contents menu"""

    label = _("Table contents")
    icon_class = 'fas fa-table'
    href = '#contents.html'


class StructureTypeTableContainerTable(ReferenceTableContainerTable):
    """Structures types container table"""

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        attributes['table'].update({
            'data-ams-order': '0,asc'
        })
        return attributes


@pagelet_config(name='contents.html',
                context=IStructureTypeTable, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class StructureTypeTableContentsView(TableAdminView):
    """Structures types table contents view"""

    title = _("Structures types")

    table_class = StructureTypeTableContainerTable
    table_label = _("Structures types list")


@adapter_config(required=(IStructureTypeTable, IAdminLayer, IPropertiesEditForm),
                provides=IFormTitle)
def structure_type_table_title(context, request, form):
    """Structures types table edit form title getter"""
    translate = request.localizer.translate
    return translate(_("Structures types table"))
