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

__docformat__ = 'restructuredtext'

from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.component.admininfo.interfaces import IAdminInfo
from pyams_utils.factory import factory_config


@factory_config(IAdminInfo)
class AdminInfo(Persistent):
    """Administrative info persistent class"""

    siret_code = FieldProperty(IAdminInfo['siret_code'])
    ape_code = FieldProperty(IAdminInfo['ape_code'])
    vat_number = FieldProperty(IAdminInfo['vat_number'])
