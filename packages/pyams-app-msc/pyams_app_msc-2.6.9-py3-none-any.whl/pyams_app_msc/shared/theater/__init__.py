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

from pyramid.events import subscriber
from zope.container.ordered import OrderedContainer
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectMovedEvent, IObjectRemovedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_app_msc.interfaces import MANAGE_THEATER_PERMISSION
from pyams_app_msc.shared.catalog.interfaces import CATALOG_ENTRY_CONTENT_TYPE, ICatalogEntryInfo, ICatalogManagerTarget
from pyams_app_msc.shared.theater.interfaces import IMovieTheater, IMovieTheaterRoles, IMovieTheaterSettings, \
    MOVIE_THEATER_ROLES, MOVIE_THEATER_SETTINGS_KEY, MSC_THEATERS_VOCABULARY
from pyams_app_msc.shared.theater.interfaces.audience import ICinemaAudienceContainerTarget
from pyams_app_msc.shared.theater.interfaces.mail import IMailTemplatesTarget
from pyams_app_msc.shared.theater.interfaces.price import ICinemaPriceContainerTarget
from pyams_app_msc.shared.theater.interfaces.room import ICinemaRoomContainer, ICinemaRoomContainerTarget
from pyams_content.component.illustration.interfaces import IIllustrationTarget, ILinkIllustrationTarget
from pyams_content.component.paragraph.interfaces import IParagraphFactorySettingsTarget
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.interfaces import IObjectType
from pyams_content.shared.common.interfaces import CONTENT_MANAGER_ROLES, ISharedContent
from pyams_content.shared.common.manager import BaseSharedTool
from pyams_content.shared.common.types import TypedSharedToolMixin
from pyams_file.property import FileProperty
from pyams_i18n.interfaces import II18n
from pyams_layer.skin import UserSkinnableContentMixin
from pyams_portal.interfaces import IPortalContext, IPortalFooterContext, IPortalHeaderContext
from pyams_security.interfaces import IDefaultProtectionPolicy, IRolesPolicy, IViewContextPermissionChecker
from pyams_security.property import RolePrincipalsFieldProperty
from pyams_security.security import ProtectedObjectMixin, ProtectedObjectRoles
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextAdapter, NullAdapter, adapter_config
from pyams_utils.factory import factory_config, get_interface_base_name, get_object_factory
from pyams_utils.registry import get_utilities_for
from pyams_utils.request import check_request, query_request
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@factory_config(IMovieTheater)
@implementer(IDefaultProtectionPolicy, IIllustrationTarget, ILinkIllustrationTarget,
             ICinemaRoomContainerTarget, ICinemaPriceContainerTarget, ICinemaAudienceContainerTarget,
             ICatalogManagerTarget, IMailTemplatesTarget, IParagraphFactorySettingsTarget,
             IPortalContext, IPortalHeaderContext, IPortalFooterContext, IPreviewTarget)
class Theater(OrderedContainer, BaseSharedTool, TypedSharedToolMixin,
              ProtectedObjectMixin, UserSkinnableContentMixin):
    """Main theater persistent class"""

    title = FieldProperty(IMovieTheater['title'])
    short_name = FieldProperty(IMovieTheater['short_name'])
    header = FieldProperty(IMovieTheater['header'])
    description = FieldProperty(IMovieTheater['description'])
    logo = FileProperty(IMovieTheater['logo'])
    address = FieldProperty(IMovieTheater['address'])
    web_address = FieldProperty(IMovieTheater['web_address'])
    contact_email = FieldProperty(IMovieTheater['contact_email'])
    phone_number = FieldProperty(IMovieTheater['phone_number'])
    banking_account = FieldProperty(IMovieTheater['banking_account'])
    admin_info = FieldProperty(IMovieTheater['admin_info'])
    notepad = FieldProperty(IMovieTheater['notepad'])

    sequence_name = ''
    sequence_prefix = ''

    content_name = _("Theater")
    shared_content_menu = False
    shared_content_type = CATALOG_ENTRY_CONTENT_TYPE
    shared_content_info_factory = ICatalogEntryInfo

    @property
    def shared_content_factory(self):
        return get_object_factory(ISharedContent, name=self.shared_content_type)

    def is_deletable(self):
        """Check if theater can be deleted"""
        container = ICinemaRoomContainer(self)
        return len(container.keys()) == 0


