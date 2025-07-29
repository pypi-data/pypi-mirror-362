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

from pyams_app_msc.component.contact.interfaces import IContact
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'


@factory_config(IContact)
class Contact(Persistent):
    """Contact persistent class"""

    name = FieldProperty(IContact['name'])
    email_address = FieldProperty(IContact['email_address'])
    phone_number = FieldProperty(IContact['phone_number'])

    def __bool__(self):
        return bool(self.name or self.email_address)
