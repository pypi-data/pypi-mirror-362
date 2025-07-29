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
from pyramid.httpexceptions import HTTPBadRequest
from zope.annotation.interfaces import IAnnotations
from zope.interface import Interface, Invalid, alsoProvides
from zope.schema import TextLine

from pyams_app_msc.feature.profile.interfaces import ActivatedPrincipalEvent, IUserProfile, \
    RegisteredPrincipalEvent, USER_PROFILE_KEY
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.form import AddForm
from pyams_form.interfaces import HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import IPrincipalInfo, PUBLIC_PERMISSION
from pyams_security.interfaces.plugin import ILocalUser, \
    IUserRegistrationConfirmationInfo as IUserRegistrationConfirmationInfoBase, LOCKED_ACCOUNT_PASSWORD
from pyams_security.interfaces.profile import IUserRegistrationViews
from pyams_security_views.interfaces.login import ILoginConfiguration
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.schema.button import ResetButton, SubmitButton
from pyams_skin.viewlet.help import AlertMessage
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import create_object
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.registry import get_utility
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@adapter_config(required=(Interface, IPyAMSLayer),
                provides=IUserRegistrationViews)
class UserRegistrationViews(ContextRequestAdapter):
    """User registration view getter"""

    @property
    def register_view(self):
        return absolute_url(self.context, self.request, 'register.html')

    @property
    def register_ok_view(self):
        return absolute_url(self.context, self.request, 'register-ok.html')

    @property
    def register_confirm_view(self):
        return absolute_url(self.context, self.request, 'register-confirm.html')

    @property
    def register_confirm_delay(self):
        configuration = ILoginConfiguration(self.request.root, None)
        if configuration is not None:
            return configuration.activation_delay
        return 30
        
    @property
    def register_final_view(self):
        return absolute_url(self.context, self.request, 'register-final.html')

    @property
    def password_reset_view(self):
        return absolute_url(self.context, self.request, 'password-reset.html')

    @property
    def password_reset_final_view(self):
        return absolute_url(self.context, self.request, 'password-final.html')

    @property
    def password_change_view(self):
        return absolute_url(self.context, self.request, 'password-change.html')

    @property
    def password_change_final_view(self):
        return absolute_url(self.context, self.request, 'password-changed.html')


class IRegisterFormButtons(Interface):
    """Register form buttons interface"""

    register = SubmitButton(name='register',
                            title=_("Create account"))

    reset = ResetButton(name='reset',
                        title=_("Reset"))


@ajax_form_config(name='register.html',
                  layer=IPyAMSLayer)
class RegisterForm(AddForm, PortalContextIndexPage):
    """Register form"""

    title = _("Registration form")
    legend = _("Account settings")

    fields = Fields(IUserProfile).omit('principal_id', 'active')
    content_factory = IUserProfile

    buttons = Buttons(IRegisterFormButtons)

    _edit_permission = PUBLIC_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        email = self.widgets.get('email')
        if email is not None:
            email.object_data = {
                'input-mask': {
                    'alias': 'email',
                    'clearIncomplete': True
                }
            }
            alsoProvides(email, IObjectData)
        phone_number = self.widgets.get('phone_number')
        if phone_number is not None:
            phone_number.object_data = {
                'input-mask': {
                    'mask': '[+9{3}] 99 99 99 99 99',
                    'clearIncomplete': True
                }
            }
            alsoProvides(phone_number, IObjectData)
        structure_type = self.widgets.get('structure_type')
        if structure_type is not None:
            structure_type.prompt = True
            structure_type.prompt_message = _("Please select your structure type...")
        address = self.widgets.get('establishment_address')
        if address is not None:
            postal_code = address.widgets.get('postal_code')
            if postal_code is not None:
                postal_code.object_data = {
                    'input-mask': {
                        'mask': '99999',
                        'clearIncomplete': True
                    }
                }
                alsoProvides(postal_code, IObjectData)

    @handler(buttons['register'])
    def handle_register(self, action):
        self.handle_add(self, action)

    def add(self, obj):
        login_config = ILoginConfiguration(self.request.root)
        if not login_config.open_registration:
            raise HTTPBadRequest(_("Registration is actually closed!"))
        sm = get_utility(ISecurityManager)
        users_folder = sm.get(login_config.users_folder)
        if users_folder is not None:
            local_user = create_object(ILocalUser)
            local_user.login = obj.email
            local_user.email = obj.email
            local_user.firstname = obj.firstname
            local_user.lastname = obj.lastname
            local_user.company_name = obj.establishment
            local_user.password = LOCKED_ACCOUNT_PASSWORD
            local_user.generate_secret(notify=True, request=self.request)
            users_folder[local_user.login] = local_user
            principal = IPrincipalInfo(local_user)
            annotations = IAnnotations(principal)
            annotations[USER_PROFILE_KEY] = obj
            obj.principal_id = annotations.principalId
            self.request.registry.notify(RegisteredPrincipalEvent(principal))


