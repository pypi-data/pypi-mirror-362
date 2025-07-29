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

__docformat__ = 'restructuredtext'

from zope.interface import Interface, Invalid
from zope.schema import TextLine

from pyams_app_msc import _
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.form import AddForm
from pyams_form.interfaces import HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import PUBLIC_PERMISSION
from pyams_security.interfaces.plugin import IUserRegistrationConfirmationInfo
from pyams_security.interfaces.profile import IUserRegistrationViews
from pyams_security_views.interfaces.login import ILoginConfiguration
from pyams_skin.schema.button import ResetButton, SubmitButton
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility


#
# Password reset request
#

class IPasswordResetInfo(Interface):
    """Password reset information interface"""

    login = TextLine(title=_("User ID"),
                     description=_("Your user ID can be your email address or a custom login"),
                     required=True)


class IPasswordResetButtons(Interface):
    """Password reset buttons"""

    change = SubmitButton(name='change',
                          title=_("Request password reset"))

    reset = ResetButton(name='reset',
                        title=_("Reset"))


@ajax_form_config(name='password-reset.html',
                  layer=IPyAMSLayer)
class PasswordResetForm(AddForm, PortalContextIndexPage):
    """Password reset form"""

    title = _("Password reset")
    legend = _("Enter account")

    fields = Fields(IPasswordResetInfo)
    buttons = Buttons(IPasswordResetButtons)

    _edit_permission = PUBLIC_PERMISSION

    @handler(buttons['change'])
    def handle_change(self, action):
        self.handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        login = data.get('login')
        if not login:
            self.widgets.errors += (Invalid(_("Login is required!")),)
            return
        login_info = ILoginConfiguration(self.request.root)
        if not login_info.allow_password_reset:
            self.widgets.errors += (Invalid(_("Password reset is not allowed!")),)
            return
        sm = get_utility(ISecurityManager)
        users_folder = sm.get(login_info.users_folder)
        user = users_folder.get(login)
        if user is not None:
            user.generate_reset_hash(notify=True, request=self.request)
            return user


@adapter_config(required=(Interface, IPyAMSLayer, PasswordResetForm),
                provides=IAJAXFormRenderer)
class PasswordResetFormRenderer(ContextRequestViewAdapter):
    """Password reset form renderer"""

    def render(self, changes):
        """Form renderer"""
        register_views = self.request.registry.getMultiAdapter((self.context, self.request),
                                                               IUserRegistrationViews)
        return {
            'status': 'redirect',
            'location': register_views.password_reset_final_view
        }


@pagelet_config(name='password-final.html',
                layer=IPyAMSLayer)
@template_config(template='templates/password-final.pt',
                 layer=IPyAMSLayer)
class PasswordResetFinalView(PortalContextIndexPage):
    """Password reset final view"""


#
# Password change
#

class IPasswordChangeButtons(Interface):
    """Password change buttons"""

    change = SubmitButton(name='change',
                          title=_("Change password"))

    reset = ResetButton(name='reset',
                        title=_("Reset"))


@ajax_form_config(name='password-change.html',
                  layer=IPyAMSLayer)
class PasswordChangeForm(AddForm, PortalContextIndexPage):
    """Password change form"""

    title = _("Password change")
    legend = _("Enter account and new password")

    fields = Fields(IUserRegistrationConfirmationInfo)
    buttons = Buttons(IPasswordChangeButtons)

    _edit_permission = PUBLIC_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        hash = self.widgets.get('activation_hash')
        if hash is not None:
            hash.mode = HIDDEN_MODE
            hash.value = self.request.params.get('hash')

    @handler(buttons['change'])
    def handle_change(self, action):
        self.handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        login = data.get('login')
        if not login:
            self.widgets.errors += (Invalid(_("Login is required!")),)
            return
        login_info = ILoginConfiguration(self.request.root)
        if not login_info.allow_password_reset:
            self.widgets.errors += (Invalid(_("Password reset is not allowed!")),)
            return
        sm = get_utility(ISecurityManager)
        users_folder = sm.get(login_info.users_folder)
        user = users_folder.get(login)
        if user is None:
            self.widgets.errors += (Invalid(_("Can't change password with provided arguments!")),)
        else:
            hash = data.get('activation_hash')
            try:
                user.reset_password(hash, data.get('password'))
            except Invalid as exc:
                translate = self.request.localizer.translate
                self.widgets.errors += (Invalid(', '.join(map(translate, exc.args))),)
            else:
                return user


@adapter_config(required=(Interface, IPyAMSLayer, PasswordChangeForm),
                provides=IAJAXFormRenderer)
class PasswordChangeFormRenderer(ContextRequestViewAdapter):
    """Password change form renderer"""

    def render(self, changes):
        """Form renderer"""
        register_views = self.request.registry.getMultiAdapter((self.context, self.request),
                                                               IUserRegistrationViews)
        return {
            'status': 'redirect',
            'location': register_views.password_change_final_view
        }


@pagelet_config(name='password-changed.html',
                layer=IPyAMSLayer)
@template_config(template='templates/password-changed.pt',
                 layer=IPyAMSLayer)
class PasswordChangeFinalView(PortalContextIndexPage):
    """Password change final view"""
