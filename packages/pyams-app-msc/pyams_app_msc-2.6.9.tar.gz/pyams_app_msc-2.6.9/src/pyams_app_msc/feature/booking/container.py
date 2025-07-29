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

from pyramid.httpexceptions import HTTPNotFound
from zope.container.btree import BTreeContainer
from zope.interface import classImplements
from zope.location.interfaces import ISublocations
from zope.traversing.interfaces import ITraversable
from ZODB.interfaces import IConnection

from pyams_app_msc.feature.booking import BOOKING_STATUS
from pyams_app_msc.feature.booking.interfaces import BOOKING_CONTAINER_KEY, IBookingContainer, \
    IBookingTarget, OCCUPIED_BOOKING_STATUS, REQUESTED_BOOKING_STATUS
from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.feature.planning.session import Session
from pyams_app_msc.feature.profile.interfaces import SEATS_DISPLAY_MODE
from pyams_catalog.utils import index_object
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.traversing import get_parent
from pyams_utils.zodb import volatile_property

__docformat__ = 'restructuredtext'


@factory_config(IBookingContainer)
class BookingContainer(BTreeContainer):
    """Booking container"""

    @volatile_property
    def session(self):
        """Booking session getter"""
        return get_parent(self, IBookingTarget)

    def append(self, booking):
        """Add booking to container"""
        IConnection(self).add(booking)
        key = ICacheKeyValue(booking)
        self[key] = booking
        index_object(booking)

    def get_requested_seats(self):
        """Get number of requested seats"""
        return sum((
            booking.nb_seats
            for booking in self.values()
            if booking.status in REQUESTED_BOOKING_STATUS
        ))

    def get_waiting_seats(self):
        """Get number of waiting seats"""
        return sum((
            booking.nb_seats
            for booking in self.values()
            if booking.status == BOOKING_STATUS.WAITING.value
        ))

    def get_confirmed_seats(self):
        """Get number of confirmed reserved seats"""
        return sum((
            booking.nb_seats
            for booking in self.values()
            if booking.status in OCCUPIED_BOOKING_STATUS
        ))

    @property
    def free_seats(self):
        """Free seats getter"""
        return (self.session.capacity or 0) - self.get_confirmed_seats()

    def get_seats(self, display_mode):
        """Get total number of seats according to given display mode"""
        if display_mode == SEATS_DISPLAY_MODE.TOTAL.value:
            return (f'{self.get_confirmed_seats()} / '
                    f'{self.get_requested_seats()} / '
                    f'{self.session.capacity}')
        if display_mode == SEATS_DISPLAY_MODE.FREE.value:
            return (f'{self.get_confirmed_seats()} / '
                    f'{self.get_requested_seats()} / '
                    f'{self.free_seats}')
        if display_mode == SEATS_DISPLAY_MODE.WAITING.value:
            return (f'{self.get_confirmed_seats()} / '
                    f'{self.get_waiting_seats()} / '
                    f'{self.session.capacity}')
        if display_mode == SEATS_DISPLAY_MODE.CONFIRMED.value:
            return (f'{self.get_confirmed_seats()} / '
                    f'{self.session.capacity}')
        return (f'{self.get_confirmed_seats()} / '
                f'{self.free_seats}')


@adapter_config(required=IBookingTarget,
                provides=IBookingContainer)
def session_booking_container(context):
    """Session booking container adapter"""
    return get_annotation_adapter(context, BOOKING_CONTAINER_KEY, IBookingContainer,
                                  name='++booking++')


@adapter_config(required=IBookingContainer,
                provides=ISession)
def booking_container_session(context):
    """Booking container session adapter"""
    return context.session


@adapter_config(name='booking',
                required=IBookingTarget,
                provides=ITraversable)
class BookingTraverser(ContextAdapter):
    """Booking target traverser"""

    def traverse(self, name, furtherPath=None):
        """Traverse to inner bookings container"""
        container = IBookingContainer(self.context, None)
        if container is not None:
            return container
        raise HTTPNotFound


@adapter_config(name='booking',
                required=IBookingTarget,
                provides=ISublocations)
class BookingSublocations(ContextAdapter):
    """Booking sub-locations"""

    def sublocations(self):
        """Booking target sub-locations getter"""
        container = IBookingContainer(self.context, None)
        if container is not None:
            yield from container.values()


classImplements(Session, IBookingTarget)
