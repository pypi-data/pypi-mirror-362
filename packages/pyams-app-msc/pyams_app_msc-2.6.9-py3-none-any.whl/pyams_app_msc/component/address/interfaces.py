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
from zope.schema import Text, TextLine

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class IAddress(Interface):
    """Address interface"""

    street = TextLine(title=_("Number and street"),
                      description=_("Entry number and street name"),
                      required=False)

    locality = TextLine(title=_("Locality"),
                        required=False)

    postal_code = TextLine(title=_("Postal code"),
                           required=True)

    city = TextLine(title=_("City"),
                    required=True)

    comments = Text(title=_("Comments"),
                    description=_("Optional observations which can be added to describe the location"),
                    required=False)
