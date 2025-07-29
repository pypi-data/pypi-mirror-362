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

from pyramid.view import view_config
from zope.interface import Interface

from pyams_app_msc.interfaces import MANAGE_THEATER_PERMISSION, VIEW_THEATER_PERMISSION
from pyams_app_msc.shared.theater import ICinemaAudienceContainerTarget
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.audience import ICinemaAudience, ICinemaAudienceContainer
from pyams_app_msc.shared.theater.zmi.interfaces import ICinemaAudiencesTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_skin.interfaces.view import IModalEditForm
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm, SimpleAddFormRenderer, SimpleEditFormRenderer
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectLabel, TITLE_SPAN, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IPropertiesMenu, IToolbarViewletManager
from pyams_zmi.table import AttributeSwitcherColumn, NameColumn, ReorderColumn, SortableTable, TableAdminView, \
    TableElementEditor, TrashColumn
from pyams_zmi.utils import get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='cinema-audiences.menu',
                context=ICinemaAudienceContainerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=530,
                permission=VIEW_THEATER_PERMISSION)
class CinemaAudiencesMenu(NavigationMenuItem):
    """Cinema audiences menu"""

    label = _("Cinema audiences")
    href = '#cinema-audiences.html'


@factory_config(ICinemaAudiencesTable)
class CinemaAudiencesTable(SortableTable):
    """Cinema audiences table"""

    container_class = ICinemaAudienceContainer

    display_if_empty = True


@adapter_config(required=(ICinemaAudienceContainerTarget, IAdminLayer, ICinemaAudiencesTable),
                provides=IValues)
class CinemaAudiencesTableValues(ContextRequestViewAdapter):
    """Cinema audiences table values adapter"""

    @property
    def values(self):
        """Cinema audiences values getter"""
        yield from ICinemaAudienceContainer(self.context).values()


@adapter_config(name='reorder',
                required=(ICinemaAudienceContainerTarget, IAdminLayer, ICinemaAudiencesTable),
                provides=IColumn)
class CinemaAudiencesTableReorderColumn(ReorderColumn):
    """Cinema audiences table reorder column"""


@view_config(name='reorder.json',
             context=ICinemaAudienceContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_THEATER_PERMISSION)
