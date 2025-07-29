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

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import Interface
from zope.schema import TextLine, Bool

from pyams_utils.schema import HTMLField

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


MAIL_TEMPLATES_KEY = 'msc.mail.templates'


class IMailTemplates(Interface):
    """Movie theater mail templates interfaces"""

    send_copy_to_sender = Bool(title=_("Send copy to operator"),
                               description=_("If 'yes', a copy of each message will be sent to operator"),
                               required=True,
                               default=False)

    cancel_subject = TextLine(title=_("Message subject"),
                              description=_("Default subject used for cancelled booking notification"),
                              required=False)

    cancel_template = HTMLField(title=_("Message template"),
                                description=_("This template is used when a session booking is cancelled"),
                                required=False)

    refuse_subject = TextLine(title=_("Message subject"),
                              description=_("Default subject used for refused booking notification"),
                              required=False)

    refuse_template = HTMLField(title=_("Message template"),
                                description=_("This template is used when a session booking is refused"),
                                required=False)

    option_subject = TextLine(title=_("Message subject"),
                              description=_("Default subject used for temporarily accepted booking"),
                              required=False)

    option_template = HTMLField(title=_("Message template"),
                                description=_("This template is used when a session booking is temporarily "
                                              "accepted but waiting for confirmation"),
                                required=False)

    accept_subject = TextLine(title=_("Message subject"),
                              description=_("Default subject used for accepted booking notification"),
                              required=False)

    accept_template = HTMLField(title=_("Message template"),
                                description=_("This template is used when a session booking is accepted"),
                                required=False)

    update_subject = TextLine(title=_("Message subject"),
                              description=_("Default subject used for updated booking notification"),
                              required=False)

    update_template = HTMLField(title=_("Message template"),
                                description=_("This template is used when a session booking is updated after "
                                              "being accepted"),
                                required=False)

    reminder_subject = TextLine(title=_("Reminder subject"),
                                description=_("Default subject used for reminder message"),
                                required=False)

    reminder_template = HTMLField(title=_("Message template"),
                                  description=_("This template is used for reminder messages which are "
                                                "sent to sessions recipients a few days before they take place"),
                                  required=False)


class IMailTemplatesTarget(IAttributeAnnotatable):
    """Cinema price container target marker interface"""
