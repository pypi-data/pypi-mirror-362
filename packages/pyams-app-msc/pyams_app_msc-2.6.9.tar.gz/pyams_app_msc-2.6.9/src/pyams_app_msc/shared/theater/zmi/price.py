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

from pyramid.decorator import reify
from pyramid.view import view_config
from zope.interface import Interface

from pyams_app_msc.interfaces import MANAGE_THEATER_PERMISSION, VIEW_THEATER_PERMISSION
from pyams_app_msc.shared.theater import ICinemaPriceContainerTarget
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.price import ICinemaPrice, ICinemaPriceContainer
from pyams_app_msc.shared.theater.zmi.interfaces import ICinemaPricesTable
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


@viewlet_config(name='cinema-prices.menu',
                context=ICinemaPriceContainerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=525,
                permission=VIEW_THEATER_PERMISSION)
class CinemaPricesMenu(NavigationMenuItem):
    """Cinema prices menu"""

    label = _("Cinema prices")
    href = '#cinema-prices.html'


@factory_config(ICinemaPricesTable)
class CinemaPricesTable(SortableTable):
    """Cinema prices table"""

    container_class = ICinemaPriceContainer

    display_if_empty = True


@adapter_config(required=(ICinemaPriceContainerTarget, IAdminLayer, ICinemaPricesTable),
                provides=IValues)
class CinemaPricesTableValues(ContextRequestViewAdapter):
    """Cinema prices table values adapter"""

    @property
    def values(self):
        """Cinema prices values getter"""
        yield from ICinemaPriceContainer(self.context).values()


@adapter_config(name='reorder',
                required=(ICinemaPriceContainerTarget, IAdminLayer, ICinemaPricesTable),
                provides=IColumn)
class CinemaPricesTableReorderColumn(ReorderColumn):
    """Cinema price table reorder column"""


@view_config(name='reorder.json',
             context=ICinemaPriceContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_THEATER_PERMISSION)
def reorder_cinema_prices_table(request):
    """Reorder cinema price table"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='active',
                required=(ICinemaPriceContainerTarget, IAdminLayer, ICinemaPricesTable),
                provides=IColumn)
class CinemaPricesActiveColumn(AttributeSwitcherColumn):
    """Cinema prices table active column"""

    attribute_name = 'active'
    attribute_switcher = 'switch-active-price.json'

    icon_off_class = 'far fa-eye-slash text-danger'

    permission = MANAGE_THEATER_PERMISSION
    weight = 1

    def get_icon_hint(self, item):
        """Icon hint getter"""
        if self.has_permission(item):
            hint = _("Click icon to switch price activity")
        elif item.active:
            hint = _("This price is active")
        else:
            hint = _("This price is not active")
        return self.request.localizer.translate(hint)


@view_config(name='switch-active-price.json',
             context=ICinemaPriceContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_active_price(request):
    """Switch cinema price activity flag"""
    return switch_element_attribute(request, container_factory=ICinemaPriceContainer)


@adapter_config(name='label',
                required=(ICinemaPriceContainerTarget, IAdminLayer, ICinemaPricesTable),
                provides=IColumn)
class CinemaPriceLabelColumn(NameColumn):
    """Cinema prices table label column"""

    attr_name = 'name'
    i18n_header = _("Price name")


@adapter_config(name='trash',
                required=(ICinemaPriceContainerTarget, IAdminLayer, ICinemaPricesTable),
                provides=IColumn)
class CinemaPriceTrashColumn(TrashColumn):
    """Cinema prices table trash column"""

    object_data = {
        'ams-modules': 'container',
        'ams-delete-target': 'delete-cinema-price.json'
    }


@view_config(name='delete-cinema-price.json',
             context=ICinemaPriceContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_THEATER_PERMISSION)
def delete_cinema_price(request):
    """Delete cinema price"""
    return delete_container_element(request, container_factory=ICinemaPriceContainer)


@pagelet_config(name='cinema-prices.html',
                context=ICinemaPriceContainerTarget, layer=IPyAMSLayer,
                permission=VIEW_THEATER_PERMISSION)
class CinemaPricesView(TableAdminView):
    """Cinema prices view"""

    title = _("Cinema prices")

    table_class = ICinemaPricesTable
    table_label = _("Cinema prices list")


#
# Cinema prices components
#

@viewlet_config(name='add-cinema-price.action',
                context=ICinemaPriceContainerTarget, layer=IAdminLayer, view=ICinemaPricesTable,
                manager=IToolbarViewletManager, weight=20,
                permission=MANAGE_THEATER_PERMISSION)
class CinemaPriceAddAction(ContextAddAction):
    """Cinema price add action"""

    label = _("Add price")
    href = 'add-cinema-price.html'


@ajax_form_config(name='add-cinema-price.html',
                  context=ICinemaPriceContainerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_THEATER_PERMISSION)
class CinemaPriceAddForm(AdminModalAddForm):
    """Cinema price add form"""

    subtitle = _("New cinema price")
    legend = _("New cinema price properties")

    content_factory = ICinemaPrice
    fields = Fields(ICinemaPrice).omit('__parent__', '__name__', 'active')

    def add(self, obj):
        ICinemaPriceContainer(self.context).append(obj)


@adapter_config(required=(ICinemaPriceContainerTarget, IAdminLayer, CinemaPriceAddForm),
                provides=IFormTitle)
def cinema_price_add_form_title(context, request, form):
    """Cinema price add form title"""
    return '<span class="tiny">{}</span>'.format(
        get_object_label(context, request, form))


@adapter_config(required=(ICinemaPriceContainerTarget, IAdminLayer, CinemaPriceAddForm),
                provides=IAJAXFormRenderer)
class CinemaPriceAddFormRenderer(SimpleAddFormRenderer):
    """Cinema price add form renderer"""

    table_factory = ICinemaPricesTable


@adapter_config(required=(ICinemaPrice, IAdminLayer, Interface),
                provides=IObjectLabel)
def cinema_price_label(context, request, view):
    """Cinema price label"""
    return context.name


@adapter_config(required=(ICinemaPrice, IAdminLayer, Interface),
                provides=IObjectHint)
def cinema_price_hint(context, request, view):
    """Cinema price hint"""
    return request.localizer.translate(_("Cinema price"))


@adapter_config(required=(ICinemaPrice, IAdminLayer, ICinemaPricesTable),
                provides=ITableElementEditor)
class CinemaPriceEditor(TableElementEditor):
    """Cinema price editor"""


@ajax_form_config(name='properties.html',
                  context=ICinemaPrice, layer=IPyAMSLayer,
                  permission=VIEW_THEATER_PERMISSION)
class CinemaPricePropertiesEditForm(AdminModalEditForm):
    """Cinema price properties edit form"""

    legend = _("Cinema price properties")

    fields = Fields(ICinemaPrice).omit('__parent__', '__name__', 'active')


@adapter_config(required=(ICinemaPrice, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def cinema_price_edit_form_title(context, request, form):
    translate = request.localizer.translate
    theater = get_parent(context, IMovieTheater)
    return '<span class="tiny">{}</span><br />{}'.format(
        get_object_label(theater, request, form),
        translate(_("Cinema price: {}")).format(get_object_label(context, request, form)))


@adapter_config(required=(ICinemaPrice, IAdminLayer, CinemaPricePropertiesEditForm),
                provides=IAJAXFormRenderer)
class CinemaPricePropertiesEditFormRenderer(SimpleEditFormRenderer):
    """Cinema price properties edit form renderer"""

    parent_interface = ICinemaPriceContainerTarget
    table_factory = ICinemaPricesTable
