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
from datetime import datetime, timezone

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Ge, Le, Not, Or
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.portlet.interfaces import IMovieTheaterCarouselPortletSettings, THEATERS_ORDER
from pyams_catalog.query import CatalogResultSet, IsNone
from pyams_i18n.interfaces import II18n
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config, get_interface_base_name
from pyams_utils.list import random_iter
from pyams_utils.registry import get_utility
from pyams_utils.request import query_request

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


MOVIE_THEATER_CAROUSEL_PORTLET_NAME = 'msc.portlet.theater.carousel'
MOVIE_THEATER_CAROUSEL_ICON_CLASS = 'far fa-images'


@factory_config(IMovieTheaterCarouselPortletSettings)
class MovieTheaterCarouselPortletSettings(PortletSettings):
    """Movie theater carousel portlet settings"""

    title = FieldProperty(IMovieTheaterCarouselPortletSettings['title'])
    theaters_order = FieldProperty(IMovieTheaterCarouselPortletSettings['theaters_order'])

    @property
    def theaters(self):
        """Movie theaters iterator"""
        catalog = get_utility(ICatalog)
        now= datetime.now(timezone.utc)
        query = And(Eq(catalog['object_types'], get_interface_base_name(IMovieTheater)),
                    Le(catalog['effective_date'], now),
                    Or(IsNone(catalog['expiration_date']),
                       Not(Ge(catalog['expiration_date'], now))))
        if self.theaters_order == THEATERS_ORDER.RANDOM.value:
            initial_set = CatalogResultSet(CatalogQuery(catalog).query(query))
            results_set = random_iter(initial_set, limit=len(initial_set))
        else:
            request = query_request()
            results_set = sorted(CatalogResultSet(CatalogQuery(catalog).query(query)),
                                 key=lambda x: II18n(x).query_attribute('title', request=request))
        yield from results_set


@portlet_config(permission=None)
class MovieTheaterCarouselPortlet(Portlet):
    """Movie theater carousel portlet"""

    name = MOVIE_THEATER_CAROUSEL_PORTLET_NAME
    label = _("MSC: Movie theaters list")

    settings_factory = IMovieTheaterCarouselPortletSettings
    toolbar_css_class = MOVIE_THEATER_CAROUSEL_ICON_CLASS
