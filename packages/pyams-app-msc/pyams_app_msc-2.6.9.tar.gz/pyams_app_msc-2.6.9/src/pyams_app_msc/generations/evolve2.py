#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
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

from zope.principalannotation.interfaces import IPrincipalAnnotationUtility

from pyams_app_msc.feature.profile import OPERATOR_PROFILE_KEY, USER_PROFILE_KEY
from pyams_utils.registry import get_local_registry, get_utility, set_local_registry
from pyams_zmi.interfaces.profile import USER_PROFILE_KEY as ADMIN_PROFILE_KEY

__docformat__ = 'restructuredtext'


def evolve(site):
    """Add missing principal_id attribute to user annotations"""
    old_registry = get_local_registry()
    try:
        registry = site.getSiteManager()
        set_local_registry(registry)
        # Get principals annotations
        utility = get_utility(IPrincipalAnnotationUtility)
        if utility is not None:
            profiles = utility.annotations
            for principal_id, annotations in profiles.items():
                # update user profile
                user_profile = annotations.get(USER_PROFILE_KEY, None)
                if user_profile is not None:
                    user_profile.principal_id = principal_id
                # update operator profile
                operator_profile = annotations.get(OPERATOR_PROFILE_KEY, None)
                if operator_profile is not None:
                    operator_profile.principal_id = principal_id
                # update admin profile
                admin_profile = annotations.get(ADMIN_PROFILE_KEY, None)
                if admin_profile is not None:
                    admin_profile.principal_id = principal_id
    finally:
        set_local_registry(old_registry)