@subscriber(IDataExtractedEvent, form_selector=RegisterForm)
def extract_register_form_data(event: IDataExtractedEvent):
    """Extract register form data"""
    data = event.data
    email = data.get('email')
    if email:
        login_config = ILoginConfiguration(event.form.request.root)
        sm = get_utility(ISecurityManager)
        if login_config.open_registration:
            users_folder = sm.get(login_config.users_folder)
            if users_folder is not None:
                user = users_folder.get(email)
                if user is not None:
                    event.form.widgets.errors += (Invalid(_("This email address is already "
                                                            "registered!")),)


@viewlet_config(name='form-help',
                context=Interface, layer=IPyAMSLayer, view=RegisterForm,
                manager=IFormHeaderViewletManager, weight=10)
class RegisterFormHelp(AlertMessage):
    """Register form help"""

    status = 'info'

    _message = _("This form allows you to register a new user account.\n"
                 "After submitting the form, you will receive an email containing a link which "
                 "must be used to confirm your email address and set a new password.")


@adapter_config(required=(Interface, IPyAMSLayer, RegisterForm),
                provides=IAJAXFormRenderer)
class RegisterFormRenderer(ContextRequestViewAdapter):
    """Register form renderer"""

    def render(self, changes):
        if changes is None:
            return None
        register_views = self.request.registry.getMultiAdapter((self.context, self.request),
                                                               IUserRegistrationViews)
        return {
            'status': 'redirect',
            'location': register_views.register_ok_view
        }


@pagelet_config(name='register-ok.html',
                layer=IPyAMSLayer)
@template_config(template='templates/register-ok.pt',
                 layer=IPyAMSLayer)
class RegisterOKView(PortalContextIndexPage):
    """Saved registration view"""

    @property
    def activation_delay(self):
        configuration = ILoginConfiguration(self.request.root)
        return configuration.activation_delay


class IUserRegistrationConfirmationInfo(IUserRegistrationConfirmationInfoBase):
    """User registration confirmation info interface"""

    login = TextLine(title=_("E-mail address"),
                     required=True)


class IUserRegistrationConfirmationButtons(Interface):
    """User registration confirmation buttons interface"""

    validate = SubmitButton(name='validate',
                            title=_("Validate account"))

    reset = ResetButton(name='reset',
                        title=_("Reset"))


@ajax_form_config(name='register-confirm.html',
                  layer=IPyAMSLayer)
class RegistrationConfirmForm(AddForm, PortalContextIndexPage):
    """Registration confirmation form"""

    title = _("Registration confirm form")
    legend = _("Confirm your login and set a new password")

    fields = Fields(IUserRegistrationConfirmationInfo).select('login', 'password', 'confirmed_password',
                                                              'activation_hash')
    buttons = Buttons(IUserRegistrationConfirmationButtons)

    _edit_permission = PUBLIC_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        hash = self.widgets.get('activation_hash')
        if hash is not None:
            hash.mode = HIDDEN_MODE
            hash.value = self.request.params.get('hash')

    @handler(buttons['validate'])
    def handle_validate(self, action):
        self.handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        login_config = ILoginConfiguration(self.request.root)
        sm = get_utility(ISecurityManager)
        users_folder = sm.get(login_config.users_folder)
        if users_folder is not None:
            user = users_folder.get(data.get('login'))
            if user is None:
                self.widgets.errors += (Invalid(_("Can't activate account with provided arguments!")),)
            else:
                hash = data.get('activation_hash')
                try:
                    user.check_activation(hash, user.login, LOCKED_ACCOUNT_PASSWORD)
                except Invalid as exc:
                    translate = self.request.localizer.translate
                    self.widgets.errors += (Invalid(', '.join(map(translate, exc.args))),)
                else:
                    user.password = data.get('password')
                    principal = IPrincipalInfo(user)
                    self.request.registry.notify(ActivatedPrincipalEvent(principal))
                    return user


@adapter_config(required=(Interface, IPyAMSLayer, RegistrationConfirmForm),
                provides=IAJAXFormRenderer)
class RegistrationConfirmFormRenderer(ContextRequestViewAdapter):
    """Registration confirm form renderer"""

    def render(self, changes):
        if changes is None:
            return None
        register_views = self.request.registry.getMultiAdapter((self.context, self.request),
                                                               IUserRegistrationViews)
        return {
            'status': 'redirect',
            'location': register_views.register_final_view
        }


@pagelet_config(name='register-final.html',
                layer=IPyAMSLayer)
@template_config(template='templates/register-final.pt',
                 layer=IPyAMSLayer)
class RegistrationFinalView(PortalContextIndexPage):
    """Registration final view"""
