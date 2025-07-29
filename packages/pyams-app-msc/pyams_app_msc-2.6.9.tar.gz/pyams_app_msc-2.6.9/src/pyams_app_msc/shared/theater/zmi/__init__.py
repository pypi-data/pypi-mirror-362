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

from pyramid.events import subscriber
from zope.interface import Interface, Invalid

from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_app_msc.shared.theater import IMovieTheater, IMovieTheaterSettings
from pyams_app_msc.shared.theater.interfaces import BOOKING_CANCEL_MODE
from pyams_content.interfaces import IBaseContent, MANAGE_SITE_TREE_PERMISSION
from pyams_content.root.zmi.sites import SiteRootSitesTable
from pyams_content.zmi.properties import PropertiesEditForm
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent, IFormContent, IGroup
from pyams_i18n.interfaces import II18n, INegotiator
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_skin.interfaces.viewlet import IBreadcrumbItem
from pyams_skin.viewlet.breadcrumb import BreadcrumbItem
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_table.interfaces import ITable
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.unicode import translate_string
from pyams_utils.url import absolute_url
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, AdminModalAddForm, FormGroupChecker
from pyams_zmi.helper.event import get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IMenuHeader, IPropertiesMenu, \
    ISiteManagementMenu
from pyams_zmi.table import TableElementEditor
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='add-movie-theater.divider',
                context=ISiteRoot, layer=IAdminLayer, view=SiteRootSitesTable,
                manager=IContextAddingsViewletManager, weight=109,
                permission=MANAGE_SITE_TREE_PERMISSION)
class MovieTheaterAddMenuDivider(MenuDivider):
    """Movie theater add menu divider"""


@viewlet_config(name='add-movie-theater.menu',
                context=ISiteRoot, layer=IAdminLayer, view=SiteRootSitesTable,
                manager=IContextAddingsViewletManager, weight=110,
                permission=MANAGE_SITE_TREE_PERMISSION)
class MovieTheaterAddMenu(MenuItem):
    """Movie theater add menu"""

    label = _("Add movie theater")
    icon_class = 'fas fa-hotel'

    href = 'add-movie-theater.html'
    modal_target = True


@ajax_form_config(name='add-movie-theater.html',
                  context=ISiteRoot, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_TREE_PERMISSION)
class MovieTheaterAddForm(AdminModalAddForm):
    """Movie theater add form"""

    title = _("Add theater")
    legend = _("New theater properties")

    fields = Fields(IMovieTheater).select('title', 'short_name')
    content_factory = IMovieTheater

    _edit_permission = MANAGE_SITE_TREE_PERMISSION

    def add(self, obj):
        short_name = II18n(obj).query_attribute('short_name', request=self.request)
        name = translate_string(short_name, force_lower=True, spaces='-')
        self.context[name] = obj


@subscriber(IDataExtractedEvent, form_selector=MovieTheaterAddForm)
def handle_new_movie_theater_data(event):
    """Handle new movie theater data"""
    data = event.data
    negotiator = get_utility(INegotiator)
    name = data.get('short_name', {}).get(negotiator.server_language)
    if not name:
        event.form.widgets.errors += (Invalid(_("Movie theater name is required!")),)
    else:
        name = translate_string(name, force_lower=True, spaces='-')
        if name in event.form.context:
            event.form.widgets.errors += (Invalid(_("A movie theater is already registered "
                                                    "with this name!")),)


@adapter_config(required=(ISiteRoot, IAdminLayer, MovieTheaterAddForm),
                provides=IAJAXFormRenderer)
class MovieTheaterAddFormRenderer(ContextRequestViewAdapter):
    """Movie theater add form renderer"""

    def render(self, changes):
        if changes is None:
            return None
        return {
            'status': 'redirect',
            'location': absolute_url(changes, self.request, 'admin')
        }


@adapter_config(required=(IMovieTheater, IPyAMSLayer),
                provides=IObjectLabel)
