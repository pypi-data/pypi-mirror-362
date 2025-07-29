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

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Or
from zope.interface import Interface

from pyams_app_msc.feature.profile import IUserProfile
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_catalog.query import CatalogResultSet
from pyams_content.feature.header.portlet import IPageHeaderPortletSettings
from pyams_content.feature.header.portlet.skin import PageHeaderPortletDefaultRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import get_interface_base_name
from pyams_utils.registry import get_utility, query_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url

__docformat__ = 'restructuredtext'

from pyams_app_msc import _
from pyams_workflow.interfaces import IWorkflowPublicationInfo


@adapter_config(name='msc::default',
                required=(IPortalContext, IPyAMSLayer, Interface, IPageHeaderPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/header-default.pt', layer=IPyAMSLayer)
class MSCPageHeaderPortletDefaultRenderer(PageHeaderPortletDefaultRenderer):
    """Page header portlet default renderer"""

    label = _("MSC: Simple banner")

    @property
    def logo(self):
        logo = None
        theater = get_parent(self.context, IMovieTheater)
        if theater is not None:
            logo = theater.logo
        return (theater, logo) if logo else super().logo

    @property
    def admin_menus(self):
        principal_id = self.request.principal.id
        catalog = get_utility(ICatalog)
        has_menus = False
        profile = IUserProfile(self.request, None)
        if profile is not None:
            for theater_name in (profile.local_theaters or ()):
                theater = query_utility(IMovieTheater, name=theater_name)
                if (theater is not None) and IWorkflowPublicationInfo(theater).is_visible(self.request):
                    menu = MenuItem(theater, self.request, self, None)
                    menu.label = II18n(theater).query_attribute('title', request=self.request)
                    menu.href = absolute_url(theater, self.request)
                    menu.update()
                    yield menu
                    has_menus = True
        query = And(Eq(catalog['object_types'], get_interface_base_name(IMovieTheater)),
                    Or(Eq(catalog['role:msc:manager'], principal_id),
                       Eq(catalog['role:msc:operator'], principal_id),
                       Eq(catalog['role:msc:contributor'], principal_id),
                       Eq(catalog['role:msc:reader'], principal_id)))
        for theater in sorted(CatalogResultSet(CatalogQuery(catalog).query(query)),
                              key=lambda x: II18n(x).query_attribute('title', request=self.request)):
            if has_menus:
                yield MenuDivider(theater, self.request, self, None)
                menu = MenuItem(theater, self.request, self, None)
                menu.label = _("Management menus")
                menu.href = None
                menu.css_class = 'font-weight-light pl-4'
                menu.update()
                yield menu
                has_menus = False
            menu = MenuItem(theater, self.request, self, None)
            menu.label = II18n(theater).query_attribute('title', request=self.request)
            menu.href = absolute_url(theater, self.request, 'admin')
            menu.update()
            yield menu
