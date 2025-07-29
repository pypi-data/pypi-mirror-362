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

from pyams_app_msc.shared.catalog import ICatalogEntryInfo, IWfCatalogEntry
from pyams_content_es.interfaces import IDocumentIndexInfo
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


@adapter_config(name='catalog_info',
                required=IWfCatalogEntry,
                provides=IDocumentIndexInfo)
def catalog_entry_index_info(context):
    """Catalog entry index info"""
    result = {}
    audiences = context.audiences
    if audiences:
        result['audiences'] = context.audiences
    entry_info = ICatalogEntryInfo(context, None)
    if entry_info is None:
        return result
    for field_name in (context.field_names or ()):
        value = getattr(entry_info, field_name)
        if not value:
            continue
        result[field_name] = value
    return {
        'catalog_info': result
    }
