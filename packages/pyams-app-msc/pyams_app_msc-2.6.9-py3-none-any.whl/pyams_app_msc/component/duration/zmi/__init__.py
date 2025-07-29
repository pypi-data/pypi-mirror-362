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

from zope.interface import Invalid, implementer_only

from pyams_app_msc.component.duration.interfaces import IDurationField
from pyams_app_msc.component.duration.zmi.interfaces import IDurationWidget
from pyams_form.browser.text import TextWidget
from pyams_form.interfaces.widget import IFieldWidget
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import NO_VALUE

__docformat__ = 'restructuredtext'


@implementer_only(IDurationWidget)
class DurationWidget(TextWidget):
    """Duration widget"""

    def extract(self, default=NO_VALUE):
        value = super().extract(default)
        if isinstance(value, str):
            if ':' in value:
                try:
                    hours, minutes = map(lambda x: int(x) if x else 0,
                                         value.split(':'))
                except ValueError:
                    pass
                else:
                    value = str(hours * 60 + minutes)
            elif 'h' in value:
                try:
                    hours, minutes = map(lambda x: int(x) if x else 0,
                                         value.split('h'))
                except ValueError:
                    pass
                else:
                    value = str(hours * 60 + minutes)
            elif value:
                try:
                    _value = int(value)
                except ValueError:
                    pass
        return value


@adapter_config(required=(IDurationField, IFormLayer),
                provides=IFieldWidget)
def DurationFieldWidget(field, request):
    """Duration field widget"""
    return FieldWidget(field, DurationWidget(request))
