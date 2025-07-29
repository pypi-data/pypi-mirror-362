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

from pyams_app_msc.interfaces import VIEW_CATALOG_PERMISSION
from pyams_app_msc.shared.catalog.interfaces import ICatalogManagerTarget
from pyams_app_msc.shared.catalog.zmi.interfaces import ICatalogManagementView
from pyams_content.shared.common.zmi.dashboard import SharedToolAllInterventionsMenu, \
    SharedToolArchivedContentsView, SharedToolDashboardMenu, SharedToolDashboardView, SharedToolLastModificationsView, \
    SharedToolLastPublicationsView, SharedToolPreparationsView, SharedToolPublicationsView, \
    SharedToolRetiredContentsView, SharedToolSubmissionsView
from pyams_content.zmi.interfaces import IAllDashboardMenu
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_utils.adapter import adapter_config
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader, INavigationViewletManager
from pyams_zmi.zmi.viewlet.menu import ContentManagementMenu

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


#
# Activities catalog dashboard
#

@viewletmanager_config(name='content-manager.menu',
                       context=ICatalogManagerTarget, layer=IAdminLayer,
                       manager=INavigationViewletManager, weight=100,
                       provides=IContentManagementMenu)
class CatalogManagementMenu(ContentManagementMenu):
    """Catalog management menu"""

    _header = _("Catalog management")


class CatalogManagementDashboardViewMixin:
    """Catalog management dashboard mixin view"""

    def get_table(self, container):
        table = super().get_table(container)
        alsoProvides(table, ICatalogManagementView)
        return table


@adapter_config(required=(ICatalogManagerTarget, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def catalog_manager_menu_header(context, request, view, menu):
    """Catalog manager menu header"""
    return request.localizer.translate(_("Activities catalog"))


@viewlet_config(name='dashboard.menu',
                context=ICatalogManagerTarget, layer=IAdminLayer,
                manager=IContentManagementMenu, weight=5,
                permission=VIEW_CATALOG_PERMISSION)
class CatalogManagerDashboardMenu(SharedToolDashboardMenu):
    """Catalog manager dashboard menu"""


@pagelet_config(name='dashboard.html',
                context=ICatalogManagerTarget, layer=IPyAMSLayer,
                permission=VIEW_CATALOG_PERMISSION)
@implementer(ICatalogManagementView)
class CatalogManagerDashboardView(SharedToolDashboardView):
    """Catalog manager dashboard view"""


@pagelet_config(name='my-preparations.html',
                context=ICatalogManagerTarget, layer=IPyAMSLayer,
                permission=VIEW_CATALOG_PERMISSION)
class CatalogManagerPreparationsView(CatalogManagementDashboardViewMixin, SharedToolPreparationsView):
    """Catalog manager preparations view"""


@pagelet_config(name='my-submissions.html',
                context=ICatalogManagerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class CatalogManagerSubmissionsView(CatalogManagementDashboardViewMixin, SharedToolSubmissionsView):
    """Catalog manager submissions view"""


@pagelet_config(name='my-publications.html',
                context=ICatalogManagerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class CatalogManagerPublicationsView(CatalogManagementDashboardViewMixin, SharedToolPublicationsView):
    """Catalog manager publications view"""


@pagelet_config(name='my-retired-contents.html',
                context=ICatalogManagerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class CatalogManagerRetiredContentsView(CatalogManagementDashboardViewMixin, SharedToolRetiredContentsView):
    """Catalog manager retired contents view"""


@pagelet_config(name='my-archived-contents.html',
                context=ICatalogManagerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class CatalogManagerArchivedContentsView(CatalogManagementDashboardViewMixin, SharedToolArchivedContentsView):
    """Catalog manager archived contents view"""


@viewletmanager_config(name='all-interventions.menu',
                       context=ICatalogManagerTarget, layer=IAdminLayer,
                       manager=IContentManagementMenu, weight=20,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IAllDashboardMenu)
class CatalogManagerAllInterventionsMenu(SharedToolAllInterventionsMenu):
    """Catalog manager 'all interventions' dashboard menu"""

    css_class = ''


@pagelet_config(name='last-published.html',
                context=ICatalogManagerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class CatalogManagerLastPublicationsView(CatalogManagementDashboardViewMixin, SharedToolLastPublicationsView):
    """Catalog manager last publications view"""


@pagelet_config(name='last-modified.html',
                context=ICatalogManagerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class CatalogManagerLastModificationsView(CatalogManagementDashboardViewMixin, SharedToolLastModificationsView):
    """Catalog manager last modifications view"""
