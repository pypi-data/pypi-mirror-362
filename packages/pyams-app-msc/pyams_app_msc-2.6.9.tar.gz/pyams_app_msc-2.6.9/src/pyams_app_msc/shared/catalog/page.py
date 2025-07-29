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

from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_app_msc.shared.catalog.interfaces import ICatalogManager, ICatalogManagerTarget
from pyams_content.shared.common.portal import shared_content_portal_page
from pyams_portal.interfaces import IPortalPage, IPortalPortletsConfiguration
from pyams_portal.page import portal_context_portlets_configuration
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent


@adapter_config(required=IWfCatalogEntry,
                provides=IPortalPage)
@adapter_config(name='catalog',
                required=IWfCatalogEntry,
                provides=IPortalPage)
def catalog_entry_page_factory(context):
    """Catalog entry page factory"""
    return shared_content_portal_page(context, page_name='catalog')


@adapter_config(name='catalog',
                required=IWfCatalogEntry,
                provides=IPortalPortletsConfiguration)
def catalog_entry_portlets_configuration(context):
    """Movie theater portlets configuration"""
    return portal_context_portlets_configuration(context, page_name='catalog')


@adapter_config(name='catalog',
                required=ICatalogManager,
                provides=IPortalPortletsConfiguration)
def catalog_manager_portlets_configuration(context):
    """Catalog manager portlets configuration"""
    parent = get_parent(context, ICatalogManagerTarget)
    return portal_context_portlets_configuration(parent, page_name='catalog')
