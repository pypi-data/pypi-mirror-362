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


__docformat__ = 'restructuredtext'


class ICinemaRoomsTable(Interface):
    """Cinema rooms table marker interface"""


class ICinemaPricesTable(Interface):
    """Cinema prices table marker interface"""


class ICinemaAudiencesTable(Interface):
    """Cinema audiences table marker interface"""


class IMovieTheaterCalendarPresentationMenu(Interface):
    """Movie theater calendar presentation menu marker interface"""


class IMovieTheaterMoviesPresentationMenu(Interface):
    """Movie theater movies presentation menu marker interface"""


class IMovieTheaterCatalogPresentationMenu(Interface):
    """Movie theater catalog presentation menu marker interface"""
