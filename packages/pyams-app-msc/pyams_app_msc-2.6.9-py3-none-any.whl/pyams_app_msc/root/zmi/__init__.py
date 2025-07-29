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

from pyams_app_msc.interfaces import VIEW_THEATER_PERMISSION
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.interfaces import MANAGE_REFERENCE_TABLE_PERMISSION, MANAGE_SITE_TREE_PERMISSION
from pyams_content.reference import IReferenceTable
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import INavigationViewletManager, ISiteManagementMenu
from pyams_zmi.zmi.viewlet.menu import SiteManagementMenu


@viewletmanager_config(name='site-manager.menu',
                       layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=200,
                       provides=ISiteManagementMenu,
                       permission=MANAGE_SITE_TREE_PERMISSION)
class MSCSiteManagementMenu(SiteManagementMenu):
    """MSC site management menu"""


@viewletmanager_config(name='site-manager.menu',
                       context=IReferenceTable, layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=200,
                       provides=ISiteManagementMenu,
                       permission=MANAGE_REFERENCE_TABLE_PERMISSION)
class MSCReferenceTableManagementMenu(SiteManagementMenu):
    """MSC reference table site management menu"""


@viewletmanager_config(name='site-manager.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=200,
                       provides=ISiteManagementMenu,
                       permission=VIEW_THEATER_PERMISSION)
class MSCMovieTheaterSiteManagementMenu(SiteManagementMenu):
    """MSC movie theater site management menu"""