def reorder_cinema_audience_table(request):
    """Reorder cinema audience table"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='active',
                required=(ICinemaAudienceContainerTarget, IAdminLayer, ICinemaAudiencesTable),
                provides=IColumn)
class CinemaAudiencesActiveColumn(AttributeSwitcherColumn):
    """Cinema audiences table active column"""

    attribute_name = 'active'
    attribute_switcher = 'switch-active-audience.json'

    icon_off_class = 'far fa-eye-slash text-danger'

    permission = MANAGE_THEATER_PERMISSION
    weight = 1

    def get_icon_hint(self, item):
        """Icon hint getter"""
        if self.has_permission(item):
            hint = _("Click icon to switch audience activity")
        elif item.active:
            hint = _("This audience is active")
        else:
            hint = _("This audience is not active")
        return self.request.localizer.translate(hint)


@view_config(name='switch-active-audience.json',
             context=ICinemaAudienceContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_active_audience(request):
    """Switch cinema audience activity flag"""
    return switch_element_attribute(request, container_factory=ICinemaAudienceContainer)


@adapter_config(name='label',
                required=(ICinemaAudienceContainerTarget, IAdminLayer, ICinemaAudiencesTable),
                provides=IColumn)
class CinemaAudienceLabelColumn(NameColumn):
    """Cinema audiences table label column"""

    attr_name = 'name'
    i18n_header = _("Audience name")


@adapter_config(name='trash',
                required=(ICinemaAudienceContainerTarget, IAdminLayer, ICinemaAudiencesTable),
                provides=IColumn)
class CinemaAudienceTrashColumn(TrashColumn):
    """Cinema audiences table trash column"""

    object_data = {
        'ams-modules': 'container',
        'ams-delete-target': 'delete-cinema-audience.json'
    }


@view_config(name='delete-cinema-audience.json',
             context=ICinemaAudienceContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_THEATER_PERMISSION)
def delete_cinema_audience(request):
    """Delete cinema audience"""
    return delete_container_element(request, container_factory=ICinemaAudienceContainer)


@pagelet_config(name='cinema-audiences.html',
                context=ICinemaAudienceContainerTarget, layer=IPyAMSLayer,
                permission=VIEW_THEATER_PERMISSION)
class CinemaAudiencesView(TableAdminView):
    """Cinema audiences view"""

    title = _("Cinema audiences")

    table_class = ICinemaAudiencesTable
    table_label = _("Cinema audiences list")


#
# Cinema audiences components
#

@viewlet_config(name='add-cinema-audience.action',
                context=ICinemaAudienceContainerTarget, layer=IAdminLayer, view=ICinemaAudiencesTable,
                manager=IToolbarViewletManager, weight=20,
                permission=MANAGE_THEATER_PERMISSION)
class CinemaAudienceAddAction(ContextAddAction):
    """Cinema audience add action"""

    label = _("Add audience")
    href = 'add-cinema-audience.html'


@ajax_form_config(name='add-cinema-audience.html',
                  context=ICinemaAudienceContainerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_THEATER_PERMISSION)
class CinemaAudienceAddForm(AdminModalAddForm):
    """Cinema audience add form"""

    subtitle = _("New cinema audience")
    legend = _("New cinema audience properties")

    content_factory = ICinemaAudience
    fields = Fields(ICinemaAudience).omit('__parent__', '__name__', 'active')

    def add(self, obj):
        ICinemaAudienceContainer(self.context).append(obj)


@adapter_config(required=(ICinemaAudienceContainerTarget, IAdminLayer, CinemaAudienceAddForm),
                provides=IFormTitle)
def cinema_audience_add_form_title(context, request, form):
    """Cinema audience add form title"""
    return TITLE_SPAN.format(
        get_object_label(context, request, form))


@adapter_config(required=(ICinemaAudienceContainerTarget, IAdminLayer, CinemaAudienceAddForm),
                provides=IAJAXFormRenderer)
class CinemaAudienceAddFormRenderer(SimpleAddFormRenderer):
    """Cinema audience add form renderer"""

    table_factory = ICinemaAudiencesTable


@adapter_config(required=(ICinemaAudience, IAdminLayer, Interface),
                provides=IObjectLabel)
def cinema_audience_label(context, request, view):
    """Cinema audience label"""
    return context.name


@adapter_config(required=(ICinemaAudience, IAdminLayer, Interface),
                provides=IObjectHint)
def cinema_audience_hint(context, request, view):
    """Cinema audience hint"""
    return request.localizer.translate(_("Cinema audience"))


@adapter_config(required=(ICinemaAudience, IAdminLayer, ICinemaAudiencesTable),
                provides=ITableElementEditor)
class CinemaAudienceEditor(TableElementEditor):
    """Cinema audience editor"""


@ajax_form_config(name='properties.html',
                  context=ICinemaAudience, layer=IPyAMSLayer,
                  permission=VIEW_THEATER_PERMISSION)
class CinemaAudiencePropertiesEditForm(AdminModalEditForm):
    """Cinema audience properties edit form"""

    legend = _("Cinema audience properties")

    fields = Fields(ICinemaAudience).omit('__parent__', '__name__', 'active')


@adapter_config(required=(ICinemaAudience, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def cinema_audience_edit_form_title(context, request, form):
    """Cinema audience edit form title"""
    translate = request.localizer.translate
    theater = get_parent(context, IMovieTheater)
    return TITLE_SPAN_BREAK.format(
        get_object_label(theater, request, form),
        translate(_("Cinema audience: {}")).format(get_object_label(context, request, form)))


@adapter_config(required=(ICinemaAudience, IAdminLayer, CinemaAudiencePropertiesEditForm),
                provides=IAJAXFormRenderer)
class CinemaAudiencePropertiesEditFormRenderer(SimpleEditFormRenderer):
    """Cinema audience properties edit form renderer"""

    parent_interface = ICinemaAudienceContainerTarget
    table_factory = ICinemaAudiencesTable
