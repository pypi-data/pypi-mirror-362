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
from zope.schema import Bool, Int, TextLine

from pyams_content.feature.renderer import IRendererSettings
from pyams_content.shared.view.portlet.skin import IViewItemsPortletPanelsRendererSettings

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class ICatalogViewItemsPortletCalendarRendererSettings(Interface):
    """Catalog view items portlet calendar renderer settings"""

    filters_css_class = TextLine(title=_('Filters CSS class'),
                                 description=_("CSS class used for filters column"),
                                 default='col col-12 col-md-4 col-lg-3 col-xl-2 float-left text-md-right')

    calendar_css_class = TextLine(title=_('Calendar CSS class'),
                                  description=_("CSS class used for calendar container"),
                                  default='row mx-0 col col-12 col-md-8 col-lg-9 col-xl-10 float-right')

    sessions_weeks = Int(title=_("Sessions weeks"),
                         description=_("Number of weeks to display sessions"),
                         required=True,
                         default=4)


class ICatalogViewItemsPortletPanelsRendererSettings(IViewItemsPortletPanelsRendererSettings):
    """Catalog view items portlet panels renderers settings"""

    first_panel_css_class = TextLine(title=_('First panel CSS class'),
                                     description=_("CSS class used for first view items panel"),
                                     default='col col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 my-3 d-flex flex-column')

    panels_css_class = TextLine(title=_('Panels CSS class'),
                                description=_("CSS class used for view items panels"),
                                default='col my-3 d-flex flex-column')

    display_sessions = Bool(title=_("Display sessions"),
                            description=_("If 'no', incoming sessions will not be displayed"),
                            required=True,
                            default=True)

    sessions_weeks = Int(title=_("Sessions weeks"),
                         description=_("Number of weeks to display sessions"),
                         required=True,
                         default=4)

    display_free_seats = Bool(title=_("Display free seats"),
                              description=_("If 'no', number of free seats is not displayed"),
                              required=True,
                              default=True)


class ICatalogEntrySpecificitiesPortletRendererSettings(IRendererSettings):
    """Catalog entry specificities portlet renderer settings interface"""

    display_sessions = Bool(title=_("Display sessions"),
                            description=_("If 'no', incoming sessions will not be displayed"),
                            required=True,
                            default=True)

    sessions_weeks = Int(title=_("Sessions weeks"),
                         description=_("Number of weeks to display sessions"),
                         required=True,
                         default=4)

    display_free_seats = Bool(title=_("Display free seats"),
                              description=_("If 'no', number of free seats is not displayed"),
                              required=True,
                              default=True)
