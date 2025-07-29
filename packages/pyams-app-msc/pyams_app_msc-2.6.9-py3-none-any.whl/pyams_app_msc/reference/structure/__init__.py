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

from pyramid.events import subscriber
from zope.component.interfaces import ISite
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from pyams_app_msc.reference.structure.interfaces import IStructureType, IStructureTypeTable, STRUCTURE_TYPES_VOCABULARY
from pyams_content.reference import ReferenceInfo, ReferenceTable, ReferencesVocabulary
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'


@factory_config(IStructureTypeTable)
class StructureTypeTable(ReferenceTable):
    """Structure type table"""


@subscriber(IObjectAddedEvent, context_selector=IStructureTypeTable)
def handle_added_structures_types_table(event):
    """Handle new structures types table"""
    site = get_parent(event.object, ISite)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, IStructureTypeTable)


@factory_config(IStructureType)
class StructureType(ReferenceInfo):
    """Structure type persistent class"""


@vocabulary_config(name=STRUCTURE_TYPES_VOCABULARY)
class StructureTypesVocabulary(ReferencesVocabulary):
    """Structure types vocabulary"""

    table_interface = IStructureTypeTable
