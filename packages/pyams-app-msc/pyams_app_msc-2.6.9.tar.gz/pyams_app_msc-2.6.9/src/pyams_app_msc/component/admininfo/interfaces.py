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


__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class IAdminInfo(Interface):
    """Theater administrative information interface"""

    siret_code = TextLine(title=_("SIRET code"),
                          max_length=14,
                          required=False)

    ape_code = TextLine(title=_("APE code"),
                        max_length=5,
                        required=False)

    vat_number = TextLine(title=_("Intra-community VAT number"),
                          max_length=13,
                          required=False)
