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
from pyams_content.component.paragraph.zmi.container import ParagraphsMenu
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu


@viewlet_config(name='paragraphs.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=650,
                permission=VIEW_SYSTEM_PERMISSION)
class MovieTheaterParagraphsMenu(ParagraphsMenu):
    """Movie theater paragraphs menu"""
