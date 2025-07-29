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

from pyams_app_msc.reference.structure.interfaces import IStructureType, IStructureTypeTable
from pyams_app_msc.reference.structure.zmi.table import StructureTypeTableContainerTable
from pyams_content.interfaces import MANAGE_REFERENCE_TABLE_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.view import IModalEditForm, IModalPage
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.intids import IUniqueID
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_row_add_callback, get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='add-structure-type.menu',
                context=IStructureTypeTable, layer=IAdminLayer, view=StructureTypeTableContainerTable,
                manager=IToolbarViewletManager, weight=10,
                permission=MANAGE_REFERENCE_TABLE_PERMISSION)
class StructureTypeAddAction(ContextAddAction):
    """StructureType add action"""

    label = _("Add structure type")
    href = 'add-structure-type.html'


@ajax_form_config(name='add-structure-type.html',
                  context=IStructureTypeTable, layer=IPyAMSLayer,
                  permission=MANAGE_REFERENCE_TABLE_PERMISSION)
class StructureTypeAddForm(AdminModalAddForm):
    """Structure type add form"""

    subtitle = _("New structure type")
    legend = _("New structure type properties")
    modal_class = 'modal-xl'

    fields = Fields(IStructureType).select('title')
    content_factory = IStructureType

    def add(self, obj):
        oid = IUniqueID(obj).oid
        self.context[oid] = obj


@adapter_config(required=(IStructureTypeTable, IAdminLayer, IModalPage),
                provides=IFormTitle)
def structure_type_add_form_title(context, request, view):
    """Structure type add form title"""
    return get_object_label(context, request, view)


@adapter_config(required=(IStructureTypeTable, IAdminLayer, StructureTypeAddForm),
                provides=IAJAXFormRenderer)
class StructureTypeAddFormAJAXRenderer(ContextRequestViewAdapter):
    """Structure type add form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        table = get_parent(self.context, IStructureTypeTable)
        return {
            'callbacks': [
                get_json_table_row_add_callback(table, self.request,
                                                StructureTypeTableContainerTable, changes)
            ]
        }


@adapter_config(required=(IStructureType, IAdminLayer, Interface),
                provides=ITableElementEditor)
class StructureTypeElementEditor(TableElementEditor):
    """Structure type table element editor"""


@ajax_form_config(name='properties.html',
                  context=IStructureType, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class StructureTypeEditForm(AdminModalEditForm):
    """Structure type properties edit form"""

    @property
    def subtitle(self):
        translate = self.request.localizer.translate
        return translate(_("Structure type: {}")).format(
            II18n(self.context).query_attribute('title', request=self.request))

    legend = _("Structure type properties")
    modal_class = 'modal-xl'

    fields = Fields(IStructureType).select('title')


@adapter_config(required=(IStructureType, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def structure_type_edit_form_title(context, request, form):
    """Structure type edit form title"""
    table = get_utility(IStructureTypeTable)
    return TITLE_SPAN.format(get_object_label(table, request, form))


@adapter_config(required=(IStructureType, IAdminLayer, StructureTypeEditForm),
                provides=IAJAXFormRenderer)
class StructureTypeEditFormAJAXRenderer(ContextRequestViewAdapter):
    """Structure type edit form AJAX renderer"""

    def render(self, changes):
        """AJAX result renderer"""
        if not changes:
            return None
        table = get_parent(self.context, IStructureTypeTable)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(table, self.request,
                                                    StructureTypeTableContainerTable, self.context)
            ]
        }