@adapter_config(required=(IMovieTheater, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def movie_theater_label(context, request, view=None):
    """Movie theater table element name"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=(IMovieTheater, IAdminLayer, ITable),
                provides=ITableElementEditor)
class MovieTheaterTableElementEditor(TableElementEditor):
    """Movie theater table element editor"""

    view_name = 'admin'
    modal_target = False


@adapter_config(required=(IMovieTheater, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class MovieTheaterBreadcrumbs(BreadcrumbItem):
    """Movie theater breadcrumb item"""

    @property
    def label(self):
        return II18n(self.context).query_attribute('short_name', request=self.request)

    css_class = 'breadcrumb-item persistent strong'
    view_name = 'admin'


@adapter_config(required=(IMovieTheater, IAdminLayer, Interface, ISiteManagementMenu),
                provides=IMenuHeader)
def movie_theater_management_menu_header(context, request, view, manager):
    """Movie theater management menu header adapter"""
    return _("Theater management")


@viewletmanager_config(name='properties.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=ISiteManagementMenu, weight=10,
                       provides=IPropertiesMenu,
                       permission=VIEW_SYSTEM_PERMISSION)
class MovieTheaterPropertiesMenu(NavigationMenuItem):
    """Movie theater properties menu"""

    label = _("Properties")
    icon_class = 'fas fa-edit'
    href = '#properties.html'


@ajax_form_config(name='properties.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class MovieTheaterPropertiesEditForm(PropertiesEditForm):
    """Movie theater properties edit form"""

    title = _("Movie theater properties")
    legend = _("Main theater properties")

    fields = Fields(IMovieTheater).select('title', 'short_name', 'header', 'description',
                                          'shared_content_workflow', 'logo', 'notepad',
                                          'address', 'banking_account', 'admin_info')


@adapter_config(name='theater-contacts',
                required=(IMovieTheater, IAdminLayer, MovieTheaterPropertiesEditForm),
                provides=IGroup)
class MovieTheaterPropertiesEditFormContactGroup(Group):
    """Movie theater contact group"""

    legend = _("Contacts")

    fields = Fields(IMovieTheater).select('web_address', 'contact_email', 'phone_number')
    weight = 1


@adapter_config(required=(IMovieTheater, IAdminLayer, MovieTheaterPropertiesEditForm),
                provides=IAJAXFormRenderer)
class MovieTheaterPropertiesEditFormRenderer(AJAXFormRenderer):
    """Movie theater properties edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        if 'title' in changes.get(IBaseContent, ()):
            return {
                'status': 'reload',
                'message': self.request.localizer.translate(self.form.success_message)
            }
        return super().render(changes)


#
# Movie theater settings edit form
#

@viewletmanager_config(name='settings.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=IPropertiesMenu, weight=510,
                       permission=VIEW_SYSTEM_PERMISSION)
class MovieTheaterSettingsMenu(NavigationMenuItem):
    """Movie theater settings menu"""

    label = _("Settings")
    href = '#settings.html'


@ajax_form_config(name='settings.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class MovieTheaterSettingsEditForm(AdminEditForm):
    """Movie theater settings edit form"""

    title = _("Movie theater settings")
    legend = _("Main theater settings")

    fields = Fields(IMovieTheaterSettings).select('calendar_first_day',
                                                  'calendar_slot_duration',
                                                  'default_session_duration',
                                                  'session_duration_delta')


@adapter_config(required=(IMovieTheater, IPyAMSLayer, MovieTheaterSettingsEditForm),
                provides=IFormContent)
def movie_theater_settings_edit_form_content(context, request, form):
    """Movie theater settings edit form content getter"""
    return IMovieTheaterSettings(context)


@adapter_config(name='',
                required=(IMovieTheater, IAdminLayer, MovieTheaterSettingsEditForm),
                provides=IGroup)
class MovieTheaterSettingsBookingGroup(Group):
    """Movie theater settings booking group"""

    legend = _("Booking settings")

    fields = Fields(IMovieTheaterSettings).select('reminder_delay',
                                                  'booking_retention_duration')
    weight = 10


@adapter_config(name='session-request-mode.group',
                required=(IMovieTheater, IAdminLayer, MovieTheaterSettingsEditForm),
                provides=IGroup)
class MovieTheaterSettingsSessionRequestModeGroup(FormGroupChecker):
    """Movie theater settings session request mode group"""

    fields = Fields(IMovieTheaterSettings).select('allow_session_request',
                                                  'session_request_mode')
    weight = 15


@adapter_config(name='booking-cancel-mode.group',
                required=(IMovieTheater, IAdminLayer, MovieTheaterSettingsEditForm),
                provides=IGroup)
class MovieTheaterSettingsBookingCancelModeGroup(Group):
    """Movie theater settings booking cancel mode"""

    legend = _("Booking cancel mode")

    fields = Fields(IMovieTheaterSettings).select('booking_cancel_mode',
                                                  'booking_cancel_max_delay',
                                                  'booking_cancel_notice_period')
    weight = 20


@subscriber(IDataExtractedEvent, form_selector=MovieTheaterSettingsBookingCancelModeGroup)
def handle_booking_cancel_mode(event):
    """Handle booking cancel mode"""
    data = event.data
    if (data.get('booking_cancel_mode') == BOOKING_CANCEL_MODE.MAX_DELAY.value) and \
            (not data.get('booking_cancel_max_delay')):
        event.form.widgets.errors += (Invalid(_("Cancel max delay must be set in \"max delay\" mode!")),)
    if (data.get('booking_cancel_mode') == BOOKING_CANCEL_MODE.NOTICE_PERIOD.value) and \
            (not data.get('booking_cancel_notice_period')):
        event.form.widgets.errors += (Invalid(_("Cancel notice period must be set in \"notice period\" mode!")),)


@adapter_config(name='quotations.group',
                required=(IMovieTheater, IAdminLayer, MovieTheaterSettingsEditForm),
                provides=IGroup)
class MovieTheaterSettingsQuotationsGroup(Group):
    """Movie theater quotations settings group"""

    legend = _("Quotations settings")

    fields = Fields(IMovieTheaterSettings).select('quotation_number_format', 'quotation_email',
                                                  'quotation_logo', 'quotation_color',
                                                  'currency', 'vat_rate')
    weight = 30


@adapter_config(required=(IMovieTheater, IAdminLayer, MovieTheaterSettingsQuotationsGroup),
                provides=IAJAXFormRenderer)
class MovieTheaterSettingsQuotationsGroupRenderer(AJAXFormRenderer):
    """Movie theater quotations settings group renderer"""

    def render(self, changes):
        result = super().render(changes)
        if 'quotation_logo' in changes.get(IMovieTheaterSettings, ()):
            result.setdefault('callbacks', []).append(
                get_json_widget_refresh_callback(self.form, 'quotation_logo', self.request))
        return result
