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

from persistent import Persistent
from pyramid.authorization import ALL_PERMISSIONS, Allow
from pyramid.interfaces import IRequest
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.feature.profile.interfaces import IOperatorProfile, IUserProfile, OPERATOR_PROFILE_KEY, \
    USER_PROFILE_KEY
from pyams_app_msc.reference.structure import IStructureType, IStructureTypeTable
from pyams_i18n.interfaces import II18n
from pyams_security.interfaces.base import IPrincipalInfo
from pyams_security.interfaces.names import ADMIN_USER_ID
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.registry import get_utility

__docformat__ = 'restructuredtext'


@factory_config(IUserProfile)
class UserProfile(Persistent, Contained):
    """User profile persistent class"""

    principal_id = None

    active = FieldProperty(IUserProfile['active'])
    firstname = FieldProperty(IUserProfile['firstname'])
    lastname = FieldProperty(IUserProfile['lastname'])
    email = FieldProperty(IUserProfile['email'])
    phone_number = FieldProperty(IUserProfile['phone_number'])
    establishment = FieldProperty(IUserProfile['establishment'])
    structure_type = FieldProperty(IUserProfile['structure_type'])
    establishment_address = FieldProperty(IUserProfile['establishment_address'])
    local_theaters = FieldProperty(IUserProfile['local_theaters'])

    def __acl__(self):
        return [
            (Allow, ADMIN_USER_ID, ALL_PERMISSIONS),
            (Allow, self.principal_id, ALL_PERMISSIONS)
        ]

    def get_structure_type(self):
        structures = get_utility(IStructureTypeTable)
        structure_type = structures.get(self.structure_type)
        if structure_type is None:
            return MISSING_INFO
        return II18n(structure_type).query_attribute('title')


@adapter_config(required=IUserProfile,
                provides=IStructureType)
def principal_structure_type(context):
    """User profile structure type adapter"""
    return context.get_structure_type()


@adapter_config(required=IPrincipalInfo,
                provides=IUserProfile)
def principal_user_profile(principal):
    """Principal user profile factory"""

    def user_profile_callback(profile):
        profile.principal_id = principal.id

    return get_annotation_adapter(principal, USER_PROFILE_KEY, IUserProfile,
                                  locate=False, callback=user_profile_callback)


@adapter_config(required=IRequest,
                provides=IUserProfile)
def request_user_profile(request):
    """Request user profile factory"""
    return IUserProfile(request.principal, None)


@factory_config(IOperatorProfile)
class OperatorProfile(Persistent, Contained):
    """Operator profile persistent class"""

    principal_id = None

    session_seats_display_mode = FieldProperty(IOperatorProfile['session_seats_display_mode'])
    today_program_length = FieldProperty(IOperatorProfile['today_program_length'])


@adapter_config(required=IPrincipalInfo,
                provides=IOperatorProfile)
def principal_operator_profile(principal):
    """Principal operator profile factory"""

    def operator_profile_callback(profile):
        profile.principal_id = principal.id

    return get_annotation_adapter(principal, OPERATOR_PROFILE_KEY, IOperatorProfile,
                                  locate=False, callback=operator_profile_callback)


@adapter_config(required=IRequest,
                provides=IOperatorProfile)
def request_operator_profile(request):
    """Request operator profile factory"""
    return IOperatorProfile(request.principal, None)
