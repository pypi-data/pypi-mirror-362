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

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Or
from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPForbidden
from zope.interface import Interface
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility

from pyams_app_msc.feature.profile import IUserProfile, USER_PROFILE_KEY
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_catalog.query import CatalogResultSet
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_security.interfaces import LOGIN_REFERER_KEY
from pyams_security.interfaces.plugin import IAuthenticatedPrincipalEvent
from pyams_security.utility import get_principal
from pyams_security_views.interfaces.login import ILoginView
from pyams_site.interfaces import ISiteRoot
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import get_interface_base_name
from pyams_utils.list import next_from
from pyams_utils.registry import get_utility, query_utility
from pyams_utils.url import absolute_url

__docformat__ = 'restructuredtext'

from pyams_app_msc import _
from pyams_workflow.interfaces import IWorkflowPublicationInfo


@adapter_config(required=(Interface, IPyAMSLayer, ILoginView),
                provides=IAJAXFormRenderer)
class LoginFormAJAXRenderer(ContextRequestViewAdapter):
    """Login form renderer"""

    def render(self, changes):  # pylint: disable=unused-argument
        """AJAX form renderer"""
        status = {
            'status': 'redirect'
        }
        request = self.request
        session = request.session
        hash = request.params.get('login_form.widgets.hash', '')
        if hash:
            if LOGIN_REFERER_KEY in session:
                status['location'] = f"{session[LOGIN_REFERER_KEY] or '/'}{hash}"
                del session[LOGIN_REFERER_KEY]
            else:
                status['location'] = f'/{hash}'
        else:
            principal_id = self.view.finished_state.get('changes')
            if principal_id:
                catalog = get_utility(ICatalog)
                query = And(Eq(catalog['object_types'], get_interface_base_name(IMovieTheater)),
                            Or(Eq(catalog['role:msc:manager'], principal_id),
                               Eq(catalog['role:msc:operator'], principal_id),
                               Eq(catalog['role:msc:contributor'], principal_id),
                               Eq(catalog['role:msc:reader'], principal_id)))
                theaters = list(CatalogResultSet(CatalogQuery(catalog).query(query)))
                if len(theaters) == 1:
                    theater = theaters[0]
                    status['location'] = absolute_url(theater, request, 'admin')
                elif len(theaters) > 1:
                    status['location'] = absolute_url(request.root, request,
                                                      'select-admin-theater.html')
                else:
                    theater = None
                    # request.principal is reified, so we can't use request.principal just
                    # after authentication to load profile!
                    profile_info = get_utility(IPrincipalAnnotationUtility) \
                        .getAnnotationsById(principal_id) \
                        .get(USER_PROFILE_KEY)
                    if (profile_info is not None) and profile_info.local_theaters:
                        if len(profile_info.local_theaters) > 1:
                            status['location'] = absolute_url(request.root, request,
                                                              'select-user-theater.html')
                            return status
                        else:
                            theater_name = next_from(profile_info.local_theaters)
                            theater = query_utility(IMovieTheater, name=theater_name)
                    session = request.session
                    if theater is not None:
                        status['location'] = absolute_url(theater, request)
                        if LOGIN_REFERER_KEY in session:
                            del session[LOGIN_REFERER_KEY]
                    else:
                        if LOGIN_REFERER_KEY in session:
                            status['location'] = session[LOGIN_REFERER_KEY]
                            del session[LOGIN_REFERER_KEY]
                        else:
                            status['location'] = absolute_url(request.context, request)
        return status


@subscriber(IAuthenticatedPrincipalEvent)
def handle_authenticated_principal(event):
    """Check for inactive profile when authenticated"""
    principal = get_principal(principal_id=event.principal_id)
    profile = IUserProfile(principal)
    if not profile.active:
        raise HTTPForbidden(_("User profile is disabled!"))


@pagelet_config(name='select-admin-theater.html',
                context=ISiteRoot, layer=IPyAMSLayer)
@template_config(template='templates/select-admin-theater.pt',
                 layer=IPyAMSLayer)
class AdminTheaterSelectionView(PortalContextIndexPage):
    """Admin theater selection view"""

    def get_theaters(self):
        """Theaters list getter"""
        principal_id = self.request.principal.id
        catalog = get_utility(ICatalog)
        query = And(Eq(catalog['object_types'], get_interface_base_name(IMovieTheater)),
                    Or(Eq(catalog['role:msc:manager'], principal_id),
                       Eq(catalog['role:msc:operator'], principal_id),
                       Eq(catalog['role:msc:contributor'], principal_id),
                       Eq(catalog['role:msc:reader'], principal_id)))
        yield from sorted(CatalogResultSet(CatalogQuery(catalog).query(query)),
                          key=lambda x: II18n(x).query_attribute('title', request=self.request))


@pagelet_config(name='select-user-theater.html',
                context=ISiteRoot, layer=IPyAMSLayer)
@template_config(template='templates/select-user-theater.pt',
                 layer=IPyAMSLayer)
class UserTheaterSelectionView(PortalContextIndexPage):
    """User theater selection view"""

    def get_theaters(self):
        """Theaters list getter"""
        profile = IUserProfile(self.request)
        for theater_name in (profile.local_theaters or ()):
            theater = query_utility(IMovieTheater, name=theater_name)
            if theater is None:
                continue
            workflow_info = IWorkflowPublicationInfo(theater)
            if workflow_info.is_visible(self.request):
                yield theater
