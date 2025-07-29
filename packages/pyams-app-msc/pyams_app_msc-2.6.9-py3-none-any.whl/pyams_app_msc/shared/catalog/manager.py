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

from zope.container.btree import BTreeContainer
from zope.location.interfaces import ISublocations
from zope.traversing.interfaces import ITraversable

from pyams_app_msc.shared.catalog.interfaces import CATALOG_MANAGER_KEY, ICatalogManager, ICatalogManagerTarget
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.shared.common.manager import BaseSharedTool
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_utils.traversing import get_parent


@factory_config(ICatalogManager)
class CatalogManager(BTreeContainer, BaseSharedTool):
    """Catalog manager"""

    shared_content_menu = False

    @property
    def shared_content_workflow(self):
        parent = get_parent(self, IMovieTheater)
        return parent.shared_content_workflow


@adapter_config(required=ICatalogManagerTarget,
                provides=ICatalogManager)
def catalog_manager(context):
    """Catalog manager factory"""
    return get_annotation_adapter(context, CATALOG_MANAGER_KEY, ICatalogManager,
                                  name='++catalog++')


@adapter_config(name='catalog',
                required=ICatalogManagerTarget,
                provides=ITraversable)
class CatalogManagerTraverser(ContextAdapter):
    """Catalog manager traverser"""

    def traverse(self, name, furtherPath=None):
        """Catalog getter"""
        return ICatalogManager(self.context)


@adapter_config(name='catalog',
                required=ICatalogManagerTarget,
                provides=ISublocations)
class CatalogManagerSublocations(ContextAdapter):
    """Catalog manager sub-locations"""

    def sublocations(self):
        """Catalog manager sub-locations iterator"""
        yield from ICatalogManager(self.context).values()
