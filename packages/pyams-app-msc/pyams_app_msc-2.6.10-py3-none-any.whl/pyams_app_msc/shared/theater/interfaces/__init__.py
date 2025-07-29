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

from zope.container.constraints import containers
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Float, Int, Object, Text, TextLine, URI
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_app_msc.component.address.interfaces import IAddress
from pyams_app_msc.component.admininfo.interfaces import IAdminInfo
from pyams_app_msc.component.banking.interfaces import IBankingAccount
from pyams_app_msc.interfaces import MSC_CONTRIBUTOR_ROLE, MSC_MANAGER_ROLE, MSC_OPERATOR_ROLE, MSC_READER_ROLE
from pyams_content.component.paragraph import IParagraphContainerTarget
from pyams_content.shared.common.interfaces import DEFAULT_CONTENT_WORKFLOW, IBaseSharedTool, IDeletableElement
from pyams_file.schema import FileField, ImageField
from pyams_i18n.schema import I18nTextField
from pyams_portal.interfaces import DESIGNER_ROLE, IPortalPage
from pyams_security.schema import PrincipalsSetField
from pyams_sequence.interfaces import ISequentialIdTarget
from pyams_site.interfaces import ISiteRoot
from pyams_utils.schema import ColorField, MailAddressField
from pyams_workflow.interfaces import IWorkflowPublicationSupport, WORKFLOWS_VOCABULARY

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


#
# Movie theater interfaces
#

MSC_THEATERS_VOCABULARY = 'msc.theaters'


class IMovieTheater(IBaseSharedTool, IDeletableElement, ISequentialIdTarget,
                    IParagraphContainerTarget, IWorkflowPublicationSupport):
    """Movie theater interface"""

    containers(ISiteRoot)

    header = I18nTextField(title=_("Header"),
                           description=_("Site's header is generally displayed in page header"),
                           required=False)

    description = I18nTextField(title=_("Meta-description"),
                                description=_("The site's description is 'hidden' into HTML's "
                                              "page headers; but it can be seen, for example, "
                                              "in some search engines results as content's "
                                              "description; if description is empty, content's "
                                              "header will be used."),
                                required=False)

    shared_content_workflow = Choice(title=_("Workflow name"),
                                     description=_("Name of workflow utility used to manage tool "
                                                   "contents"),
                                     vocabulary=WORKFLOWS_VOCABULARY,
                                     default=DEFAULT_CONTENT_WORKFLOW)

    shared_content_type = Attribute("Shared data content type name")

    logo = ImageField(title=_("Logo"),
                      description=_("This image will be used in documents and email messages"),
                      required=False)

    address = Object(title=_("Address"),
                     description=_("Full theater address"),
                     schema=IAddress,
                     required=False)

    web_address = URI(title=_("Website address"),
                      description=_("URL of theater web site"),
                      required=False)

    contact_email = MailAddressField(title=_("Contact email"),
                                     required=False)

    phone_number = TextLine(title=_("Phone number"),
                            required=False)

    banking_account = Object(title=_("Banking account"),
                             schema=IBankingAccount,
                             required=False)

    admin_info = Object(title=_("Administrative information"),
                        schema=IAdminInfo,
                        required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("Internal information to be known about this content"),
                   required=False)


MOVIE_THEATER_ROLES = 'msc.theater.roles'


class IMovieTheaterRoles(Interface):
    """Movie theater roles interface"""

    msc_managers = PrincipalsSetField(title=_("Managers"),
                                      description=_("Managers can manage all theater configuration and properties"),
                                      role_id=MSC_MANAGER_ROLE,
                                      required=False)

    msc_operators = PrincipalsSetField(title=_("Operators"),
                                       description=_("Operators can manage theater activities catalog, and "
                                                     "reservations"),
                                       role_id=MSC_OPERATOR_ROLE,
                                       required=False)

    msc_contributors = PrincipalsSetField(title=_("Contributors"),
                                          description=_("Contributors can add activities to theater catalog, but "
                                                        "can't publish them"),
                                          role_id=MSC_CONTRIBUTOR_ROLE,
                                          required=False)

    msc_designers = PrincipalsSetField(title=_("Designers"),
                                       description=_("Designers are users which are allowed to "
                                                     "manage presentation templates"),
                                       role_id=DESIGNER_ROLE,
                                       required=False)

    msc_readers = PrincipalsSetField(title=_("Readers"),
                                     description=_("Readers are guest users which can only view theater properties "
                                                   "and activities catalog"),
                                     role_id=MSC_READER_ROLE,
                                     required=False)


MOVIE_THEATER_SETTINGS_KEY = 'msc.theater.settings'


class CALENDAR_DAYS(Enum):
    """Calendar days enumeration"""
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


CALENDAR_FIRST_DAY = OrderedDict((
    (CALENDAR_DAYS.SUNDAY, _("Sunday")),
    (CALENDAR_DAYS.MONDAY, _("Monday")),
    (CALENDAR_DAYS.TUESDAY, _("Tuesday")),
    (CALENDAR_DAYS.WEDNESDAY, _("Wednesday")),
    (CALENDAR_DAYS.THURSDAY, _("Thursday")),
    (CALENDAR_DAYS.FRIDAY, _("Friday")),
    (CALENDAR_DAYS.SATURDAY, _("Saturday"))
))


CALENDAR_FIRST_DAY_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in CALENDAR_FIRST_DAY.items()
])


class SESSION_REQUEST_MODE(Enum):
    """Session request modes"""
    FORM = 'form'
    MAILTO = 'mailto'


