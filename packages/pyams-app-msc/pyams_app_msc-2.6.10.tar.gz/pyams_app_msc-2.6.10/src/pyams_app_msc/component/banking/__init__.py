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

from pyams_app_msc.component.banking.interfaces import IBankingAccount
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'


@factory_config(IBankingAccount)
class BankingAccount(Persistent):
    """Banking account persistent class"""

    company_name = FieldProperty(IBankingAccount['company_name'])
    bank_code = FieldProperty(IBankingAccount['bank_code'])
    counter_code = FieldProperty(IBankingAccount['counter_code'])
    account_number = FieldProperty(IBankingAccount['account_number'])
    account_key = FieldProperty(IBankingAccount['account_key'])
    iban_number = FieldProperty(IBankingAccount['iban_number'])
    bic_code = FieldProperty(IBankingAccount['bic_code'])
