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

from zope.annotation import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.schema import Bool, Int, Object, Text, TextLine

from pyams_app_msc.component.contact import IContact

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


AUDIENCES_VOCABULARY = 'msc.theater.audiences'


class ICinemaAudience(IAttributeAnnotatable):
    """Cinema audience interface"""

    active = Bool(title=_("Active audience?"),
                  description=_("An inactive audience can't be assigned to new activities"),
                  required=True,
                  default=True)

    name = TextLine(title=_("Audience name"),
                    description=_("This name should be unique for each theater audience..."),
                    required=True)

    age_min = Int(title=_("Minimal age"),
                  description=_("This is the minimal age of the audience"),
                  required=False)

    age_max = Int(title=_("Maximal age"),
                  description=_("This is the maximal age of the audience"),
                  required=False)

    comment = Text(title=_("Comments"),
                   description=_("Additional comments"),
                   required=False)

    contact = Object(title=_("Contact"),
                     schema=IContact,
                     required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("This comment is for internal use only"),
                   required=False)


CINEMA_AUDIENCE_CONTAINER_KEY = 'msc.audience.container'


class ICinemaAudienceContainer(IContainer):
    """Cinema audience container interface"""

    contains(ICinemaAudience)

    def append(self, item):
        """Add audience to container"""

    def get_active_items(self):
        """Get iterator over active items"""


class ICinemaAudienceContainerTarget(IAttributeAnnotatable):
    """Cinema audience container target marker interface"""
