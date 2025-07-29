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

"""PyAMS_app_msc.component.banking.interfaces module

"""

from zope.interface import Interface, Invalid, invariant
from zope.schema import TextLine

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class IBankingAccount(Interface):
    """Banking account interface"""

    company_name = TextLine(title=_("Company name"),
                            required=False)

    bank_code = TextLine(title=_("Bank code"),
                         required=False,
                         min_length=5,
                         max_length=5)

    counter_code = TextLine(title=_("Counter code"),
                            required=False,
                            min_length=5,
                            max_length=5)

    account_number = TextLine(title=_("Account number"),
                              required=False,
                              min_length=11,
                              max_length=11)

    account_key = TextLine(title=_("Account key"),
                           required=False,
                           min_length=2,
                           max_length=2)

    iban_number = TextLine(title=_("IBAN code"),
                           required=False,
                           min_length=14,
                           max_length=34)

    bic_code = TextLine(title=_("Bank identifier code"),
                        description=_("BIC or SWIFT code"),
                        required=False,
                        min_length=8,
                        max_length=11)

    @invariant
    def check_account(self):
        """Account checker"""
        values = tuple(filter(bool, {self.bank_code, self.counter_code,
                                     self.account_number, self.account_key}))
        if len(values) not in (0, 4):
            raise Invalid(_("Banking account information must contain bank code, "
                            "counter code, account number and account key"))
