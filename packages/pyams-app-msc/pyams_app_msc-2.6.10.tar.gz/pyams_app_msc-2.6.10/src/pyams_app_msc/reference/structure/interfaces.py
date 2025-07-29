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

from zope.container.constraints import containers, contains

from pyams_content.reference import IReferenceInfo, IReferenceTable

__docformat__ = 'restructuredtext'

STRUCTURE_TYPES_VOCABULARY = 'msc.structures_types'


class IStructureType(IReferenceInfo):
    """Structure type interface"""

    containers('.IStructureTypeTable')


class IStructureTypeTable(IReferenceTable):
    """Structure type table interface"""

    contains(IStructureType)
