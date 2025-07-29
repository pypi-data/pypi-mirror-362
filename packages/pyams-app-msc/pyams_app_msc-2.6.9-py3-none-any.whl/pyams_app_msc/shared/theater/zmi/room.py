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
from pyams_app_msc.shared.theater import ICinemaRoomContainer, ICinemaRoomContainerTarget
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.room import ICinemaRoom
from pyams_app_msc.shared.theater.zmi.interfaces import ICinemaRoomsTable
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
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectLabel
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IPropertiesMenu, IToolbarViewletManager
from pyams_zmi.table import AttributeSwitcherColumn, NameColumn, ReorderColumn, SortableTable, TableAdminView, \
    TableElementEditor, TrashColumn
from pyams_zmi.utils import get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='cinema-rooms.menu',
                context=ICinemaRoomContainerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=520,
                permission=VIEW_THEATER_PERMISSION)
class CinemaRoomsMenu(NavigationMenuItem):
    """Cinema rooms menu"""

    label = _("Cinema rooms")
    href = '#cinema-rooms.html'


@factory_config(ICinemaRoomsTable)
class CinemaRoomsTable(SortableTable):
    """Cinema rooms table"""

    container_class = ICinemaRoomContainer

    display_if_empty = True


@adapter_config(required=(ICinemaRoomContainerTarget, IAdminLayer, ICinemaRoomsTable),
                provides=IValues)
class CinemaRoomsTableValues(ContextRequestViewAdapter):
    """Cinema rooms table values adapter"""

    @property
    def values(self):
        """Cinema rooms values getter"""
        yield from ICinemaRoomContainer(self.context).values()


@adapter_config(name='reorder',
                required=(ICinemaRoomContainerTarget, IAdminLayer, ICinemaRoomsTable),
                provides=IColumn)
class CinemaRoomTableReorderColumn(ReorderColumn):
    """Cinema rooms table reorder column"""


@view_config(name='reorder.json',
             context=ICinemaRoomContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_THEATER_PERMISSION)
