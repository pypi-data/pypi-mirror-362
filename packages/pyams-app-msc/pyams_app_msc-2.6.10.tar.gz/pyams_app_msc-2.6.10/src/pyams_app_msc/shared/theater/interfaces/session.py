# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.shared.catalog.interfaces import CATALOG_ENTRY_CONTENT_TYPE
from pyams_sequence.schema import InternalReferenceField

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class IMovieTheaterSession(ISession):
    """Movie theater session interface"""

    activity = InternalReferenceField(title=_("Activity"),
                                      description=_("You can select an existing activity from your catalog, or keep "
                                                    "this input empty if you just want to mark a period as not being "
                                                    "available for booking"),
                                      content_type=CATALOG_ENTRY_CONTENT_TYPE,
                                      required=False)
