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

from pyams_app_msc.feature.messaging import IMessagingSettings
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='messaging-settings.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=700,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class MessagingSettingsMenu(NavigationMenuItem):
    """Messaging settings menu"""

    label = _("Messaging settings")
    href = '#messaging-settings.html'


@ajax_form_config(name='messaging-settings.html',
                  context=ISiteRoot, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class MessagingSettingsEditForm(AdminEditForm):
    """Messaging settings edit form"""

    title = _("Messaging service settings")
    legend = _("Messaging properties")

    fields = Fields(IMessagingSettings)


@adapter_config(required=(ISiteRoot, IPyAMSLayer, MessagingSettingsEditForm),
                provides=IFormContent)
def site_root_messaging_edit_form_content(context, request, form):
    """Site root messaging edit form content getter"""
    return IMessagingSettings(context)
