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

from persistent import Persistent
from zope.container.contained import Contained
from zope.location.interfaces import ISublocations
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.traversing.interfaces import ITraversable

from pyams_app_msc.interfaces import MANAGE_THEATER_PERMISSION
from pyams_app_msc.shared.theater import ICinemaRoomContainer, ICinemaRoomContainerTarget, IMovieTheater
from pyams_app_msc.shared.theater.interfaces.room import CINEMA_ROOM_CONTAINER_KEY, ICinemaRoom, ROOMS_SEATS_VOCABULARY, \
    ROOMS_TITLE_VOCABULARY
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config

from pyams_app_msc import _


@factory_config(ICinemaRoom)
class CinemaRoom(Persistent, Contained):
    """Cinema room persistent class"""

    active = FieldProperty(ICinemaRoom['active'])
    name = FieldProperty(ICinemaRoom['name'])
    capacity = FieldProperty(ICinemaRoom['capacity'])
    start_time = FieldProperty(ICinemaRoom['start_time'])
    end_time = FieldProperty(ICinemaRoom['end_time'])
    notepad = FieldProperty(ICinemaRoom['notepad'])


@factory_config(ICinemaRoomContainer)
class CinemaRoomContainer(BTreeOrderedContainer):
    """Cinema room container persistent class"""

    def get_active_items(self):
        """Active items iterator"""
        yield from filter(lambda x: x.active, self.values())


@adapter_config(required=ICinemaRoomContainerTarget,
                provides=ICinemaRoomContainer)
def cinema_room_container(context):
    """Cinema room container adapter"""
    return get_annotation_adapter(context, CINEMA_ROOM_CONTAINER_KEY,
                                  ICinemaRoomContainer,
                                  name='++room++')


@adapter_config(name='room',
                required=ICinemaRoomContainerTarget,
                provides=ITraversable)
class CinemaRoomContainerTraverser(ContextAdapter):
    """Cinema room container traverser"""

    def traverse(self, name, furtherPath):
        """Traverse target to rooms container"""
        return ICinemaRoomContainer(self.context)


@adapter_config(name='rooms',
                required=ICinemaRoomContainerTarget,
                provides=ISublocations)
class CinemaRoomSublocations(ContextAdapter):
    """Cinema rooms sub-locations"""

    def sublocations(self):
        """Sub-locations getter"""
        yield from ICinemaRoomContainer(self.context).values()


@adapter_config(required=ICinemaRoom,
                provides=IViewContextPermissionChecker)
class CinemaRoomPermissionChecker(ContextAdapter):
    """Cinema room permission checker"""

    edit_permission = MANAGE_THEATER_PERMISSION


@vocabulary_config(name=ROOMS_TITLE_VOCABULARY)
class CinemaRoomsTitleVocabulary(SimpleVocabulary):
    """Cinema rooms title vocabulary"""

    def __init__(self, context):
        terms = []
        theater = get_parent(context, IMovieTheater)
        if theater is not None:
            terms = sorted([
                SimpleTerm(item.__name__, title=item.name)
                for item in ICinemaRoomContainer(theater).get_active_items()
            ], key=lambda x: x.title)
        super().__init__(terms)


@vocabulary_config(name=ROOMS_SEATS_VOCABULARY)
class CinemaRoomsSeatsVocabulary(SimpleVocabulary):
    """Cinema rooms seats vocabulary"""

    def __init__(self, context):
        terms = []
        theater = get_parent(context, IMovieTheater)
        if theater is not None:
            request = check_request()
            translate = request.localizer.translate
            terms = sorted([
                SimpleTerm(item.__name__,
                           title=translate(_("{} ({} seats)")).format(item.name, item.capacity))
                for item in ICinemaRoomContainer(theater).get_active_items()
            ], key=lambda x: x.title)
        super().__init__(terms)
