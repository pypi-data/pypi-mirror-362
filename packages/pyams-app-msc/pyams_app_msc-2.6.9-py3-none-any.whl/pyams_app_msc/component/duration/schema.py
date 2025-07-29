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

from zope.interface import implementer
from zope.schema import Int

from pyams_app_msc.component.duration.interfaces import IDurationField

__docformat__ = 'restructuredtext'


@implementer(IDurationField)
class DurationField(Int):
    """Custom duration field"""

    def __init__(self, min=None, max=None, default=None, **kwargs):
        super().__init__(min=0, max=1440, default=default, **kwargs)
