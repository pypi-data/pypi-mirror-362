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

__docformat__ = 'restructuredtext'

from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_app_msc.shared.theater import IMovieTheater, IMovieTheaterRoles
from pyams_content.shared.common import IWfSharedContentRoles
from pyams_content.shared.common.interfaces import ISharedToolRoles
from pyams_content.shared.common.security import WfSharedContentRoles
from pyams_security.property import RolePrincipalsFieldProperty
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent


class WfCatalogEntryRoles(WfSharedContentRoles):
    """Catalog entry roles"""

    _managers = RolePrincipalsFieldProperty(IWfSharedContentRoles['managers'])
    _contributors = RolePrincipalsFieldProperty(IWfSharedContentRoles['contributors'])

    @property
    def managers(self):
        theater = get_parent(self.__parent__, IMovieTheater)
        return IMovieTheaterRoles(theater).msc_operators | (self._managers or set())

    @managers.setter
    def managers(self, value):
        self._managers = value

    @property
    def contributors(self):
        theater = get_parent(self.__parent__, IMovieTheater)
        return IMovieTheaterRoles(theater).msc_contributors | (self._contributors or set())

    @contributors.setter
    def contributors(self, value):
        self._contributors = value


@adapter_config(required=IWfCatalogEntry,
                provides=IWfSharedContentRoles)
def catalog_entry_roles_adapter(context):
    """Catalog entry roles adapter"""
    return WfCatalogEntryRoles(context)
