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

"""PyAMS_app_msc.shared.catalog.interfaces module

"""

from collections import OrderedDict
from datetime import datetime
from enum import Enum

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.interface import Attribute, Interface
from zope.schema import Choice, Int, List, Text, TextLine
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_app_msc.component.duration.schema import DurationField
from pyams_app_msc.shared.theater.interfaces.audience import AUDIENCES_VOCABULARY
from pyams_content.feature.filter import IFilter
from pyams_content.feature.filter.interfaces import FILTER_SORTING, MANUAL_FILTER_SORTING_VOCABULARY
from pyams_content.shared.common.interfaces import IBaseSharedTool, ISharedContent
from pyams_content.shared.common.interfaces.types import IWfTypedSharedContentPortalContext, \
    VISIBLE_DATA_TYPES_VOCABULARY
from pyams_i18n.interfaces import BASE_LANGUAGES_VOCABULARY_NAME
from pyams_portal.interfaces import IPortalContext
from pyams_utils.schema import HTMLField

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


CATALOG_ENTRY_INFORMATION_KEY = 'msc.entry_info'


class ICatalogEntryInfo(Interface):
    """Catalog entry additional information interface"""

    description = HTMLField(title=_("Description"),
                            required=False)

    booking_period = TextLine(title=_("Booking period"),
                              description=_("This is the next period for which this activity "
                                            "will be available"),
                              required=False)

    release_year = Choice(title=_("Release year"),
                          values=range(datetime.today().year, 1900, -1),
                          required=False)

    original_country = TextLine(title=_("Original country"),
                                required=False)

    original_title = TextLine(title=_("Original title"),
                              required=False)

    original_language = Choice(title=_("Original language"),
                               vocabulary=BASE_LANGUAGES_VOCABULARY_NAME,
                               required=False)

    producer = TextLine(title=_("Producers"),
                        required=False)

    writer = TextLine(title=_("Writers"),
                      required=False)

    director = TextLine(title=_("Director"),
                        required=False)

    composer = TextLine(title=_("Composer"),
                        required=False)

    actors = TextLine(title=_("Main actors"),
                      required=False)

    awards = Text(title=_("Awards"),
                  required=False)

    duration = DurationField(title=_("Duration"),
                             description=_("Duration, in minutes"),
                             required=False)

    synopsis = Text(title=_("Synopsis"),
                    required=False)


CATALOG_ENTRY_CONTENT_TYPE = 'catalog'
CATALOG_ENTRY_CONTENT_NAME = _("Catalog entry")


class IWfCatalogEntryAddInfo(Interface):
    """Catalog entry adding info interface"""

    title = TextLine(title=_("Title"),
                     description=_("Movie or activity title; you can select an entry from TMDB database, "
                                   "or enter your own title"),
                     required=True)


class CATALOG_ENTRY_SESSION_REQUEST_MODE(Enum):
    """Catalog entry session request mode"""
    INHERIT = 'inherit'
    ENABLED = 'enabled'
    DISABLED = 'disabled'


CATALOG_ENTRY_SESSION_REQUEST_MODE_LABELS = OrderedDict((
    (CATALOG_ENTRY_SESSION_REQUEST_MODE.INHERIT.value, _("(inherit from theater settings)")),
    (CATALOG_ENTRY_SESSION_REQUEST_MODE.ENABLED.value, _("Enable new sessions requests")),
    (CATALOG_ENTRY_SESSION_REQUEST_MODE.DISABLED.value, _("Disable new sessions requests")),
))


CATALOG_ENTRY_SESSION_REQUEST_MODE_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in CATALOG_ENTRY_SESSION_REQUEST_MODE_LABELS.items()
])


class IWfCatalogEntry(IWfTypedSharedContentPortalContext):
    """Catalog entry interface"""

    data_type = Choice(title=_("Activity type"),
                       required=True,
                       vocabulary=VISIBLE_DATA_TYPES_VOCABULARY)

    tmdb_movie_id = Int(title=_("TMDB movie ID"),
                        description=_("Movie ID in TMDB database"),
                        required=False)

    audiences = List(title=_("Selected audiences"),
                     description=_("List of audiences selected for this activity"),
                     value_type=Choice(vocabulary=AUDIENCES_VOCABULARY),
                     required=False)

    allow_session_request = Choice(title=_("New sessions requests"),
                                   description=_('When enabled, external partners will be allowed to '
                                                 'send requests for new sessions of this activity'),
                                   vocabulary=CATALOG_ENTRY_SESSION_REQUEST_MODE_VOCABULARY,
                                   required=True,
                                   default=CATALOG_ENTRY_SESSION_REQUEST_MODE.INHERIT.value)

    def can_request_session(self):
        """Check if a new session request can be created for this activity"""


class ICatalogEntry(ISharedContent):
    """Workflow managed catalog entry interface"""


CATALOG_MANAGER_KEY = 'msc.catalog'


class ICatalogManager(IBaseSharedTool, IPortalContext):
    """Catalog manager interface"""

    contains('.ICatalogEntry')

    shared_content_type = Attribute("Shared data content type name")


class ICatalogManagerTarget(IAttributeAnnotatable):
    """Catalog manager target marker interface"""


class IAudienceFilter(IFilter):
    """Audience filter interface"""


class IDurationFilter(IFilter):
    """Activity duration filter interface"""

    sorting_mode = Choice(title=_("Sorting mode"),
                          description=_("Filter entries sorting mode"),
                          vocabulary=MANUAL_FILTER_SORTING_VOCABULARY,
                          default=FILTER_SORTING.MANUAL.value,
                          required=True)
