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

from zope.interface import Interface, alsoProvides, implementer
from zope.schema.vocabulary import SimpleTerm

from pyams_app_msc.feature.tmdb.interfaces import ITMDBService, TMDB_SEARCH_PATH, TMDB_SEARCH_ROUTE
from pyams_app_msc.feature.tmdb.zmi.lookup import ITMDBSearchInterface
from pyams_app_msc.interfaces import MANAGE_CATALOG_PERMISSION
from pyams_app_msc.shared.catalog.interfaces import ICatalogEntryInfo, ICatalogManager, ICatalogManagerTarget, \
    IWfCatalogEntry, IWfCatalogEntryAddInfo
from pyams_app_msc.shared.catalog.zmi.interfaces import ICatalogManagementMenu, ICatalogManagementView
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_content.shared.common.zmi import SharedContentAddAction, SharedContentAddForm
from pyams_content.shared.common.zmi.content import SharedContentHeaderViewlet
from pyams_content.shared.common.zmi.types.content import TypedSharedContentCustomInfoEditForm, \
    TypedSharedContentPropertiesEditForm
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.browser.select import SelectWidget
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IFormContent
from pyams_form.widget import FieldWidget
from pyams_i18n.interfaces import INegotiator
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_skin.interfaces.widget import IDynamicSelectWidget, IHTMLEditorConfiguration
from pyams_utils.adapter import NullAdapter, adapter_config
from pyams_utils.factory import create_object
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu, IToolbarViewletManager
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class EncodedSimpleTerm(SimpleTerm):
    """Encoded simple term"""

    def __init__(self, value, token=None, title=None):
        """Create a term for *value* and *token*. If *token* is
        omitted, str(value) is used for the token, escaping any
        non-ASCII characters.

        If *title* is provided, term implements
        :class:`zope.schema.interfaces.ITitledTokenizedTerm`.
        """
        super().__init__(value, token, title)
        if token:
            self.token = token


@implementer(IDynamicSelectWidget)
class TMDBMovieSelectWidget(SelectWidget):
    """TMDB movie select widget"""

    placeholder = _("Enter text for TMDB movie search")

    @property
    def ajax_url(self):
        """AJAX search API URL getter"""
        return self.request.registry.settings.get(f'{TMDB_SEARCH_ROUTE}_route.path',
                                                  TMDB_SEARCH_PATH)

    @staticmethod
    def term_factory(value):
        """Select movie term factory"""
        return EncodedSimpleTerm(value, token=value)


def TMDBMovieFieldSelectWidget(field, request):
    """TMDB movie field select widget"""
    return FieldWidget(field, TMDBMovieSelectWidget(request))


@viewlet_config(name='add-content.action',
                context=IMovieTheater, layer=IAdminLayer)
class MovieTheaterSharedContentAddAction(NullAdapter):
    """Disabled shared content add action on movie theater"""


@viewlet_config(name='add-content.action',
                context=ICatalogManagerTarget, layer=IAdminLayer,
                view=ICatalogManagementView,
                manager=IToolbarViewletManager, weight=10,
                permission=MANAGE_CATALOG_PERMISSION)
class CatalogEntryAddAction(SharedContentAddAction):
    """Catalog entry add action"""

    label = _("Add catalog entry")


@ajax_form_config(name='add-shared-content.html',
                  context=ICatalogManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_CATALOG_PERMISSION)
class CatalogEntryAddForm(SharedContentAddForm):
    """Catalog entry add form"""

    legend = _("New catalog entry properties")

    fields = Fields(IWfCatalogEntryAddInfo) + \
        Fields(IWfCatalogEntry).select('data_type') + \
        Fields(ITMDBSearchInterface) + \
        Fields(IWfCatalogEntry).select('notepad')
    fields['title'].widget_factory = TMDBMovieFieldSelectWidget

    _edit_permission = MANAGE_CATALOG_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        title = self.widgets.get('title')
        if title is not None:
            title.object_data = {
                'ams-select2-options': {
                    'tags': True
                }
            }
            alsoProvides(title, IObjectData)

    @property
    def container_target(self):
        return ICatalogManager(self.context)

    def update_content(self, obj, data):
        negotiator = get_utility(INegotiator)
        title = data.get(self, data).pop('title', '')
        if title.startswith('movie_id::'):
            service = create_object(ITMDBService)
            if (service is not None) and (service.configuration is not None):
                _, movie_id = title.split('::', 1)
                movie = service.get_movie_info(movie_id, with_credits=False)
                if movie is not None:
                    obj.title = {negotiator.server_language: movie.get('title')}
                    obj.tmdb_movie_id = movie.get('id')
        else:
            obj.title = {negotiator.server_language: title}
        return super().update_content(obj, data)


