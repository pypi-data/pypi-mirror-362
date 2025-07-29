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
from pyams_app_msc.shared.theater import ICinemaPriceContainerTarget, IMovieTheater
from pyams_app_msc.shared.theater.interfaces.price import CINEMA_PRICE_CONTAINER_KEY, ICinemaPrice, \
    ICinemaPriceContainer, PRICES_VOCABULARY
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config


@factory_config(ICinemaPrice)
class CinemaPrice(Persistent, Contained):
    """Cinema price persistent class"""

    active = FieldProperty(ICinemaPrice['active'])
    name = FieldProperty(ICinemaPrice['name'])
    participant_price = FieldProperty(ICinemaPrice['participant_price'])
    accompanying_ratio = FieldProperty(ICinemaPrice['accompanying_ratio'])
    accompanying_price = FieldProperty(ICinemaPrice['accompanying_price'])
    comment = FieldProperty(ICinemaPrice['comment'])
    notepad = FieldProperty(ICinemaPrice['notepad'])


@factory_config(ICinemaPriceContainer)
class CinemaPriceContainer(BTreeOrderedContainer):
    """Cinema price container persistent class"""

    def get_active_items(self):
        """Active items iterator"""
        yield from filter(lambda x: x.active, self.values())


@adapter_config(required=ICinemaPriceContainerTarget,
                provides=ICinemaPriceContainer)
def cinema_price_container(context):
    """Cinema price container adapter"""
    return get_annotation_adapter(context, CINEMA_PRICE_CONTAINER_KEY,
                                  ICinemaPriceContainer,
                                  name='++price++')


@adapter_config(name='price',
                required=ICinemaPriceContainerTarget,
                provides=ITraversable)
class CinemaPriceContainerTraverser(ContextAdapter):
    """Cinema price container traverser"""

    def traverse(self, name, furtherPath):
        """Traverse target to prices container"""
        return ICinemaPriceContainer(self.context)


@adapter_config(name='prices',
                required=ICinemaPriceContainerTarget,
                provides=ISublocations)
class CinemaPriceSublocations(ContextAdapter):
    """Cinema prices sub-locations"""

    def sublocations(self):
        """Sub-locations getter"""
        yield from ICinemaPriceContainer(self.context).values()


@adapter_config(required=ICinemaPrice,
                provides=IViewContextPermissionChecker)
class CinemaPricePermissionChecker(ContextAdapter):
    """Cinema price permission checker"""

    edit_permission = MANAGE_THEATER_PERMISSION


@vocabulary_config(name=PRICES_VOCABULARY)
class CinemaPricesVocabulary(SimpleVocabulary):
    """Cinema prices vocabulary"""

    def __init__(self, context):
        terms = []
        theater = get_parent(context, IMovieTheater)
        if theater is not None:
            terms = sorted([
                SimpleTerm(item.__name__, title=item.name)
                for item in ICinemaPriceContainer(theater).get_active_items()
            ], key=lambda x: x.title)
        super().__init__(terms)
