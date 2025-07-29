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

from pyams_zmi.interfaces.viewlet import INavigationMenuItem

__docformat__ = 'restructuredtext'


class IPlanningMenu(INavigationMenuItem):
    """Planning menu marker interface"""


class IActivitySessionsTable(Interface):
    """Activity sessions table marker interface"""
    
    
class IActivityCurrentSessionsTable(IActivitySessionsTable):
    """Activity current sessions table marker interface"""


class IActivityArchivedSessionsTable(IActivitySessionsTable):
    """Activity archived sessions table marker interface"""


class ISessionForm(Interface):
    """Session form marker interface"""
