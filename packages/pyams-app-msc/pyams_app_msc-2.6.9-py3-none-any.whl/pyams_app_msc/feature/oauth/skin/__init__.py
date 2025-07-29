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
from pyramid.events import subscriber

from pyams_app_msc.feature.profile import IUserProfile
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_catalog.query import CatalogResultSet
from pyams_security.interfaces import LOGIN_REFERER_KEY
from pyams_security.utility import get_principal
from pyams_utils.factory import get_interface_base_name
from pyams_utils.registry import get_utility
from pyams_utils.url import absolute_url

__docformat__ = 'restructuredtext'


try:

    from pyams_auth_oauth.interfaces import IOAuthAuthenticationEvent

    @subscriber(IOAuthAuthenticationEvent)
    def handle_oauth_authentication(event):
        """Handle redirect on OAuth authentication"""
        principal_id = event.principal_id
        principal = get_principal(principal_id=principal_id)
        profile_info = IUserProfile(principal, None)
        if profile_info is None:
            return
        request = event.request
        if not (profile_info.firstname and profile_info.lastname and
                profile_info.email and profile_info.establishment and
                profile_info.local_theaters):
            event.redirect_location = absolute_url(request.root, request, 'my-profile.html')
        else:
            theaters_names = profile_info.local_theaters
            if len(theaters_names) == 1:
                theater = get_utility(IMovieTheater, name=theaters_names[0])
                if theater is not None:
                    event.redirect_location = absolute_url(theater, request)
                    return
            session = request.session
            if LOGIN_REFERER_KEY in session:
                event.redirect_location = session[LOGIN_REFERER_KEY]
                del session[LOGIN_REFERER_KEY]
            else:
                catalog = get_utility(ICatalog)
                query = And(Eq(catalog['object_types'], get_interface_base_name(IMovieTheater)),
                            Or(Eq(catalog['role:msc:manager'], principal_id),
                               Eq(catalog['role:msc:operator'], principal_id),
                               Eq(catalog['role:msc:contributor'], principal_id),
                               Eq(catalog['role:msc:reader'], principal_id)))
                theaters = list(CatalogResultSet(CatalogQuery(catalog).query(query)))
                if len(theaters) == 1:
                    theater = theaters[0]
                    event.redirect_location = absolute_url(theater, request, 'admin')
                elif len(theaters) > 1:
                    event.redirect_location = absolute_url(request.root, request,
                                                          'select-admin-theater.html')
                else:
                    event.redirect_location = absolute_url(request.context, request)

except ImportError:
    pass
