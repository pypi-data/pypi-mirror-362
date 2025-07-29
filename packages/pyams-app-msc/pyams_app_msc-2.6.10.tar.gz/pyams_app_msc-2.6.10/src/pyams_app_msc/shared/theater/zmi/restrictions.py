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

from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_security_views.zmi.interfaces import IObjectSecurityMenu
from pyams_utils.adapter import NullAdapter
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer


@viewlet_config(name='managers-restrictions.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IObjectSecurityMenu, weight=200,
                permission=MANAGE_TOOL_PERMISSION)
class MovieTheaterManagersRestrictionsMenu(NullAdapter):
    """Disabled movie theater manager restrictions menu"""


@viewlet_config(name='contributors-restrictions.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IObjectSecurityMenu, weight=210,
                permission=MANAGE_TOOL_PERMISSION)
class MovieTheaterContributorsRestrictionsMenu(NullAdapter):
    """Disabled movie theater contributor restrictions menu"""
