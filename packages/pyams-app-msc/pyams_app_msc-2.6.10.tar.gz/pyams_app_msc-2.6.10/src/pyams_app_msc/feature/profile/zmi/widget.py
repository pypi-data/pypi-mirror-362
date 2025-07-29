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

from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_form.interfaces import INPUT_MODE
from pyams_form.template import widget_template_config
from pyams_form.widget import FieldWidget
from pyams_security_views.widget.principal import PrincipalWidget
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@widget_template_config(mode=INPUT_MODE,
                        template='templates/principal-input.pt',
                        layer=IAdminLayer)
class PrincipalSelectWidget(PrincipalWidget):
    """Principal select widget"""

    @property
    def ajax_url(self):
        theater = get_parent(self.context, IMovieTheater)
        return absolute_url(theater, self.request, 'get-principals.json')


def PrincipalSelectFieldWidget(field, request):  # pylint: disable=invalid-name
    """Principal select field widget"""
    return FieldWidget(field, PrincipalSelectWidget(request))
