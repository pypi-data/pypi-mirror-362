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

from pyramid.interfaces import IRequest

from pyams_app_msc.shared.catalog import ICatalogEntryInfo, IWfCatalogEntry
from pyams_content_api.feature.json import IJSONExporter, JSONBaseExporter
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


@adapter_config(name='catalog_entry',
                required=(IWfCatalogEntry, IRequest),
                provides=IJSONExporter)
class JSONCatalogEntryExporter(JSONBaseExporter):
    """Catalog entry API info"""
    
    is_inner = True
    conversion_target = None

    def convert_content(self, **params):
        """JSON catalog entry conversion"""
        result = super().convert_content(**params)
        info = ICatalogEntryInfo(self.context)
        for name in self.context.field_names:
            self.get_attribute(result, name, context=info)
        return result
