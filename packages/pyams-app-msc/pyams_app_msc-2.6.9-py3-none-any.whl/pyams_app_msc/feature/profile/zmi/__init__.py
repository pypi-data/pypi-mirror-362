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

"""PyAMS_app_msc.feature.profile.zmi module

This module defines components which are used to manage users profiles.
"""

from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPNotFound
from zope.annotation.interfaces import IAnnotations
from zope.interface import Interface, Invalid, alsoProvides
from zope.schema import Bool

from pyams_app_msc.feature.profile.interfaces import IOperatorProfile, IUserProfile, USER_PROFILE_KEY
from pyams_app_msc.feature.profile.zmi.interfaces import IUserProfilesSearchResultsTable
from pyams_app_msc.interfaces import MANAGE_BOOKING_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces import DISPLAY_MODE, HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent, IFormContent, IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_mail.interfaces import IPrincipalMailInfo
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import IMissingPrincipalInfo, IPrincipalInfo
from pyams_security.interfaces.plugin import ILocalUser, LOCKED_ACCOUNT_PASSWORD
from pyams_security.utility import get_principal
from pyams_security_views.interfaces.login import ILoginConfiguration
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.schema.button import ActionButton
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import create_object
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.registry import get_utility
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IModalDisplayFormButtons, IModalEditFormButtons
from pyams_zmi.zmi.profile import UserProfileEditForm as ZMIProfileEditForm

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class IUserProfileAddFields(IUserProfile):
    """USer profile add fields info interface"""

    notify = Bool(title=_("Notify user?"),
                  description=_("If 'yes', a notification message containing an activation link will be sent to "
                                "this user after his profile creation"),
                  required=True,
                  default=True)


@adapter_config(required=IUserProfile,
                provides=IUserProfileAddFields)
def user_profile_add_form_fields(profile):
    """User profile add form context adapter"""
    return profile


@ajax_form_config(name='add-user-profile.html',
                  layer=IPyAMSLayer,
                  permission=MANAGE_BOOKING_PERMISSION)
class UserProfileAddForm(AdminModalAddForm):
    """User profile add form"""

    title = _("User add form")
    legend = _("User account settings")
    autocomplete = 'off'

    fields = Fields(IUserProfileAddFields).omit('active', 'principal_id')
    content_factory = IUserProfile

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        phone_number = self.widgets.get('phone_number')
        if phone_number is not None:
            phone_number.object_data = {
                'input-mask': '[+9{3}] [9]9 99 99 99 99'
            }
            alsoProvides(phone_number, IObjectData)
        email = self.widgets.get('email')
        if email is not None:
            email.object_data = {
                'input-mask': {
                    'alias': 'email',
                    'clearIncomplete': True
                }
            }
            alsoProvides(email, IObjectData)
        structure_type = self.widgets.get('structure_type')
        if structure_type is not None:
            structure_type.prompt = True
            structure_type.prompt_message = _("Select structure type...")
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

    def create(self, data):
        result = super().create(data)
        result._v_notify = data.get(self, data).get('notify')
        return result

    def add(self, obj):
        login_config = ILoginConfiguration(self.request.root)
        sm = get_utility(ISecurityManager)
        users_folder = sm.get(login_config.users_folder)
        if users_folder is not None:
            local_user = create_object(ILocalUser)
            local_user.self_registered = False
            local_user.login = obj.email
            local_user.email = obj.email
            local_user.firstname = obj.firstname
            local_user.lastname = obj.lastname
            local_user.company_name = obj.establishment
            local_user.password = LOCKED_ACCOUNT_PASSWORD
            local_user.generate_secret(notify=getattr(obj, '_v_notify', False),
                                       request=self.request)
            users_folder[local_user.login] = local_user
            principal = IPrincipalInfo(local_user)
            annotations = IAnnotations(principal)
            annotations[USER_PROFILE_KEY] = obj


@subscriber(IDataExtractedEvent, form_selector=UserProfileAddForm)
def extract_user_profile_add_form_data(event: IDataExtractedEvent):
    """Extract user profile add form data"""
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
                context=Interface, layer=IPyAMSLayer, view=UserProfileAddForm,
                manager=IFormHeaderViewletManager, weight=10)
class UserProfileAddFormHelp(AlertMessage):
    """User profile add form help"""

    status = 'info'

    _message = _("This form allows you to register a new user account.\n"
                 "If this user want to login, he will have to use the \"Forgotten "
                 "password\" feature to get a new activation link to set his password.")


#
# User profile edit form
#

class IUserProfileEditFormButtons(IModalEditFormButtons):
    """User profile edit form buttons interface"""

    disable = ActionButton(name='disable',
                           title=_("Disable profile"),
                           condition=lambda form: IUserProfile(form.form_content).active)

    enable = ActionButton(name='enable',
                          title=_("Enable profile"),
                          condition=lambda form: not IUserProfile(form.form_content).active)


