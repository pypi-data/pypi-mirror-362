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

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.schema import Bool, Float, Int, Text, TextLine

from pyams_app_msc import _


PRICES_VOCABULARY = 'msc.theater.prices'


class ICinemaPrice(IAttributeAnnotatable):
    """Cinema price interface"""

    active = Bool(title=_("Active price?"),
                  description=_("An inactive price can't be assigned to new reservations"),
                  required=True,
                  default=True)

    name = TextLine(title=_("Price name"),
                    description=_("This name should be unique for each theater price..."),
                    required=True)

    participant_price = Float(title=_("Participant price"),
                              description=_("This is the price which is applied to each participant"),
                              required=True)

    accompanying_ratio = Int(title=_("Accompanying ratio"),
                             description=_("You can set an integer number which will define the count of "
                                           "participants for which one accompanying person will have free access; "
                                           "this ratio will still be updatable on all bookings using this price"),
                             default=0,
                             min=0,
                             required=False)

    accompanying_price = Float(title=_("Accompanying price"),
                               description=_("This is the price which is applied to each accompanying person"),
                               required=True)

    comment = Text(title=_("Comments"),
                   description=_("Additional comments"),
                   required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("This comment is for internal use only"),
                   required=False)


CINEMA_PRICE_CONTAINER_KEY = 'msc.price.container'


class ICinemaPriceContainer(IContainer):
    """Cinema price container interface"""

    contains(ICinemaPrice)

    def append(self, item):
        """Add price to container"""

    def get_active_items(self):
        """Get iterator over active items"""


class ICinemaPriceContainerTarget(IAttributeAnnotatable):
    """Cinema price container target marker interface"""
