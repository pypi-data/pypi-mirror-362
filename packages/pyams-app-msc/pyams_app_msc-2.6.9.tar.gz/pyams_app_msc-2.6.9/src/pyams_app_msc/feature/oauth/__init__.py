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

"""PyAMS_app_msc.feature.oauth module

This module is used to handle OAuth authentication, and initialize user profile
on successful login.
"""

import mimetypes

import requests
from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPOk
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from pyams_app_msc.feature.profile import IUserProfile
from pyams_zmi.interfaces.profile import IUserProfile as IZMIProfile

__docformat__ = 'restructuredtext'


try:

    from pyams_auth_oauth.interfaces import IOAuthUser

    @subscriber(IObjectAddedEvent, context_selector=IOAuthUser)
    def handle_new_oauth_user(event):
        """Handle new OAuth user"""
        folder = event.newParent
        if folder is None:
            return
        user_info = event.object
        principal_info = folder.get_principal(principal_id=f'{folder.prefix}:{user_info.user_id}', info=True)
        if principal_info is None:
            return
        profile = IUserProfile(principal_info)
        profile.firstname = user_info.first_name
        profile.lastname = user_info.last_name
        profile.email = user_info.email
        if user_info.picture:
            response = requests.get(user_info.picture)
            if response.status_code == HTTPOk.code:
                zmi_profile = IZMIProfile(principal_info)
                content_type = response.headers.get('content-type')
                if content_type:
                    filename = f'profile{mimetypes.guess_extension(content_type)}'
                else:
                    filename = 'profile.jpg'
                zmi_profile.avatar = (filename, response.content)

except ImportError:
    pass
