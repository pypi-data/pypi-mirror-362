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

from fanstatic import Library, Resource
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IControlPanelMenu, INavigationViewletManager
from pyams_zmi.zmi.viewlet.menu import ControlPanelMenu


library = Library('msc', 'resources')

msc = Resource(library, 'js/msc.js',
               minified='js/msc.min.js')


@viewletmanager_config(name='control-panel.menu', layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=300,
                       provides=IControlPanelMenu,
                       permission=MANAGE_SYSTEM_PERMISSION)
class MSCControlPanelMenu(ControlPanelMenu):
    """MSC control panel menu"""
