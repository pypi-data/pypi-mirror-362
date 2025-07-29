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

from collections import OrderedDict
from enum import Enum

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.interface import Attribute, Invalid, invariant
from zope.schema import Bool, Choice, Datetime, Int, Text, TextLine
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_app_msc.component.address import IAddress
from pyams_app_msc.shared.theater.interfaces.price import PRICES_VOCABULARY
from pyams_file.schema import FileField
from pyams_scheduler.interfaces import ITask
from pyams_security.schema import PrincipalField
from pyams_utils.schema import HTMLField

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class BOOKING_STATUS(Enum):
    """Booking status"""
    WAITING = 'waiting'
    CANCELLED = 'cancelled'
    REFUSED = 'refused'
    OPTION = 'option'
    ACCEPTED = 'accepted'


BOOKING_CANCELLABLE_STATUS = {
    BOOKING_STATUS.WAITING.value,
    BOOKING_STATUS.REFUSED.value,
    BOOKING_STATUS.OPTION.value,
    BOOKING_STATUS.ACCEPTED.value
}

BOOKING_OPTIONABLE_STATUS = {
    BOOKING_STATUS.WAITING.value,
    BOOKING_STATUS.CANCELLED.value,
    BOOKING_STATUS.REFUSED.value,
    BOOKING_STATUS.ACCEPTED.value
}

BOOKING_REFUSABLE_STATUS = {
    BOOKING_STATUS.WAITING.value,
    BOOKING_STATUS.OPTION.value
}

BOOKING_ACCEPTABLE_STATUS = {
    BOOKING_STATUS.WAITING.value,
    BOOKING_STATUS.CANCELLED.value,
    BOOKING_STATUS.REFUSED.value,
    BOOKING_STATUS.OPTION.value
}


BOOKING_STATUS_LABEL = OrderedDict((
    (BOOKING_STATUS.WAITING, _("Waiting")),
    (BOOKING_STATUS.CANCELLED, _("Cancelled")),
    (BOOKING_STATUS.REFUSED, _("Refused")),
    (BOOKING_STATUS.OPTION, _("Optional")),
    (BOOKING_STATUS.ACCEPTED, _("Accepted"))
))


BOOKING_STATUS_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in BOOKING_STATUS_LABEL.items()
])


REQUESTED_BOOKING_STATUS = {
    BOOKING_STATUS.WAITING.value,
    BOOKING_STATUS.OPTION.value,
    BOOKING_STATUS.ACCEPTED.value
}

OCCUPIED_BOOKING_STATUS = {
    BOOKING_STATUS.ACCEPTED.value
}


BOOKING_SESSIONS_VOCABULARY = 'msc.booking_sessions'


