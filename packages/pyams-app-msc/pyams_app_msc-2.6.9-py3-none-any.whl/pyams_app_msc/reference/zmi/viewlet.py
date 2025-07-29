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

from zope.interface import Interface

from pyams_content.interfaces import MANAGE_REFERENCE_TABLE_PERMISSION
from pyams_content.reference.zmi.viewlet import ReferencesTablesMenu
from pyams_content.zmi.viewlet.toplinks import TopTabsViewletManager
from pyams_viewlet.manager import viewletmanager_config
from pyams_zmi.interfaces import IAdminLayer


@viewletmanager_config(name='reference-tables.menu',
                       context=Interface, layer=IAdminLayer,
                       manager=TopTabsViewletManager, weight=40)
class MSCReferencesTablesMenu(ReferencesTablesMenu):
    """MSC reference tables menu"""

    menus_permissions = {MANAGE_REFERENCE_TABLE_PERMISSION}
