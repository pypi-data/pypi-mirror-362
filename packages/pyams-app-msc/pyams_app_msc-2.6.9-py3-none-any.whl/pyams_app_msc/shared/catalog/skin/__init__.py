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

from urllib.parse import urlencode

from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.skin.interfaces import IPublicURL
from pyams_layer.interfaces import IPyAMSLayer
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.interfaces.url import ICanonicalURL
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url


@adapter_config(required=(IWfCatalogEntry, IPyAMSLayer),
                provides=ICanonicalURL)
class CatalogEntryCanonicalURL(ContextRequestAdapter):
    """Catalog entry canonical URL"""

    def get_url(self, view_name=None, query=None):
        theater = get_parent(self.context, IMovieTheater)
        query = urlencode(query) if query else None
        return absolute_url(theater, self.request,
                            f"+/{ISequentialIdInfo(self.context).get_base_oid().strip()}"
                            f"::{self.context.content_url}"
                            f"{'/{}'.format(view_name) if view_name else '.html'}"
                            f"{'?{}'.format(query) if query else ''}")


@adapter_config(name='booking-new.html',
                required=(IWfCatalogEntry, IPyAMSLayer),
                provides=IPublicURL)
class CatalogEntryPublicURL(ContextRequestAdapter):
    """Catalog entry public URL"""

    def get_url(self):
        """Public URL getter"""
        return self.request.url