class IBookingInfo(IAttributeAnnotatable):
    """Booking information interface

    This interface defines properties of a single booking.
    """

    creator = PrincipalField(title=_("Creator"),
                             description=_("Name of the principal who created the booking"),
                             required=True)

    recipient = PrincipalField(title=_("Recipient"),
                               description=_("Name of the principal for which the booking is done"),
                               required=True)

    recipient_establishment = TextLine(title="Recipient establishment memo",
                                       description=_("Recipient establishment is memoized into "
                                                     "booking properties when the booking is archived..."),
                                       required=False)

    def get_recipient(self, with_info=True):
        """Recipient principal getter"""

    status = Choice(title=_("Status"),
                    vocabulary=BOOKING_STATUS_VOCABULARY,
                    required=False,
                    default=BOOKING_STATUS.WAITING.value)

    nb_participants = Int(title=_("Participants"),
                          description=_("Number of participants seats reserved for this session"),
                          required=True,
                          min=0)

    participants_age = Text(title=_("Participants age"),
                            description=_("Please let us know the age of the participants so that we "
                                          "can welcome them more easily"),
                            required=True)

    nb_accompanists = Int(title=_("Accompanists"),
                          description=_("Total number of accompanists seats reserved for this session"),
                          required=True,
                          min=0)

    nb_seats = Int(title=_("Total participants"),
                   description=_("Total number of participants reserved for this session"),
                   readonly=True)
    
    nb_free_accompanists = Int(title=_("Free accompanists"),
                               description=_("Number of free accompanists seats reserved for this session"),
                               required=True,
                               min=0,
                               default=0)
    
    @invariant
    def check_nb_accompanists(self):
        if self.nb_free_accompanists > self.nb_accompanists:
            raise Invalid(_("Number of free accompanists can't be higher than total number of accompanists!"))

    accompanying_ratio = Int(title=_("Accompanying ratio"),
                             description=_("You can set an integer number which will define the count of "
                                           "participants for which one accompanying person will have free access"),
                             default=0,
                             min=0,
                             required=False)

    nb_groups = Int(title=_("Groups count"),
                    description=_("Number of groups or classrooms attending this session"),
                    required=True,
                    min=1,
                    default=1)

    price = Choice(title=_("Price"),
                   description=_("Price applied to this booking"),
                   vocabulary=PRICES_VOCABULARY,
                   required=False)

    def get_price(self):
        """Price instance getter"""

    cultural_pass = Bool(title=_("Cultural pass"),
                         description=_("Check this option if payment is done using cultural pass"),
                         required=True,
                         default=False)

    comments = Text(title=_("Comments"),
                    description=_("These comments where added by booking recipient"),
                    required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("These comments are for internal use only"),
                   required=False)

    archived = Bool(title=_("Archived"),
                    description=_("A booking is archived automatically after session end and "
                                  "can't be modified anymore"),
                    required=True,
                    default=False)

    session = Attribute("Booking session")

    session_index = Attribute("Booking session index value")

    def set_session(self, new_session):
        """Update booking session"""

    def get_quotation(self, force_refresh=False, store=True, **kwargs):
        """Create quotation document from booking information"""

    quotation_number = TextLine(title=_("Quotation number"),
                                description=_("This is the reference number of the quotation"),
                                required=False)

    quotation_message = Text(title=_("Quotation message"),
                             description=_("This message is added to quotation as an information message"),
                             required=False)

    quotation = FileField(title=_("Quotation"),
                          description=_("This quotation was attached to booking confirmation"),
                          required=False)

    send_update = Bool(title=_("Send update message?"),
                       description=_("If 'yes', a message will be sent to the recipient "),
                       required=True,
                       default=False)

    update_subject = TextLine(title=_("Update subject"),
                              description=_("Subject of update message sent to the recipient"),
                              required=False)

    update_message = HTMLField(title=_("Update message"),
                               description=_("Update message will be sent to the recipient if booking "
                                             "properties are changed..."),
                               required=False)

    send_reminder = Bool(title=_("Send reminder?"),
                         description=_("If 'yes', a reminder message will be sent to the recipient a few "
                                       "days before the session take place; delay before session is defined "
                                       "into theater settings"),
                         required=False,
                         default=True)

    reminder_subject = TextLine(title=_("Reminder subject"),
                                description=_("Subject of reminder message sent to the recipient"),
                                required=False)

    reminder_message = HTMLField(title=_("Reminder message"),
                                 description=_("Reminder message will be sent to the recipient a few days before "
                                               "the session take place; delay before session is defined into "
                                               "theater settings"),
                                 required=False)

    reminder_date = Datetime(title=_("Reminder date"),
                             description=_("Date and time at which reminder message was sent"),
                             required=False)

    def send_request_notification_message(self, audience, view):
        """Send request notification message to movie operator"""

    def send_reminder_message(self):
        """Send reminder message to booking recipient"""


class IBookingAcceptInfo(IBookingInfo):
    """Booking accept info interface"""

    accepted = Bool(title=_("Accept booking"),
                    required=True,
                    default=False)


class IBaseBookingWorkflowInfo(IBookingInfo):
    """Base booking workflow info interface"""

    created = Datetime(title=_("Creation date"),
                       description=_("Date at which the booking was created"),
                       required=False)

    notify_recipient = Bool(title=_("Notify recipient?"),
                            description=_("If 'yes', a notification message will be sent to the recipient"),
                            required=False,
                            default=True)

    notify_subject = TextLine(title=_("Notification subject"),
                              description=_("Subject of notification message sent to the recipient"),
                              required=False)

    notify_message = HTMLField(title=_("Notification message"),
                               description=_("Notification message sent to the recipient"),
                               required=False)


class IAcceptedBookingWorkflowInfo(IBaseBookingWorkflowInfo):
    """Accepted booking workflow interface"""

    include_quotation = Bool(title=_("Include quotation"),
                             description=_("Include quotation document into notification message"),
                             required=False,
                             default=True)

    quotation_message = Text(title=_("Quotation message"),
                             description=_("This message will be added to quotation"),
                             required=False)


#
# Booking container
#

BOOKING_CONTAINER_KEY = 'msc.booking'


class IBookingContainer(IContainer):
    """Booking manager interface

    This interface is an :py:class:`IBookingInfo` container.
    """

    contains(IBookingInfo)

    session = Attribute("Booking session")

    def append(self, booking):
        """Add booking to container"""

    def get_requested_seats(self):
        """Get number of requested seats"""

    def get_waiting_seats(self):
        """Get number of waiting seats"""

    def get_confirmed_seats(self):
        """Get number of confirmed reserved seats"""

    free_seats = Int(title=_("Free seats"),
                     description=_("Number of free seats for this session"),
                     readonly=True)

    def get_seats(self, display_mode):
        """Get total number of seats according to given display mode"""


class IBookingTarget(IAttributeAnnotatable):
    """Booking target marker interface"""


class IBookingReminderTask(ITask):
    """Booking reminder task interface"""


class IBookingArchiverTask(ITask):
    """Booking archiver task interface"""
