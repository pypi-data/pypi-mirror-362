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

from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.shared.common.zmi.dashboard import SharedToolDashboardView
from pyams_content.shared.common.zmi.search import SharedToolQuickSearchView
from pyams_utils.adapter import adapter_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IInnerTable

from pyams_app_msc import _


@adapter_config(name='quick-search',
                required=(IMovieTheater, IAdminLayer, SharedToolDashboardView),
                provides=IInnerTable)
class MovieTheaterQuickSearchView(SharedToolQuickSearchView):
    """Movie theater quick search view"""

    @property
    def legend(self):
        """Legend getter"""
        translate = self.request.localizer.translate
        return translate(_("Between all catalog contents"))
