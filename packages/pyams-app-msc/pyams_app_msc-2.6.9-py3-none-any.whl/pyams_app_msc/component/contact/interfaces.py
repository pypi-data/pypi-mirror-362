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
from zope.schema import TextLine

from pyams_utils.schema import MailAddressField

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class IContact(Interface):
    """Contact interface"""

    name = TextLine(title=_("Full name"),
                    description=_("Contact full name"),
                    required=False)

    email_address = MailAddressField(title=_("Email address"),
                                     description=_("Contact email address"),
                                     required=False)

    phone_number = TextLine(title=_("Phone number"),
                            description=_("Contact phone number"),
                            required=False)