def reorder_cinema_rooms_table(request):
    """Reorder cinema rooms table"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='active',
                required=(ICinemaRoomContainerTarget, IAdminLayer, ICinemaRoomsTable),
                provides=IColumn)
class CinemaRoomsActiveColumn(AttributeSwitcherColumn):
    """Cinema rooms table active column"""

    attribute_name = 'active'
    attribute_switcher = 'switch-active-room.json'

    icon_off_class = 'far fa-eye-slash text-danger'

    permission = MANAGE_THEATER_PERMISSION
    weight = 1

    def get_icon_hint(self, item):
        """Icon hint getter"""
        if self.has_permission(item):
            hint = _("Click icon to switch room activity")
        elif item.active:
            hint = _("This room is active")
        else:
            hint = _("This room is not active")
        return self.request.localizer.translate(hint)


@view_config(name='switch-active-room.json',
             context=ICinemaRoomContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_active_room(request):
    """Switch cinema room activity flag"""
    return switch_element_attribute(request, container_factory=ICinemaRoomContainer)


@adapter_config(name='label',
                required=(ICinemaRoomContainerTarget, IAdminLayer, ICinemaRoomsTable),
                provides=IColumn)
class CinemaRoomLabelColumn(NameColumn):
    """Cinema rooms table label column"""

    attr_name = 'name'
    i18n_header = _("Room name")


@adapter_config(name='trash',
                required=(ICinemaRoomContainerTarget, IAdminLayer, ICinemaRoomsTable),
                provides=IColumn)
class CinemaRoomTrashColumn(TrashColumn):
    """Cinema rooms table trash column"""

    object_data = {
        'ams-modules': 'container',
        'ams-delete-target': 'delete-cinema-room.json'
    }


@view_config(name='delete-cinema-room.json',
             context=ICinemaRoomContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_THEATER_PERMISSION)
def delete_cinema_room(request):
    """Delete cinema room"""
    return delete_container_element(request, container_factory=ICinemaRoomContainer)


@pagelet_config(name='cinema-rooms.html',
                context=ICinemaRoomContainerTarget, layer=IPyAMSLayer,
                permission=VIEW_THEATER_PERMISSION)
class CinemaRoomsView(TableAdminView):
    """Cinema rooms view"""

    title = _("Cinema rooms")

    table_class = ICinemaRoomsTable
    table_label = _("Cinema rooms list")


#
# Cinema rooms components
#

@viewlet_config(name='add-cinema-room.action',
                context=ICinemaRoomContainerTarget, layer=IAdminLayer, view=ICinemaRoomsTable,
                manager=IToolbarViewletManager, weight=20,
                permission=MANAGE_THEATER_PERMISSION)
class CinemaRoomAddAction(ContextAddAction):
    """Cinema room add action"""

    label = _("Add room")
    href = 'add-cinema-room.html'


@ajax_form_config(name='add-cinema-room.html',
                  context=ICinemaRoomContainerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_THEATER_PERMISSION)
class CinemaRoomAddForm(AdminModalAddForm):
    """Cinema room add form"""

    subtitle = _("New cinema room")
    legend = _("New cinema room properties")

    content_factory = ICinemaRoom
    fields = Fields(ICinemaRoom).omit('__parent__', '__name__', 'active')

    def add(self, obj):
        ICinemaRoomContainer(self.context).append(obj)


@adapter_config(required=(ICinemaRoomContainerTarget, IAdminLayer, CinemaRoomAddForm),
                provides=IFormTitle)
def cinema_room_add_form_title(context, request, form):
    return '<span class="tiny">{}</span>'.format(
        get_object_label(context, request, form))


@adapter_config(required=(ICinemaRoomContainerTarget, IAdminLayer, CinemaRoomAddForm),
                provides=IAJAXFormRenderer)
class CinemaRoomAddFormRenderer(SimpleAddFormRenderer):
    """Cinema room add form renderer"""

    table_factory = ICinemaRoomsTable


@adapter_config(required=(ICinemaRoom, IAdminLayer, Interface),
                provides=IObjectLabel)
def cinema_room_label(context, request, view):
    """Cinema room label"""
    return context.name


@adapter_config(required=(ICinemaRoom, IAdminLayer, Interface),
                provides=IObjectHint)
def cinema_room_hint(context, request, view):
    """Cinema room hint"""
    return request.localizer.translate(_("Cinema room"))


@adapter_config(required=(ICinemaRoom, IAdminLayer, ICinemaRoomsTable),
                provides=ITableElementEditor)
class CinemaRoomEditor(TableElementEditor):
    """Cinema room editor"""


@ajax_form_config(name='properties.html',
                  context=ICinemaRoom, layer=IPyAMSLayer,
                  permission=VIEW_THEATER_PERMISSION)
class CinemaRoomPropertiesEditForm(AdminModalEditForm):
    """Cinema room properties edit form"""

    legend = _("Cinema room properties")

    fields = Fields(ICinemaRoom).omit('__parent__', '__name__', 'active')


@adapter_config(required=(ICinemaRoom, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def cinema_room_edit_form_title(context, request, form):
    translate = request.localizer.translate
    theater = get_parent(context, IMovieTheater)
    return '<span class="tiny">{}</span><br />{}'.format(
        get_object_label(theater, request, form),
        translate(_("Cinema room: {}")).format(get_object_label(context, request, form)))


@adapter_config(required=(ICinemaRoom, IAdminLayer, CinemaRoomPropertiesEditForm),
                provides=IAJAXFormRenderer)
class CinemaRoomPropertiesEditFormRenderer(SimpleEditFormRenderer):
    """Cinema room properties edit form renderer"""

    parent_interface = ICinemaRoomContainerTarget
    table_factory = ICinemaRoomsTable