@adapter_config(required=(ICatalogManagerTarget, IAdminLayer, CatalogEntryAddForm),
                provides=IAJAXFormRenderer)
class CatalogEntryAddFormRenderer(AJAXFormRenderer):
    """Catalog entry add form renderer"""

    def render(self, changes):
        return {
            'status': 'redirect',
            'location': self.form.next_url()
        }


@viewlet_config(name='pyams.content_header',
                context=IWfCatalogEntry, layer=IAdminLayer,
                manager=IHeaderViewletManager, weight=10)
class CatalogEntryHeaderViewlet(SharedContentHeaderViewlet):
    """Catalog entry header viewlet"""

    @property
    def parent_target_url(self):
        """Parent target URL"""
        tool = get_parent(self.context, IMovieTheater)
        if tool is None:
            return None
        return absolute_url(tool, self.request, 'admin#dashboard.html')


@ajax_form_config(name='properties.html',
                  context=IWfCatalogEntry, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class CatalogEntryPropertiesEditForm(TypedSharedContentPropertiesEditForm):
    """Catalog entry properties edit form"""

    interface = IWfCatalogEntry
    fieldnames = ('title', 'short_name', 'content_url', 'data_type',
                  'audiences', 'allow_session_request', 'header',
                  'description', 'notepad')


@viewlet_config(name='activity-info.menu',
                context=IWfCatalogEntry, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=15,
                permission=VIEW_SYSTEM_PERMISSION)
class CatalogEntryInformationMenu(NavigationMenuItem):
    """Activity information menu"""

    label = _("Activity details")
    href = '#activity-info.html'


@ajax_form_config(name='activity-info.html',
                  context=IWfCatalogEntry, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class CatalogEntryInformationEditForm(TypedSharedContentCustomInfoEditForm):
    """Activity information edit form"""

    title = _("Activity information")
    legend = _("Custom properties")

    @property
    def fields(self):
        """Form fields getter"""
        datatype = self.datatype
        if datatype is None:
            return Fields(Interface)
        return Fields(ICatalogEntryInfo).select(*datatype.field_names)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        synopsis = self.widgets.get('synopsis')
        if synopsis is not None:
            synopsis.add_class('h-200px')


@adapter_config(required=(IWfCatalogEntry, IPyAMSLayer, CatalogEntryInformationEditForm),
                provides=IFormContent)
def catalog_entry_info_edit_form_content(context, request, form):
    """Catalog entry information edit form content getter"""
    return ICatalogEntryInfo(context)


@adapter_config(required=(ICatalogEntryInfo, IAdminLayer, CatalogEntryInformationEditForm),
                provides=IViewContextPermissionChecker)
def catalog_entry_info_permission_checker(context, request, view):
    """Catalog entry activity info permission checker"""
    catalog_entry = get_parent(context, IWfCatalogEntry)
    return IViewContextPermissionChecker(catalog_entry)


@adapter_config(name='description',
                required=(ICatalogEntryInfo, IAdminLayer, CatalogEntryInformationEditForm),
                provides=IHTMLEditorConfiguration)
def catalog_entry_description_editor_configuration(context, request, view):
    """Catalog entry description editor configuration"""
    return {
        'menubar': False,
        'plugins': 'paste textcolor lists charmap link pyams_link',
        'toolbar': 'undo redo | pastetext | h3 h4 | bold italic superscript | '
                   'forecolor backcolor | bullist numlist | '
                   'charmap pyams_link link',
        'toolbar1': False,
        'toolbar2': False,
        'height': 200
    }