@ajax_form_config(name='edit-user-profile.html',
                  layer=IPyAMSLayer,
                  permission=MANAGE_BOOKING_PERMISSION)
class UserProfileEditForm(AdminModalEditForm):
    """User profile edit form"""

    title = _("User edit form")
    legend = _("User account settings")

    fields = Fields(IUserProfile).omit('active')

    @property
    def buttons(self):
        if self.mode == DISPLAY_MODE:
            return Buttons(IModalDisplayFormButtons)
        return Buttons(IUserProfileEditFormButtons).select('disable', 'enable', 'apply', 'close')

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        request = self.request
        principal_id = (request.params.get('principal_id') or
                        request.params.get(f'{self.prefix}widgets.principal_id'))
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
                sm = get_utility(ISecurityManager)
                principal_info = sm.get_principal(principal_id, info=False)
                if principal_info is not None:
                    mail_info = IPrincipalMailInfo(principal_info, None)
                    if mail_info is not None:
                        _title, principal_email = next(mail_info.get_addresses())
                        email.value = principal_email
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

    def update_actions(self):
        super().update_actions()
        translate = self.request.localizer.translate
        disable = self.actions.get('disable')
        if disable is not None:
            disable.add_class('btn-danger mr-auto')
            disable.hint = translate(_("Disabled profiles can't be used for website login anymore but can "
                                       "still be assigned new bookings"))
        enable = self.actions.get('enable')
        if enable is not None:
            enable.add_class('btn-danger mr-auto')

    @handler(IUserProfileEditFormButtons['disable'])
    def handle_disable(self, action):
        """Handle disable button"""
        principal_info = self.form_content
        IUserProfile(principal_info).active = False
        sm = get_utility(ISecurityManager)
        user = sm.get_raw_principal(principal_info.id)
        if ILocalUser.providedBy(user):
            user.activated = False
        self.finished_state.update({
            'action': action,
            'changes': user
        })

    @handler(IUserProfileEditFormButtons['enable'])
    def handle_enable(self, action):
        """Handle enable action"""
        principal_info = self.form_content
        IUserProfile(principal_info).active = True
        sm = get_utility(ISecurityManager)
        user = sm.get_raw_principal(principal_info.id)
        if ILocalUser.providedBy(user):
            user.wait_confirmation = False
            user.activated = True
        self.finished_state.update({
            'action': action,
            'changes': user
        })

    @handler(IUserProfileEditFormButtons['apply'])
    def handle_apply(self, action):
        super().handle_apply(self, action)

    def apply_changes(self, data):
        changes = super().apply_changes(data)
        if changes:
            data = data.get(self, data)
            login_config = ILoginConfiguration(self.request.root)
            sm = get_utility(ISecurityManager)
            users_folder = sm.get(login_config.users_folder)
            local_user = users_folder[data.get('email')]
            if local_user is not None:
                local_user.firstname = data.get('firstname')
                local_user.lastname = data.get('lastname')
                local_user.company_name = data.get('establishment')
        return changes


@adapter_config(required=(Interface, IAdminLayer, UserProfileEditForm),
                provides=IFormContent)
def user_profile_edit_form_content(context, request, view):
    """User profile edit form content getter"""
    principal = None
    principal_id = request.params.get('principal_id') or request.params.get(f'{view.prefix}widgets.principal_id')
    if principal_id:
        principal = get_principal(request, principal_id)
    else:
        email = request.params.get(f'{view.prefix}widgets.email')
        if email:
            login_config = ILoginConfiguration(request.root)
            sm = get_utility(ISecurityManager)
            users_folder = sm.get(login_config.users_folder)
            if users_folder is not None:
                try:
                    principal = next(users_folder.find_principals(email, exact_match=True))
                except StopIteration:
                    principal = None
    if (principal is None) or IMissingPrincipalInfo.providedBy(principal):
        raise HTTPNotFound()
    return principal


@adapter_config(required=(Interface, IAdminLayer, UserProfileEditForm),
                provides=IAJAXFormRenderer)
class UserProfileEditFormRenderer(ContextRequestViewAdapter):
    """User profile edit form renderer"""
    
    table_factory = IUserProfilesSearchResultsTable
    
    def render(self, changes):
        if not changes:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_refresh_callback(self.context, self.request,
                                                    self.table_factory, IUserProfile(self.view.form_content))
            ]
        }
    

#
# Operator profile edit form
#

@adapter_config(name='operator-profile',
                required=(Interface, IAdminLayer, ZMIProfileEditForm),
                provides=IGroup)
class OperatorProfileGroup(Group):
    """Operator profile group"""

    legend = _("Operator profile")

    fields = Fields(IOperatorProfile)


@adapter_config(required=(Interface, IAdminLayer, OperatorProfileGroup),
                provides=IFormContent)
def operator_profile_group_content(context, request, group):
    """Operator profile edit group content getter"""
    return IOperatorProfile(request.principal)
