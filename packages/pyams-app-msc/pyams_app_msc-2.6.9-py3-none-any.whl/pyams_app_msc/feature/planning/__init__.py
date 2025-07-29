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

from pyramid.httpexceptions import HTTPNotFound
from ZODB.interfaces import IConnection
from zope.container.btree import BTreeContainer
from zope.interface import classImplements
from zope.location.interfaces import ISublocations
from zope.traversing.interfaces import ITraversable

from pyams_app_msc.feature.planning.interfaces import IPlanning, IPlanningTarget, IWfPlanningTarget, \
    PLANNING_ANNOTATION_KEY
from pyams_app_msc.shared.catalog import CatalogEntry, WfCatalogEntry
from pyams_app_msc.shared.theater import Theater
from pyams_catalog.utils import index_object
from pyams_utils.adapter import ContextAdapter, NullAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.traversing import get_parent


classImplements(Theater, IPlanningTarget)

classImplements(CatalogEntry, IPlanningTarget)
classImplements(WfCatalogEntry, IWfPlanningTarget)


@factory_config(IPlanning)
class Planning(BTreeContainer):
    """Planning persistent class"""

    def add_session(self, session):
        """Add session to planning"""
        IConnection(self).add(session)
        key = ICacheKeyValue(session)
        self[key] = session
        index_object(session)


@adapter_config(required=IPlanningTarget,
                provides=IPlanning)
def planning_factory(context):
    """Planning factory adapter"""
    return get_annotation_adapter(context, PLANNING_ANNOTATION_KEY, IPlanning,
                                  name='++planning++')


@adapter_config(name='planning',
                required=IPlanningTarget,
                provides=ITraversable)
class PlanningTraverser(ContextAdapter):
    """Planning traverser"""

    def traverse(self, name, furtherPath=None):
        """Traverse to inner planning"""
        planning = IPlanning(self.context, None)
        if planning is not None:
            return planning
        raise HTTPNotFound()


@adapter_config(required=IWfPlanningTarget,
                provides=IPlanning)
def workflow_planning_factory(context):
    """Workflow managed planning factory adapter"""
    parent = get_parent(context, IPlanningTarget, allow_context=False)
    return IPlanning(parent, None)


@adapter_config(name='planning',
                required=IWfPlanningTarget,
                provides=ITraversable)
def workflow_planning_traverser(context):
    """Workflow managed content planning traverser"""
    parent = get_parent(context, IPlanningTarget, allow_context=False)
    return ITraversable(parent, None)


@adapter_config(name='planning',
                required=IPlanningTarget,
                provides=ISublocations)
class PlanningSublocations(ContextAdapter):
    """Planning sublocations adapter"""

    def sublocations(self):
        """Planning target sub-locations getter"""
        planning = IPlanning(self.context, None)
        if planning is not None:
            yield from planning.values()


@adapter_config(name='planning',
                required=IWfPlanningTarget,
                provides=ISublocations)
class WorkflowPlanningSublocations(NullAdapter):
    """Disabled sublocations adapter on workflow planning target

    This adapter must be disabled to avoid removal of all planning events
    from catalog when a new version is removed!

    Planning events should then be removed from catalog only when the
    whole content is removed.
    """
