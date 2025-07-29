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

"""PyAMS_app_msc.feature.profile.interfaces module

This module defines user profile interfaces.
"""

from enum import Enum

from zope.interface import Attribute, Interface, implementer
from zope.interface.interfaces import IObjectEvent, ObjectEvent
from zope.schema import Bool, Choice, Int, List, Object, TextLine
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_app_msc.component.address.interfaces import IAddress
from pyams_app_msc.reference.structure import STRUCTURE_TYPES_VOCABULARY
from pyams_app_msc.shared.theater.interfaces import MSC_THEATERS_VOCABULARY
from pyams_scheduler.interfaces import ITask
from pyams_utils.schema import MailAddressField

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


USER_PROFILE_KEY = 'msc.profile'


class IUserProfile(Interface):
    """User profile interface"""

    principal_id = TextLine(title="Principal ID",
                            description=_("Principal ID"),
                            required=True)

    active = Bool(title=_("Active user?"),
                  description=_("Inactive users can't login anymore to website"),
                  required=True,
                  default=True)

    firstname = TextLine(title=_("First name"),
                         required=True)

    lastname = TextLine(title=_("Last name"),
                        required=True)

    email = MailAddressField(title=_("Mail address"),
                             required=True)

    phone_number = TextLine(title=_("Phone number"),
                            required=True)

    establishment = TextLine(title=_("Establishment of affiliation"),
                             required=True)

    structure_type = Choice(title=_("Structure type"),
                            description=_("Select structure type matching this establishment"),
                            vocabulary=STRUCTURE_TYPES_VOCABULARY,
                            required=True)

    establishment_address = Object(title=_("Establishment address"),
                                   schema=IAddress,
                                   required=False)

    local_theaters = List(title=_("Preferred local theaters"),
                          value_type=Choice(vocabulary=MSC_THEATERS_VOCABULARY),
                          required=True)

    def get_structure_type(self):
        """Structure type label getter"""


class SEATS_DISPLAY_MODE(Enum):
    """Session seats display mode"""
    NONE = 'none'
    TOTAL = 'total'
    FREE = 'free'
    WAITING = 'waiting'
    CONFIRMED = 'confirmed'
    CONFIRMED_FREE = 'confirmed_free'


SEATS_DISPLAY_LABELS = {
    SEATS_DISPLAY_MODE.NONE.value: _("Not displayed"),
    SEATS_DISPLAY_MODE.TOTAL.value: _("Display confirmed/requested/capacity seats"),
    SEATS_DISPLAY_MODE.FREE.value: _("Display confirmed/requested/free seats"),
    SEATS_DISPLAY_MODE.WAITING.value: _("Display confirmed/waiting/capacity seats"),
    SEATS_DISPLAY_MODE.CONFIRMED.value: _("Display confirmed/capacity seats"),
    SEATS_DISPLAY_MODE.CONFIRMED_FREE.value: _("Display confirmed/free seats")
}


SEATS_DISPLAY_VOCABULARY = SimpleVocabulary([
    SimpleTerm(i, title=t)
    for i, t in SEATS_DISPLAY_LABELS.items()
])


OPERATOR_PROFILE_KEY = 'msc.operator'


class IOperatorProfile(Interface):
    """Operator management operator profile"""

    session_seats_display_mode = Choice(title=_("Session seats display mode"),
                                        description=_("You can choose how session seats are displayed in "
                                                      "movie theater planning view"),
                                        vocabulary=SEATS_DISPLAY_VOCABULARY,
                                        required=True,
                                        default=SEATS_DISPLAY_MODE.TOTAL.value)

    today_program_length = Int(title=_("Today program length"),
                               description=_("Number of days displayed in today program"),
                               min=1,
                               max=7,
                               required=True,
                               default=1)


class IRegisteredPrincipalEvent(IObjectEvent):
    """Registered principal event interface"""


@implementer(IRegisteredPrincipalEvent)
class RegisteredPrincipalEvent(ObjectEvent):
    """Registered principal event"""


class IActivatedPrincipalEvent(IObjectEvent):
    """Activated principal event interface"""


@implementer(IActivatedPrincipalEvent)
class ActivatedPrincipalEvent(ObjectEvent):
    """Activated principal event"""


class IUserProfileCleanerTask(ITask):
    """User profile cleaner task interface"""

    user_id = Attribute("User profile ID")
