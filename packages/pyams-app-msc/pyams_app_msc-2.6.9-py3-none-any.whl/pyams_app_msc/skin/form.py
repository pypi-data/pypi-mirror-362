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

from pyramid.csrf import get_csrf_token
from zope.interface import Interface

from pyams_app_msc.skin import IPyAMSMSCLayer
from pyams_form.interfaces.form import IForm
from pyams_skin.interfaces.metas import IHTMLContentMetas
from pyams_skin.metas import ContentMeta
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config

__docformat__ = 'restructuredtext'


@adapter_config(name='csrf',
                required=(Interface, IPyAMSMSCLayer, IForm),
                provides=IHTMLContentMetas)
class CSRFContentMetas(ContextRequestViewAdapter):
    """CSRF content metas"""

    def get_metas(self):
        yield ContentMeta('csrf-param', value='csrf_token')
        yield ContentMeta('csrf-token', value=get_csrf_token(self.request))
