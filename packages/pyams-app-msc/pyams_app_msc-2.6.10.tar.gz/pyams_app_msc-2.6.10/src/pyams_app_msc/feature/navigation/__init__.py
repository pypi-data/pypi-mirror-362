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

from pyams_app_msc.feature.navigation.interfaces import INavigationViewletManager
from pyams_app_msc.skin import IPyAMSMSCLayer
from pyams_template.template import template_config
from pyams_viewlet.manager import TemplateBasedViewletManager, WeightOrderedViewletManager, viewletmanager_config
from pyams_viewlet.viewlet import Viewlet

__docformat__ = 'restructuredtext'


@viewletmanager_config(name='msc.navigation',
                       layer=IPyAMSMSCLayer,
                       provides=INavigationViewletManager)
@template_config(template='templates/navigation.pt',
                 layer=IPyAMSMSCLayer)
class NavigationViewletManager(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Navigation viewlet manager"""


@template_config(template='templates/navigation-menu.pt',
                 layer=IPyAMSMSCLayer)
class NavigationMenuItem(Viewlet):
    """Navigation menu"""

    css_class = ''
