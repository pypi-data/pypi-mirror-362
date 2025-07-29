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
from collections import OrderedDict
from enum import Enum

from zope.interface import Attribute
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_i18n.schema import I18nTextLineField
from pyams_portal.interfaces import IPortlet, IPortletSettings

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class THEATERS_ORDER(Enum):
    """Theaters carousel order"""
    ALPHA = 'alpha'
    RANDOM = 'random'


THEATERS_ORDER_LABEL = OrderedDict((
    (THEATERS_ORDER.ALPHA, _("Alphabetical order")),
    (THEATERS_ORDER.RANDOM, _("Random order"))
))


THEATERS_ORDER_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in THEATERS_ORDER_LABEL.items()
])


class IMovieTheaterCarouselPortletSettings(IPortletSettings):
    """Movie theaters carousel portlet settings interface"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Portlet main title"),
                              required=False)

    theaters = Attribute("Movie theaters iterator")

    theaters_order = Choice(title=_("Theaters display order"),
                            description=_("Choose order in which theaters are displayed"),
                            vocabulary=THEATERS_ORDER_VOCABULARY,
                            required=True,
                            default=THEATERS_ORDER.ALPHA.value)


class IAudiencesPortletSettings(IPortletSettings):
    """Audiences portlet settings interface"""

    def get_parent(self, context):
        """Get movie theater parent from given context"""

    def get_audiences(self, context):
        """Movie theater audiences iterator getter"""
