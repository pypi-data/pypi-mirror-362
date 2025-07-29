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

from pyams_app_msc.shared.theater.interfaces import IMovieTheater, IMovieTheaterCalendarPortalPage, \
    IMovieTheaterCatalogPortalPage, IMovieTheaterMoviesPortalPage
from pyams_portal.interfaces import IPortalPage, IPortalPortletsConfiguration, PORTAL_PAGE_KEY
from pyams_portal.page import PortalPage, portal_context_portlets_configuration
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.zodb import volatile_property

__docformat__ = 'restructuredtext'


#
# Movie theater calendar pages
#

class MovieTheaterCalendarPageMixin:
    """Movie theater calendar page mixin class"""

    @volatile_property
    def can_inherit(self):
        return False


@factory_config(IMovieTheaterCalendarPortalPage)
class MovieTheaterCalendarPortalPage(MovieTheaterCalendarPageMixin, PortalPage):
    """Movie theater calendar portal page"""


@adapter_config(name='calendar',
                required=IMovieTheater,
                provides=IPortalPage)
def movie_theater_calendar_page(context, page_name='calendar'):
    """Movie theater calendar page factory"""

    def set_page_name(page):
        """Set page name after creation"""
        page.name = page_name

    key = f'{PORTAL_PAGE_KEY}::{page_name}' if page_name else PORTAL_PAGE_KEY
    return get_annotation_adapter(context, key, IMovieTheaterCalendarPortalPage,
                                  name=f'++page++{page_name}',
                                  callback=set_page_name)


@adapter_config(name='calendar',
                required=IMovieTheater,
                provides=IPortalPortletsConfiguration)
def movie_theater_calendar_portlets_configuration(context):
    """Movie theater calendar portlets configuration"""
    return portal_context_portlets_configuration(context, page_name='calendar')


#
# Movie theater movies list pages
#

class MovieTheaterMoviesPageMixin:
    """Movie theater movies list page mixin class"""

    @volatile_property
    def can_inherit(self):
        return False


@factory_config(IMovieTheaterMoviesPortalPage)
class MovieTheaterMoviesPortalPage(MovieTheaterMoviesPageMixin, PortalPage):
    """Movie theater movies list portal page"""


@adapter_config(name='movies',
                required=IMovieTheater,
                provides=IPortalPage)
def movie_theater_movies_page(context, page_name='movies'):
    """Movie theater movies list page factory"""

    def set_page_name(page):
        """Set page name after creation"""
        page.name = page_name

    key = f'{PORTAL_PAGE_KEY}::{page_name}' if page_name else PORTAL_PAGE_KEY
    return get_annotation_adapter(context, key, IMovieTheaterMoviesPortalPage,
                                  name=f'++page++{page_name}',
                                  callback=set_page_name)


@adapter_config(name='movies',
                required=IMovieTheater,
                provides=IPortalPortletsConfiguration)
def movie_theater_movies_portlets_configuration(context):
    """Movie theater movies list portlets configuration"""
    return portal_context_portlets_configuration(context, page_name='movies')


#
# Movie theater catalog entries pages
#

class MovieTheaterCatalogPageMixin:
    """Movie theater catalog page mixin class"""

    @volatile_property
    def can_inherit(self):
        return False


@factory_config(IMovieTheaterCatalogPortalPage)
class MovieTheaterCatalogPortalPage(MovieTheaterCatalogPageMixin, PortalPage):
    """Movie theater catalog portal page"""


@adapter_config(name='catalog',
                required=IMovieTheater,
                provides=IPortalPage)
def movie_theater_catalog_page(context, page_name='catalog'):
    """Movie theater catalog page factory"""

    def set_page_name(page):
        """Set page name after creation"""
        page.name = page_name

    key = f'{PORTAL_PAGE_KEY}::{page_name}' if page_name else PORTAL_PAGE_KEY
    return get_annotation_adapter(context, key, IMovieTheaterCatalogPortalPage,
                                  name=f'++page++{page_name}',
                                  callback=set_page_name)


@adapter_config(name='catalog',
                required=IMovieTheater,
                provides=IPortalPortletsConfiguration)
def movie_theater_catalog_portlets_configuration(context):
    """Movie theater catalog portlets configuration"""
    return portal_context_portlets_configuration(context, page_name='catalog')