@adapter_config(required=IMovieTheater,
                provides=IObjectType)
def movie_theater_object_type(context):
    """Movie theater object type adapter"""
    return get_interface_base_name(IMovieTheater)


@implementer(IMovieTheaterRoles)
class MovieTheaterRoles(ProtectedObjectRoles):
    """Movie theater roles"""

    msc_managers = RolePrincipalsFieldProperty(IMovieTheaterRoles['msc_managers'])
    msc_operators = RolePrincipalsFieldProperty(IMovieTheaterRoles['msc_operators'])
    msc_contributors = RolePrincipalsFieldProperty(IMovieTheaterRoles['msc_contributors'])
    msc_designers = RolePrincipalsFieldProperty(IMovieTheaterRoles['msc_designers'])
    msc_readers = RolePrincipalsFieldProperty(IMovieTheaterRoles['msc_readers'])


@adapter_config(required=IMovieTheater,
                provides=IMovieTheaterRoles)
def movie_theater_roles(context):
    """Movie theater roles adapter"""
    return MovieTheaterRoles(context)


@adapter_config(name=CONTENT_MANAGER_ROLES,
                required=IMovieTheater,
                provides=IRolesPolicy)
class MovieTheaterContentManagerRolesPolicy(NullAdapter):
    """Movie theater content manager roles policy"""


@adapter_config(name=MOVIE_THEATER_ROLES,
                required=IMovieTheater,
                provides=IRolesPolicy)
class MovieTheaterRolesPolicy(ContextAdapter):
    """Movie theater roles policy"""

    roles_interface = IMovieTheaterRoles
    weight = 20


@subscriber(IObjectAddedEvent, context_selector=IMovieTheater)
def handle_added_movie_theater(event):
    """Register movie theater when added"""
    site = get_parent(event.newParent, ISiteRoot)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, IMovieTheater, name=event.newName)


@subscriber(IObjectMovedEvent, context_selector=IMovieTheater)
def handle_moved_movie_theater(event: IObjectMovedEvent):
    """Update movie theater registration when renamed"""
    if IObjectRemovedEvent.providedBy(event):
        return
    request = check_request()
    registry = request.root.getSiteManager()
    if registry is not None:
        old_name = event.oldName
        new_name = event.newName
        if old_name == new_name:
            return
        registry.unregisterUtility(event.object, IMovieTheater, name=old_name)
        if new_name:
            registry.registerUtility(event.object, IMovieTheater, name=new_name)


@subscriber(IObjectRemovedEvent, context_selector=IMovieTheater)
def handle_deleted_movie_theater(event: IObjectRemovedEvent):
    """Un-register movie theater when deleted"""
    site = get_parent(event.oldParent, ISiteRoot)
    registry = site.getSiteManager()
    if registry is not None:
        registry.unregisterUtility(event.object, IMovieTheater, name=event.oldName)


@adapter_config(required=IMovieTheater,
                provides=IViewContextPermissionChecker)
class MovieTheaterPermissionChecker(ContextAdapter):
    """Movie theater edit permission checker"""

    edit_permission = MANAGE_THEATER_PERMISSION


@vocabulary_config(name=MSC_THEATERS_VOCABULARY)
class MovieTheaterVocabulary(SimpleVocabulary):
    """Movie theaters vocabulary"""

    interface = IMovieTheater

    def __init__(self, context=None):
        request = query_request()
        super().__init__(sorted([
            SimpleTerm(v, title=II18n(t).query_attribute('title', request=request))
            for v, t in get_utilities_for(self.interface)
        ], key=lambda x: x.title))
