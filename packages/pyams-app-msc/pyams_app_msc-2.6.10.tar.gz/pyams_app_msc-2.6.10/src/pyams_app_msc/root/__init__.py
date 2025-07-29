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

from zope.interface import implementer

__docformat__ = 'restructuredtext'

from pyams_app_msc.root.interfaces import IMSCSiteRootRoles, MSC_SITEROOT_ROLES
from pyams_security.interfaces import IRolesPolicy
from pyams_security.property import RolePrincipalsFieldProperty
from pyams_security.security import ProtectedObjectRoles
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextAdapter, adapter_config


@implementer(IMSCSiteRootRoles)
class SiteRootRoles(ProtectedObjectRoles):
    """Site root roles"""

    msc_site_managers = RolePrincipalsFieldProperty(IMSCSiteRootRoles['msc_site_managers'])


@adapter_config(required=ISiteRoot,
                provides=IMSCSiteRootRoles)
def site_root_roles_adapter(context):
    """Site root roles adapter"""
    return SiteRootRoles(context)


@adapter_config(name=MSC_SITEROOT_ROLES,
                required=ISiteRoot,
                provides=IRolesPolicy)
class SiteRootRolesPolicy(ContextAdapter):
    """Site root roles policy"""

    roles_interface = IMSCSiteRootRoles
    weight = 50
