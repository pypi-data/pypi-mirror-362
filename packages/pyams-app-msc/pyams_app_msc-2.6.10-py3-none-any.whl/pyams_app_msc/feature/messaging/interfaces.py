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
from zope.schema import Choice, TextLine

from pyams_mail.interfaces import MAILERS_VOCABULARY_NAME

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


MESSAGING_SETTINGS_KEY = 'msc.messaging'


class IMessagingSettings(Interface):
    """Server messaging settings interface"""

    mailer_name = Choice(title=_("Selected mailer"),
                         description=_("Mail delivery utility used to send mails"),
                         required=False,
                         vocabulary=MAILERS_VOCABULARY_NAME)

    def get_mailer(self):
        """Mailer utility getter"""

    source_name = TextLine(title=_("Source name"),
                           description=_("Name used as messages sender name"),
                           required=False)

    source_address = TextLine(title=_("Source address"),
                              description=_("Email address used as messages sender source"),
                              required=False)

    subject_prefix = TextLine(title=_("Subject prefix"),
                              description=_("This prefix, if any, will be used as subject prefix "
                                            "to all sent email messages"),
                              required=False)
