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

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.component.address.interfaces import IAddress
from pyams_utils.factory import factory_config


__docformat__ = 'restructuredtext'


@factory_config(IAddress)
class Address(Persistent):
    """Address persistent class"""

    street = FieldProperty(IAddress['street'])
    locality = FieldProperty(IAddress['locality'])
    postal_code = FieldProperty(IAddress['postal_code'])
    city = FieldProperty(IAddress['city'])
    comments = FieldProperty(IAddress['comments'])
