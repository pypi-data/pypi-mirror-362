#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
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

from hypatia.interfaces import ICatalog
from zope.annotation.interfaces import IAnnotations

from pyams_app_msc.shared.catalog import ICatalogEntryInfo, IWfCatalogEntry
from pyams_catalog.index import KeywordIndexWithInterface
from pyams_utils.finder import find_objects_providing
from pyams_utils.registry import get_local_registry, get_utility, set_local_registry

__docformat__ = 'restructuredtext'


def color_print(text, color='91'):
    """Print to console with color"""
    print(f'\033[{color}m{text}\033[00m')


def evolve(site):
    """Switch audiences from CatalogEntryInfo to IWfCatalogEntry"""
    old_registry = get_local_registry()
    try:
        registry = site.getSiteManager()
        set_local_registry(registry)
        # Replace catalog index
        catalog = get_utility(ICatalog)
        if 'catalog_audience' in catalog:
            del catalog['catalog_audience']
        catalog['catalog_audience'] = KeywordIndexWithInterface(IWfCatalogEntry,
                                                                discriminator='audiences')
        # Update all catalog entries with new audiences value
        updated = False
        for object in find_objects_providing(site, IWfCatalogEntry):
            catalog_entry = IWfCatalogEntry(object)
            # remove old annotations
            annotations = IAnnotations(catalog_entry)
            if 'msc.activity_info' in annotations:
                del annotations['msc.activity_info']
            # update audiences
            entry_info = ICatalogEntryInfo(catalog_entry)
            if hasattr(entry_info, 'audiences'):
                print(f"Updating audiences for catalog entry « {catalog_entry} »")
                catalog_entry.audiences = entry_info.audiences
                del entry_info.audiences
                updated = True
        if updated:
            color_print("Catalog has been updated; you should reindex the whole site using 'pyams_index' "
                        "and 'pyams_es_index' command-line scripts!")
    finally:
        set_local_registry(old_registry)
