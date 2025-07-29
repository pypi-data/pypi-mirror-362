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

from datetime import time

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.schema import Bool, Int, Text, TextLine, Time

from pyams_app_msc import _


ROOMS_TITLE_VOCABULARY = 'msc.theater.rooms.title'
ROOMS_SEATS_VOCABULARY = 'msc.theater.rooms.seats'


class ICinemaRoom(IAttributeAnnotatable):
    """Cinema room interface"""

    active = Bool(title=_("Active room?"),
                  description=_("An inactive room can't be selected to assign new activities"),
                  required=True,
                  default=True)

    name = TextLine(title=_("Room name or number"),
                    description=_("This name should be unique inside a single theater..."),
                    required=True)

    capacity = Int(title=_("Capacity"),
                   description=_("Maximum number or seats available in this room"),
                   required=True,
                   min=0)

    start_time = Time(title=_("Opening time"),
                      description=_("First time available for sessions planning"),
                      required=True,
                      default=time(hour=8))

    end_time = Time(title=_("Closing time"),
                    description=_("Last time available for sessions planning"),
                    required=True,
                    default=time(hour=23, minute=59))

    notepad = Text(title=_("Notepad"),
                   description=_("This comment is for internal use only"),
                   required=False)


CINEMA_ROOM_CONTAINER_KEY = 'msc.room.container'


class ICinemaRoomContainer(IContainer):
    """Cinema room container interface"""

    contains(ICinemaRoom)

    def append(self, item):
        """Add room to container"""

    def get_active_items(self):
        """Get iterator over active items"""


class ICinemaRoomContainerTarget(IAttributeAnnotatable):
    """Cinema room container target marker interface"""
