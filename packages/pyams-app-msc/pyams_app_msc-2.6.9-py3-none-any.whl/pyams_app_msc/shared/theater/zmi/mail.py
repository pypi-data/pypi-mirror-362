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

from zope.interface import Interface

from pyams_app_msc.interfaces import MANAGE_THEATER_PERMISSION
from pyams_app_msc.shared.theater import IMailTemplatesTarget
from pyams_app_msc.shared.theater.interfaces.mail import IMailTemplates
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='mail-templates.menu',
                context=IMailTemplatesTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=590,
                permission=MANAGE_THEATER_PERMISSION)
class MailTemplatesMenu(NavigationMenuItem):
    """Mail templates menu"""

    label = _("Mail templates")
    href = '#mail-templates.html'


@ajax_form_config(name='mail-templates.html',
                  context=IMailTemplatesTarget, layer=IPyAMSLayer,
                  permission=MANAGE_THEATER_PERMISSION)
class MailTemplatesEditForm(AdminEditForm):
    """Mail templates edit form"""

    title = _("Movie theater mail templates")
    legend = _("Mail templates")

    fields = Fields(Interface)


@adapter_config(name='main',
                context=(IMailTemplatesTarget, IAdminLayer, MailTemplatesEditForm),
                provides=IGroup)
class MailTemplatesMainGroup(Group):
    """Mail templates main group"""

    legend = _("Messages management")
    fields = Fields(IMailTemplates).select('send_copy_to_sender')

    weight = 0


@adapter_config(name='cancel',
                required=(IMailTemplatesTarget, IAdminLayer, MailTemplatesEditForm),
                provides=IGroup)
class MailTemplatesCancelGroup(Group):
    """Mail templates cancel group"""

    legend = _("Cancelled booking")
    fields = Fields(IMailTemplates).select('cancel_subject', 'cancel_template')

    weight = 10


@adapter_config(name='refuse',
                required=(IMailTemplatesTarget, IAdminLayer, MailTemplatesEditForm),
                provides=IGroup)
class MailTemplatesRefuseGroup(Group):
    """Mail templates refuse group"""

    legend = _("Refused booking")
    fields = Fields(IMailTemplates).select('refuse_subject', 'refuse_template')

    weight = 20


@adapter_config(name='option',
                required=(IMailTemplatesTarget, IAdminLayer, MailTemplatesEditForm),
                provides=IGroup)
class MailTemplatesOptionGroup(Group):
    """Mail templates option group"""

    legend = _("Booking accepted 'in option'")
    fields = Fields(IMailTemplates).select('option_subject', 'option_template')

    weight = 30


@adapter_config(name='accept',
                required=(IMailTemplatesTarget, IAdminLayer, MailTemplatesEditForm),
                provides=IGroup)
class MailTemplatesAcceptGroup(Group):
    """Mail templates accept group"""

    legend = _("Accepted booking")
    fields = Fields(IMailTemplates).select('accept_subject', 'accept_template')

    weight = 40


@adapter_config(name='update',
                required=(IMailTemplatesTarget, IAdminLayer, MailTemplatesEditForm),
                provides=IGroup)
class MailTemplatesUpdateGroup(Group):
    """Mail templates update group"""

    legend = _("Updated booking")
    fields = Fields(IMailTemplates).select('update_subject', 'update_template')

    weight = 50


@adapter_config(name='reminder',
                required=(IMailTemplatesTarget, IAdminLayer, MailTemplatesEditForm),
                provides=IGroup)
class MailTemplatesReminderGroup(Group):
    """Mail templates reminder group"""

    legend = _("Booking reminder")
    fields = Fields(IMailTemplates).select('reminder_subject', 'reminder_template')

    weight = 60


@viewlet_config(name='mail-templates.help',
                context=IMailTemplatesTarget, layer=IAdminLayer, view=MailTemplatesEditForm,
                manager=IFormHeaderViewletManager, weight=10)
class MailTemplatesEditFormHelp(AlertMessage):
    """Mail templates edit form help"""

    message_renderer = 'markdown'
    _message = _("""Mail templates can include spaces for predefined variables, including:

 - {theater_name}: theater name
 - {theater_address}: theater postal address
 - {theater_email}: theater email address
 - {theater_phone}: theater phone number
 - {theater_logo}: theater logo image
 - {sender_name}: sender name
 - {sender_email}: sender email address
 - {sender_phone}: sender phone number
 - {contact_name}: audience contact name
 - {contact_email}: audience contact email address
 - {contact_phone}: audience contact phone number
 - {booking_date}: booking date
 - {session}: session full label
 - {session_title}: session activity title
 - {session_date}: session date
 - {{session_date}}: new session date (used only after booking update)
""")
