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
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.audience import ICinemaAudienceContainer
from pyams_app_msc.shared.theater.portlet.interfaces import IAudiencesPortletSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_app_msc import _
from pyams_utils.traversing import get_parent

AUDIENCES_PORTLET_NAME = 'msc.portlet.audiences'
AUDIENCES_ICON_CLASS = 'fas fa-bullhorn'


@factory_config(IAudiencesPortletSettings)
class AudiencesPortletSettings(PortletSettings):
    """Audiences banner portlet settings"""

    @staticmethod
    def get_parent(context):
        """Parent movie theater getter"""
        return get_parent(context, IMovieTheater)

    @staticmethod
    def get_audiences(context):
        """Audiences list getter"""
        theater = get_parent(context, IMovieTheater)
        audiences = ICinemaAudienceContainer(theater, None)
        if audiences is not None:
            yield from audiences.get_active_items()


@portlet_config(permission=None)
class AudiencesPortlet(Portlet):
    """Audiences portlet"""

    name = AUDIENCES_PORTLET_NAME
    label = _("MSC: Audiences list")

    settings_factory = IAudiencesPortletSettings
    toolbar_css_class = AUDIENCES_ICON_CLASS
