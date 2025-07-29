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

from pyramid.view import view_config

from pyams_app_msc.feature.profile import IUserProfile
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import MANAGE_SYSTEM_PERMISSION, VIEW_SYSTEM_PERMISSION
from pyams_utils.registry import query_utility
from pyams_utils.rest import STATUS

__docformat__ = 'restructuredtext'


@view_config(name='get-principals.json',
             context=IMovieTheater, request_type=IPyAMSLayer,
             renderer='json',
             permission=VIEW_SYSTEM_PERMISSION)
def get_theater_principals(request):
    """Get theater principals"""
    query = request.params.get('term')
    if not query:
        return {
            'status': STATUS.ERROR.value,
            'message': "Missing arguments"
        }
    manager = query_utility(ISecurityManager)
    return {
        'status': STATUS.SUCCESS.value,
        'results': [
            {
                'id': principal.id,
                'text': principal.title
            }
            for principal in manager.find_principals(query)
            if request.has_permission(MANAGE_SYSTEM_PERMISSION, context=request.context) or
               (request.context.__name__ in (IUserProfile(principal).local_theaters or ()))
        ]
    }
