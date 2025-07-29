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

from zope.interface import Interface

from pyams_zmi.interfaces.viewlet import INavigationMenu


class IBookingContainerTable(Interface):
    """Booking target container table interface"""


class IBookingContainerView(Interface):
    """Booking target container view interface"""


class IBookingStatusTable(Interface):
    """Booking status table marker interface"""


class IBookingWaitingStatusTable(IBookingStatusTable):
    """Booking waiting status table marker interface"""


class IBookingAcceptedStatusTable(IBookingStatusTable):
    """Booking accepted status table marker interface"""


class IBookingManagementMenu(INavigationMenu):
    """Booking management menu marker interface"""


class IBookingDashboardMenu(INavigationMenu):
    """Booking dashboard menu marker interface"""


class IBookingStatusDashboardView(Interface):
    """Booking status dashboard view"""


class IBookingForm(Interface):
    """Booking form marker interface"""
