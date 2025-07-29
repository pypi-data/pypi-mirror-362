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

"""PyAMS_app_msc.feature.profile.skin module

"""

from pyramid.authorization import Authenticated
from pyramid.events import subscriber
from zope.interface import Interface, Invalid, alsoProvides, implementer
from zope.schema import Password

from pyams_app_msc.feature.navigation import NavigationMenuItem
from pyams_app_msc.feature.navigation.interfaces import INavigationViewletManager
from pyams_app_msc.feature.profile.interfaces import IUserProfile
from pyams_app_msc.feature.profile.skin.interfaces import IUserProfileView
from pyams_app_msc.skin import IPyAMSMSCLayer
from pyams_content.root import ISiteRootInfos
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.form import AddForm, EditForm
from pyams_form.interfaces import HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent, IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_mail.interfaces import IPrincipalMailInfo
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import MANAGE_PERMISSION
from pyams_security.interfaces.names import ADMIN_USER_ID, INTERNAL_USER_ID
from pyams_security.interfaces.plugin import ILocalUser, check_password
from pyams_skin.schema.button import ResetButton, SubmitButton
from pyams_template.template import layout_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.registry import get_utility
from pyams_viewlet.viewlet import viewlet_config

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class UserMenu(NavigationMenuItem):
    """Base user menu"""

    href = None

    @property
    def css_class(self):
        return 'selected' if self.request.view_name == self.href else ''


@layout_config(template='templates/profile-layout.pt',
               layer=IPyAMSMSCLayer)
class ProfileContextIndexPage(PortalContextIndexPage):
    """Profile context index page"""


@viewlet_config(name='user-profile.menu',
                layer=IPyAMSMSCLayer, view=IUserProfileView,
                manager=INavigationViewletManager, weight=10)
class UserProfileMenu(UserMenu):
    """User profile menu"""

    label = _("My profile")
    href = 'my-profile.html'


@ajax_form_config(name='my-profile.html',
                  layer=IPyAMSLayer)
@implementer(IUserProfileView)
class UserProfileEditForm(EditForm, ProfileContextIndexPage):
    """User profile edit form"""

    title = _("My user profile")
    legend = _("Account settings")

    fields = Fields(IUserProfile).omit('active')
    _edit_permission = MANAGE_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        principal_id = self.request.principal.id
        principal_widget = self.widgets.get('principal_id')
        if principal_widget is not None:
            principal_widget.mode = HIDDEN_MODE
            principal_widget.value = principal_id
        phone_number = self.widgets.get('phone_number')
        if phone_number is not None:
            phone_number.object_data = {
                'input-mask': '[+9{3}] [9]9 99 99 99 99'
            }
            alsoProvides(phone_number, IObjectData)
        email = self.widgets.get('email')
        if email is not None:
            email.readonly = 'readonly'
            if not email.value:
                if principal_id in (ADMIN_USER_ID, INTERNAL_USER_ID):
                    infos = ISiteRootInfos(self.request.root)
                    email.value = infos.support_email
                else:
                    sm = get_utility(ISecurityManager)
                    principal_info = sm.get_principal(principal_id, info=False)
                    if principal_info is not None:
                        mail_info = IPrincipalMailInfo(principal_info, None)
                        if mail_info is not None:
                            _title, principal_email = next(mail_info.get_addresses())
                            email.value = principal_email

    def update_actions(self):
        super().update_actions()
        action = self.actions.get('apply')
        if action is not None:
            action.add_class('btn-primary')


@adapter_config(required=(Interface, IPyAMSLayer, UserProfileEditForm),
                provides=IFormContent)
def user_profile_edit_form_content(context, request, form):
    """User profile edit form content getter"""
    return IUserProfile(request)


#
# User password change form
#

@viewlet_config(name='user-password.menu',
                layer=IPyAMSMSCLayer, view=IUserProfileView,
                manager=INavigationViewletManager, weight=20)
class UserPasswordMenu(UserMenu):
    """User password menu"""

    label = _("My password")
    href = 'my-password.html'

    def __new__(cls, context, request, view, manager):
        identity = request.identity
        if (identity is None) or (Authenticated not in identity.get('principals', ())):
            return None
        sm = get_utility(ISecurityManager)
        principal = sm.get_raw_principal(request.principal.id)
        if not ILocalUser.providedBy(principal):
            return None
        return NavigationMenuItem.__new__(cls)


class IUserPasswordEditFormFields(IUserProfile):
    """User password change form fields interface"""

    old_password = Password(title=_("Old password"),
                            required=True)

    new_password = Password(title=_("New password"),
                            min_length=8,
                            required=True)

    confirmed_password = Password(title=_("Confirmed new password"),
                                  min_length=8,
                                  required=True)


class IUserPasswordEditFormButtons(Interface):
    """User password edit form buttons interface"""

    change = SubmitButton(name='change',
                          title=_("Change password"))

    reset = ResetButton(name='reset',
                        title=_("Reset"))


@ajax_form_config(name='my-password.html',
                  layer=IPyAMSLayer)
@implementer(IUserProfileView)
class UserPasswordEditForm(AddForm, ProfileContextIndexPage):
    """User password change form"""

    title = _("My password")
    legend = _("Change password")

    fields = Fields(IUserPasswordEditFormFields).select('principal_id', 'old_password',
                                                        'new_password', 'confirmed_password')
    buttons = Buttons(IUserPasswordEditFormButtons)

    _edit_permission = MANAGE_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        principal_id = self.request.principal.id
        principal_widget = self.widgets.get('principal_id')
        if principal_widget is not None:
            principal_widget.mode = HIDDEN_MODE
            principal_widget.value = principal_id

    def update_actions(self):
        super().update_actions()
        change = self.actions.get('change')
        if change is not None:
            change.add_class('btn-primary')

    @handler(buttons['change'])
    def handle_change(self, action):
        super().handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        sm = get_utility(ISecurityManager)
        principal = sm.get_raw_principal(data.get('principal_id'))
        if ILocalUser.providedBy(principal):
            principal.password = data['new_password']
            return principal


@adapter_config(required=(Interface, IPyAMSLayer, UserPasswordEditForm),
                provides=IFormContent)
def user_password_edit_form_content(context, request, form):
    """User password edit form content getter"""
    return IUserProfile(request)


@subscriber(IDataExtractedEvent, form_selector=UserPasswordEditForm)
def extract_user_password_form_data(event):
    """Check new local user password data"""
    data = event.data
    principal_id = data.get('principal_id')
    sm = get_utility(ISecurityManager)
    principal = sm.get_raw_principal(principal_id)
    if not ILocalUser.providedBy(principal):
        event.form.widgets.errors += (Invalid(_("Can't find local principal!")),)
        return
    if not principal.check_password(data.get('old_password')):
        event.form.widgets.errors += (Invalid(_("Wrong current password!")),)
    new_password = data.get('new_password')
    if new_password:
        try:
            check_password(new_password)
        except Invalid as ex:
            event.form.widgets.errors += (ex,)
        if new_password != data.get('confirmed_password'):
            event.form.widgets.errors += (Invalid(_("User password was not confirmed correctly.")),)
        else:
            del data['confirmed_password']


@adapter_config(required=(Interface, IPyAMSLayer, UserPasswordEditForm),
                provides=IAJAXFormRenderer)
class UserPasswordEditFormRenderer(ContextRequestViewAdapter):
    """User password edit form renderer"""

    def render(self, changes):
        if changes is None:
            return {
                'status': 'reload'
            }
        return {
            'status': 'success',
            'message': self.request.localizer.translate(_("Your password was changed successfully."))
        }
