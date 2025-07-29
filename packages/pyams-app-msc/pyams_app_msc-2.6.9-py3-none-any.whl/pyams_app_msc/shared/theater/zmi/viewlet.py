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

from zope.interface import Interface

from pyams_app_msc.interfaces import VIEW_CATALOG_PERMISSION
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_content.interfaces import MANAGE_SITE_PERMISSION
from pyams_content.shared.site.zmi.viewlet import SharedSitesMenu
from pyams_content.zmi.viewlet.toplinks import TopTabsViewletManager
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer


__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewletmanager_config(name='movie-theaters.menu',
                       context=Interface, layer=IAdminLayer,
                       manager=TopTabsViewletManager, weight=5)
class MovieTheatersMenu(SharedSitesMenu):
    """Movie theaters menu"""

    label = _("My theaters")
    interface = IMovieTheater

    menus_permissions = {
        VIEW_CATALOG_PERMISSION
    }
