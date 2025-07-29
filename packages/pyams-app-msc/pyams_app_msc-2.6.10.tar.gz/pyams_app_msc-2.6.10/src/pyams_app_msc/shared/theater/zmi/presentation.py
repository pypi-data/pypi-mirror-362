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

from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.zmi.interfaces import IMovieTheaterCalendarPresentationMenu, \
    IMovieTheaterCatalogPresentationMenu, IMovieTheaterMoviesPresentationMenu
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_portal.zmi.interfaces import IPortalContextPresentationMenu
from pyams_portal.zmi.presentation import PortalContextPresentationEditForm, PortalContextTemplateLayoutMenu, \
    PortalContextTemplateLayoutView
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

from pyams_app_msc import _


#
# Movie theater calendar presentation components
#

@viewletmanager_config(name='calendar-presentation.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=IPortalContextPresentationMenu, weight=30,
                       provides=IMovieTheaterCalendarPresentationMenu,
                       permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCalendarPresentationMenu(NavigationMenuItem):
    """Movie theater calendar presentation menu"""

    label = _("Calendar presentation")
    icon_class = 'fas fa-calendar'
    href = '#calendar-presentation.html'


@ajax_form_config(name='calendar-presentation.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCalendarPresentationEditForm(PortalContextPresentationEditForm):
    """Movie theater calendar presentation edit form"""

    title = _("Calendar template configuration")

    page_name = 'calendar'


@viewlet_config(name='calendar-template-layout.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IMovieTheaterCalendarPresentationMenu, weight=10,
                permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCalendarTemplateLayoutMenu(PortalContextTemplateLayoutMenu):
    """Movie theater calendar template layout menu"""

    label = _("Calendar layout")
    href = '#calendar-template-layout.html'

    page_name = 'calendar'


@pagelet_config(name='calendar-template-layout.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCalendarTemplateLayoutView(PortalContextTemplateLayoutView):
    """Movie theater calendar template layout view"""

    page_name = 'calendar'


#
# Movie theater movies list presentation components
#

@viewletmanager_config(name='movies-presentation.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=IPortalContextPresentationMenu, weight=35,
                       provides=IMovieTheaterMoviesPresentationMenu,
                       permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterMoviesPresentationMenu(NavigationMenuItem):
    """Movie theater movies presentation menu"""

    label = _("Movies list presentation")
    icon_class = 'fas fa-photo-film'
    href = '#movies-presentation.html'


@ajax_form_config(name='movies-presentation.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterMoviesPresentationEditForm(PortalContextPresentationEditForm):
    """Movie theater movies presentation edit form"""

    title = _("Movies list template configuration")

    page_name = 'movies'


@viewlet_config(name='movies-template-layout.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IMovieTheaterMoviesPresentationMenu, weight=10,
                permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterMoviesTemplateLayoutMenu(PortalContextTemplateLayoutMenu):
    """Movie theater movies list template layout menu"""

    label = _("Movies list layout")
    href = '#movies-template-layout.html'

    page_name = 'movies'


@pagelet_config(name='movies-template-layout.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterMoviesTemplateLayoutView(PortalContextTemplateLayoutView):
    """Movie theater movies list template layout view"""

    page_name = 'movies'


#
# Catalog entries presentation components
#

@viewletmanager_config(name='catalog-presentation.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=IPortalContextPresentationMenu, weight=40,
                       provides=IMovieTheaterCatalogPresentationMenu,
                       permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCatalogPresentationMenu(NavigationMenuItem):
    """Movie theater catalog presentation menu"""

    label = _("Catalog presentation")
    icon_class = 'fas fa-panorama'
    href = '#catalog-presentation.html'


@ajax_form_config(name='catalog-presentation.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCatalogPresentationEditForm(PortalContextPresentationEditForm):
    """Portal context footer presentation edit form"""

    title = _("Catalog template configuration")

    page_name = 'catalog'


@viewlet_config(name='catalog-template-layout.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IMovieTheaterCatalogPresentationMenu, weight=10,
                permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCatalogTemplateLayoutMenu(PortalContextTemplateLayoutMenu):
    """Movie theater catalog template layout menu"""

    label = _("Catalog layout")
    href = '#catalog-template-layout.html'

    page_name = 'catalog'


@pagelet_config(name='catalog-template-layout.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCatalogTemplateLayoutView(PortalContextTemplateLayoutView):
    """Movie theater catalog template layout view"""

    page_name = 'catalog'
