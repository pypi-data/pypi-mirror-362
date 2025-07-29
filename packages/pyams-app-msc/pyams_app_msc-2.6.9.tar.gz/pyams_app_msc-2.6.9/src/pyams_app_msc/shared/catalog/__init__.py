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
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.feature.tmdb.interfaces import ITMDBServiceClientTarget
from pyams_app_msc.shared.catalog.interfaces import CATALOG_ENTRY_CONTENT_NAME, CATALOG_ENTRY_CONTENT_TYPE, \
    CATALOG_ENTRY_INFORMATION_KEY, CATALOG_ENTRY_SESSION_REQUEST_MODE, ICatalogEntry, ICatalogEntryInfo, IWfCatalogEntry
from pyams_app_msc.shared.theater.interfaces import IMovieTheater, IMovieTheaterSettings
from pyams_content.component.illustration.interfaces import IIllustrationTarget, ILinkIllustrationTarget
from pyams_content.component.paragraph.interfaces import IParagraphContainerTarget
from pyams_content.component.thesaurus.interfaces import ITagsTarget, IThemesTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.feature.review.interfaces import IReviewTarget
from pyams_content.shared.common import SharedContent, WfSharedContent
from pyams_content.shared.common.interfaces import ISharedContent, IWfSharedContent
from pyams_content.shared.common.types import WfTypedSharedContentMixin
from pyams_portal.interfaces import IPortalContext
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent


@factory_config(IWfCatalogEntry)
@factory_config(IWfSharedContent, name=CATALOG_ENTRY_CONTENT_TYPE)
@implementer(ITMDBServiceClientTarget,
             IIllustrationTarget, ILinkIllustrationTarget,
             IParagraphContainerTarget, ITagsTarget, IThemesTarget,
             IPortalContext, IReviewTarget, IPreviewTarget)
class WfCatalogEntry(WfSharedContent, WfTypedSharedContentMixin):
    """Catalog entry"""

    content_type = CATALOG_ENTRY_CONTENT_TYPE
    content_name = CATALOG_ENTRY_CONTENT_NAME
    content_intf = IWfCatalogEntry

    tmdb_movie_id = FieldProperty(IWfCatalogEntry['tmdb_movie_id'])
    audiences = FieldProperty(IWfCatalogEntry['audiences'])
    allow_session_request = FieldProperty(IWfCatalogEntry['allow_session_request'])

    def can_request_session(self):
        """Check if a new session request can be made for this activity"""
        if self.allow_session_request == CATALOG_ENTRY_SESSION_REQUEST_MODE.INHERIT.value:
            theater = get_parent(self, IMovieTheater)
            settings = IMovieTheaterSettings(theater, None)
            return settings.allow_session_request if settings is not None else False
        return self.allow_session_request == CATALOG_ENTRY_SESSION_REQUEST_MODE.ENABLED.value


@factory_config(ICatalogEntryInfo)
class CatalogEntryInfo(Persistent, Contained):
    """Catalog entry persistent information"""

    description = FieldProperty(ICatalogEntryInfo['description'])
    booking_period = FieldProperty(ICatalogEntryInfo['booking_period'])
    release_year = FieldProperty(ICatalogEntryInfo['release_year'])
    original_country = FieldProperty(ICatalogEntryInfo['original_country'])
    original_title = FieldProperty(ICatalogEntryInfo['original_title'])
    original_language = FieldProperty(ICatalogEntryInfo['original_language'])
    producer = FieldProperty(ICatalogEntryInfo['producer'])
    writer = FieldProperty(ICatalogEntryInfo['writer'])
    director = FieldProperty(ICatalogEntryInfo['director'])
    composer = FieldProperty(ICatalogEntryInfo['composer'])
    actors = FieldProperty(ICatalogEntryInfo['actors'])
    awards = FieldProperty(ICatalogEntryInfo['awards'])
    duration = FieldProperty(ICatalogEntryInfo['duration'])
    synopsis = FieldProperty(ICatalogEntryInfo['synopsis'])


@adapter_config(required=ICatalogEntryInfo,
                provides=IViewContextPermissionChecker)
def catalog_entry_info_permission_checker(context):
    """Catalog entry info permission checker"""
    entry = get_parent(context, IWfCatalogEntry)
    return IViewContextPermissionChecker(entry)


@adapter_config(required=IWfCatalogEntry,
                provides=ICatalogEntryInfo)
def catalog_entry_info(context):
    """Catalog entry information adapter"""
    return get_annotation_adapter(context, CATALOG_ENTRY_INFORMATION_KEY, ICatalogEntryInfo)


@factory_config(ICatalogEntry)
@factory_config(ISharedContent, name=CATALOG_ENTRY_CONTENT_TYPE)
class CatalogEntry(SharedContent):
    """Workflow managed catalog entry"""

    content_type = CATALOG_ENTRY_CONTENT_TYPE
    content_name = CATALOG_ENTRY_CONTENT_NAME
