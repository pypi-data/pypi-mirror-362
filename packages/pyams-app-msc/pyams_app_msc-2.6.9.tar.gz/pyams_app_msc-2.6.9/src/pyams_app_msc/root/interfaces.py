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

from zope.interface import Interface

from pyams_app_msc.interfaces import MSC_SITES_MANAGER_ROLE
from pyams_security.schema import PrincipalsSetField

from pyams_app_msc import _


MSC_SITEROOT_ROLES = 'msc.root.roles'


class IMSCSiteRootRoles(Interface):
    """Site root roles interface"""

    msc_site_managers = PrincipalsSetField(title=_("Sites managers"),
                                           description=_("These principals are allowed to create "
                                                         "and manage sites and movie theaters"),
                                           role_id=MSC_SITES_MANAGER_ROLE,
                                           required=False)