SESSION_REQUEST_MODE_LABEL = OrderedDict((
    (SESSION_REQUEST_MODE.FORM, _('Use site form')),
    (SESSION_REQUEST_MODE.MAILTO, _('Use mailto link'))
))


SESSION_REQUEST_MODE_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in SESSION_REQUEST_MODE_LABEL.items()
])


class BOOKING_CANCEL_MODE(Enum):
    """Booking cancel modes"""
    FORBIDDEN = 'forbidden'
    MAX_DELAY = 'max-delay'
    NOTICE_PERIOD = 'notice-period'


BOOKING_CANCEL_MODE_LABEL = OrderedDict((
    (BOOKING_CANCEL_MODE.FORBIDDEN, _("Forbidden cancellation")),
    (BOOKING_CANCEL_MODE.MAX_DELAY, _("Max delay after booking")),
    (BOOKING_CANCEL_MODE.NOTICE_PERIOD, _("Minimum notice period before session"))
))


BOOKING_CANCEL_MODE_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in BOOKING_CANCEL_MODE_LABEL.items()
])


class IMovieTheaterSettings(Interface):
    """Movie theater settings"""

    calendar_first_day = Choice(title=_("Calendar first week day"),
                                description=_("First week day used in calendars"),
                                vocabulary=CALENDAR_FIRST_DAY_VOCABULARY,
                                required=False,
                                default=CALENDAR_DAYS.SUNDAY.value)

    calendar_slot_duration = Int(title=_("Calendar slot duration"),
                                 description=_("Calendar time slots frequency in week or day views"),
                                 required=False,
                                 min=5,
                                 max=60,
                                 default=30)

    default_session_duration = Int(title=_("Default session duration"),
                                   description=_("This is a default duration, in minutes, of sessions for "
                                                 "which activity has no duration"),
                                   required=False,
                                   default=120)

    session_duration_delta = Int(title=_("Session duration delta"),
                                 description=_("This is a number of minutes which will be added automatically "
                                               "to activities duration when adding new sessions"),
                                 required=False,
                                 default=0)

    allow_session_request = Bool(title=_('Allow session request'),
                                 description=_('When enabled, external partners will be allowed to '
                                               'send requests for new sessions'),
                                 required=True,
                                 default=True)

    session_request_mode = Choice(title=_("Session request mode"),
                                  description=_(""),
                                  required=True,
                                  vocabulary=SESSION_REQUEST_MODE_VOCABULARY,
                                  default=SESSION_REQUEST_MODE.FORM.value)

    reminder_delay = Int(title=_("Reminder delay"),
                         description=_("This is a delay, given in days before a session beginning, at which "
                                       "a reminder message can be sent to booking recipients; leave value "
                                       "empty or set it to 0 to disable reminders messages"),
                         required=False)

    booking_cancel_mode = Choice(title=_("User booking cancel mode"),
                                 description=_("This mode determines how and when a principal can cancel "
                                               "a booking by it's own way"),
                                 vocabulary=BOOKING_CANCEL_MODE_VOCABULARY,
                                 required=True,
                                 default=BOOKING_CANCEL_MODE.FORBIDDEN.value)

    booking_cancel_max_delay = Int(title=_("Cancel max delay"),
                                   description=_("This is the maximum period length after user booking, "
                                                 "given in hours, during which a principal can cancel a "
                                                 "booking by it's own way"),
                                   required=False,
                                   min=0)

    booking_cancel_notice_period = Int(title=_("Cancel notice period"),
                                       description=_("This is the minimum amount of time before session, "
                                                     "given in hours, during which a principal can cancel "
                                                     "a booking by it's own way"),
                                       required=False,
                                       min=0)

    booking_retention_duration = Int(title=_("Booking retention duration"),
                                     description=_("This is the minimum amount of time, given in hours, during which a "
                                                   "a booking is kept 'active' before being archived"),
                                     required=False,
                                     min=0,
                                     default=24)

    quotation_number_format = TextLine(title=_("Quotation number format"),
                                       description=_("This number will be used as formatting string to "
                                                     "create quotations numbers; you can use date elements "
                                                     "like {yyyy} for current year in long format, {yy} for current "
                                                     "year in short format, {mm} for current month, {dd} for current "
                                                     "date, {yinc} for year increment, {minc} for month increment and "
                                                     "{operator} for operator initials"),
                                       default='PREFIX-{yyyy}{yinc}',
                                       required=False)

    quotation_email = MailAddressField(title=_("Quotation email address"),
                                       description=_("If set, this address will be used on quotations instead of "
                                                     "general theater contact email"),
                                       required=False)

    quotation_logo = FileField(title=_("Quotation logo"),
                               description=_("This image will be displayed in quotations headers"),
                               required=False)

    def get_logo_color(self):
        """Extract median color from logo"""

    quotation_color = ColorField(title=_("Base color"),
                                 description=_("This color will be used as base color for graphic elements "
                                               "displayed in quotations"),
                                 required=False)

    currency = TextLine(title=_("Currency"),
                        description=_("This is the currency used for all transactions"),
                        required=False)

    vat_rate = Float(title=_("VAT rate"),
                     description=_("This is the VAT rate which will be used in quotations"),
                     required=False)

    def get_quotation_number(self):
        """Get new quotation number"""

    def get_quotation_color(self):
        """Get base quotation color"""


class IMovieTheaterCalendarPortalPage(IPortalPage):
    """Movie theater calendar portal page marker interface"""


class IMovieTheaterMoviesPortalPage(IPortalPage):
    """Movie theater movies list portal page marker interface"""


class IMovieTheaterCatalogPortalPage(IPortalPage):
    """Movie theater catalog portal page marker interface"""
