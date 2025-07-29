#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS MSC application.include module

This module is used for Pyramid integration
"""

import re

from pyams_app_msc.feature.booking.api import MSC_BOOKING_SEARCH_API_ROUTE
from pyams_app_msc.feature.booking.api.interfaces import MSC_BOOKING_API_PATH, MSC_BOOKING_API_ROUTE, \
    MSC_BOOKING_SEARCH_API_PATH, MSC_BOOKING_VALIDATION_API_PATH, MSC_BOOKING_VALIDATION_API_ROUTE
from pyams_app_msc.feature.planning.api.interfaces import MSC_PLANNING_API_PATH, MSC_PLANNING_API_ROUTE, \
    MSC_SESSION_API_PATH, MSC_SESSION_API_ROUTE
from pyams_app_msc.feature.tmdb.interfaces import TMDB_SEARCH_PATH, TMDB_SEARCH_ROUTE
from pyams_app_msc.interfaces import CANCEL_BOOKING_PERMISSION, CREATE_BOOKING_PERMISSION, MANAGE_BOOKING_PERMISSION, \
    MANAGE_CATALOG_PERMISSION, MANAGE_PLANNING_PERMISSION, MANAGE_THEATER_PERMISSION, MSC_CLIENT_ROLE, \
    MSC_CONTRIBUTOR_ROLE, MSC_MANAGER_ROLE, MSC_OPERATOR_ROLE, MSC_OWNER_ROLE, MSC_READER_ROLE, MSC_SITES_MANAGER_ROLE, \
    VIEW_BOOKING_PERMISSION, VIEW_CATALOG_PERMISSION, VIEW_PLANNING_PERMISSION, VIEW_THEATER_PERMISSION
from pyams_app_msc.shared.theater.api.interfaces import MSC_PRICE_API_PATH, MSC_PRICE_API_ROUTE, MSC_ROOM_API_PATH, \
    MSC_ROOM_API_ROUTE
from pyams_content.interfaces import COMMENT_CONTENT_PERMISSION, CREATE_CONTENT_PERMISSION, CREATE_VERSION_PERMISSION, \
    MANAGE_CONTENT_PERMISSION, MANAGE_SITE_PERMISSION, MANAGE_SITE_TREE_PERMISSION, MANAGE_TOOL_PERMISSION, \
    PUBLISH_CONTENT_PERMISSION, WEBMASTER_ROLE
from pyams_layer.interfaces import MANAGE_SKIN_PERMISSION
from pyams_portal.interfaces import DESIGNER_ROLE
from pyams_security.interfaces.base import MANAGE_ROLES_PERMISSION, ROLE_ID, VIEW_SYSTEM_PERMISSION
from pyams_security.interfaces.names import ADMIN_USER_ID, SYSTEM_ADMIN_ROLE

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


def include_package(config):
    """Pyramid package include"""

    # add translations
    config.add_translation_dirs('pyams_app_msc:locales')

    # override PyAMS_content packages
    config.include('pyams_content_es')
    config.include('pyams_content_themes')
    config.include('pyams_content_api')

    # register permissions
    config.register_permission({
        'id': MANAGE_THEATER_PERMISSION,
        'title': _("Manage movie theater properties")
    })
    config.register_permission({
        'id': VIEW_THEATER_PERMISSION,
        'title': _("View movie theater properties")
    })
    config.register_permission({
        'id': MANAGE_CATALOG_PERMISSION,
        'title': _("Manage movie theater activities catalog")
    })
    config.register_permission({
        'id': VIEW_CATALOG_PERMISSION,
        'title': _("Read movie theater activities catalog")
    })
    config.register_permission({
        'id': VIEW_PLANNING_PERMISSION,
        'title': _("View sessions planning on movie theater activities")
    })
    config.register_permission({
        'id': MANAGE_PLANNING_PERMISSION,
        'title': _("Manage sessions planning on movie theater activities")
    })
    config.register_permission({
        'id': CREATE_BOOKING_PERMISSION,
        'title': _("Create booking request for movie theater activity")
    })
    config.register_permission({
        'id': MANAGE_BOOKING_PERMISSION,
        'title': _("Manage bookings for movie theater activity")
    })
    config.register_permission({
        'id': VIEW_BOOKING_PERMISSION,
        'title': _("View booking information for movie theater activity")
    })
    config.register_permission({
        'id': CANCEL_BOOKING_PERMISSION,
        'title': _("Cancel own bookings on movie theater activity")
    })

    # upgrade system manager roles
    config.upgrade_role(SYSTEM_ADMIN_ROLE,
                        permissions={
                            MANAGE_THEATER_PERMISSION, VIEW_THEATER_PERMISSION,
                            MANAGE_CATALOG_PERMISSION, VIEW_CATALOG_PERMISSION,
                            VIEW_PLANNING_PERMISSION, MANAGE_PLANNING_PERMISSION,
                            CREATE_BOOKING_PERMISSION, MANAGE_BOOKING_PERMISSION,
                            VIEW_BOOKING_PERMISSION, CANCEL_BOOKING_PERMISSION
                        })
    config.upgrade_role(WEBMASTER_ROLE,
                        managers={
                            ROLE_ID.format(MSC_SITES_MANAGER_ROLE)
                        })
    config.upgrade_role(DESIGNER_ROLE,
                        managers={
                            ROLE_ID.format(MSC_MANAGER_ROLE)
                        })

    # register new roles
    config.register_role({
        'id': MSC_SITES_MANAGER_ROLE,
        'title': _("MSC: Sites manager"),
        'permissions': {
            MANAGE_SITE_TREE_PERMISSION, MANAGE_ROLES_PERMISSION,
            VIEW_THEATER_PERMISSION, VIEW_SYSTEM_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE)
        }
    })
    config.register_role({
        'id': MSC_MANAGER_ROLE,
        'title': _("MSC: Theater manager"),
        'permissions': {
            MANAGE_THEATER_PERMISSION, VIEW_THEATER_PERMISSION,
            MANAGE_SITE_PERMISSION, MANAGE_SKIN_PERMISSION,
            MANAGE_TOOL_PERMISSION, MANAGE_CATALOG_PERMISSION,
            VIEW_CATALOG_PERMISSION, MANAGE_PLANNING_PERMISSION,
            VIEW_PLANNING_PERMISSION, VIEW_BOOKING_PERMISSION,
            MANAGE_BOOKING_PERMISSION, CANCEL_BOOKING_PERMISSION,
            VIEW_SYSTEM_PERMISSION, MANAGE_ROLES_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(MSC_SITES_MANAGER_ROLE),
            ROLE_ID.format(MSC_MANAGER_ROLE)
        },
        'set_as_operator': False
    })
    config.register_role({
        'id': MSC_OPERATOR_ROLE,
        'title': _("MSC: Theater operator"),
        'permissions': {
            CREATE_CONTENT_PERMISSION, CREATE_VERSION_PERMISSION,
            MANAGE_CONTENT_PERMISSION, PUBLISH_CONTENT_PERMISSION,
            VIEW_THEATER_PERMISSION, MANAGE_CATALOG_PERMISSION,
            VIEW_CATALOG_PERMISSION, MANAGE_PLANNING_PERMISSION,
            VIEW_PLANNING_PERMISSION, VIEW_BOOKING_PERMISSION,
            MANAGE_BOOKING_PERMISSION, CANCEL_BOOKING_PERMISSION,
            VIEW_SYSTEM_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(MSC_MANAGER_ROLE)
        },
        'set_as_operator': False
    })
    config.register_role({
        'id': MSC_CONTRIBUTOR_ROLE,
        'title': _("MSC: Theater contributor"),
        'permissions': {
            CREATE_CONTENT_PERMISSION, CREATE_VERSION_PERMISSION,
            VIEW_CATALOG_PERMISSION, MANAGE_CATALOG_PERMISSION,
            VIEW_PLANNING_PERMISSION, VIEW_BOOKING_PERMISSION,
            VIEW_SYSTEM_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(MSC_MANAGER_ROLE),
            ROLE_ID.format(MSC_OPERATOR_ROLE)
        },
        'set_as_operator': False
    })
    config.register_role({
        'id': MSC_READER_ROLE,
        'title': _("MSC: Theater consultant"),
        'permissions': {
            COMMENT_CONTENT_PERMISSION, VIEW_THEATER_PERMISSION,
            VIEW_CATALOG_PERMISSION, VIEW_PLANNING_PERMISSION,
            VIEW_BOOKING_PERMISSION, VIEW_SYSTEM_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE),
            ROLE_ID.format(MSC_MANAGER_ROLE)
        },
        'set_as_operator': False
    })
    config.register_role({
        'id': MSC_CLIENT_ROLE,
        'title': _("MSC: Theater client"),
        'permissions': {
            VIEW_CATALOG_PERMISSION, CREATE_BOOKING_PERMISSION, CANCEL_BOOKING_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE)
        },
        'set_as_operator': False
    })
    config.register_role({
        'id': MSC_OWNER_ROLE,
        'title': _("MSC: Reservation owner"),
        'permissions': {
            VIEW_CATALOG_PERMISSION, MANAGE_BOOKING_PERMISSION, CANCEL_BOOKING_PERMISSION
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE)
        },
        'set_as_operator': False
    })

    # register custom REST API route
    settings = config.registry.settings
    config.add_route(TMDB_SEARCH_ROUTE,
                     settings.get(f'{TMDB_SEARCH_ROUTE}_route.path',
                                  TMDB_SEARCH_PATH))

    config.add_route(MSC_PRICE_API_ROUTE,
                     settings.get(f'{MSC_PRICE_API_ROUTE}_route.path',
                                  MSC_PRICE_API_PATH))

    config.add_route(MSC_ROOM_API_ROUTE,
                     settings.get(f'{MSC_ROOM_API_ROUTE}_route.path',
                                  MSC_ROOM_API_PATH))
    
    config.add_route(MSC_PLANNING_API_ROUTE,
                     settings.get(f'{MSC_PLANNING_API_ROUTE}_route.path',
                                  MSC_PLANNING_API_PATH))
    
    config.add_route(MSC_SESSION_API_ROUTE,
                     settings.get(f'{MSC_SESSION_API_ROUTE}_route.path',
                                  MSC_SESSION_API_PATH))
    
    config.add_route(MSC_BOOKING_SEARCH_API_ROUTE,
                     settings.get(f'{MSC_BOOKING_SEARCH_API_ROUTE}_route.path',
                                  MSC_BOOKING_SEARCH_API_PATH))
    
    config.add_route(MSC_BOOKING_API_ROUTE,
                     settings.get(f'{MSC_BOOKING_API_ROUTE}_route.path',
                                  MSC_BOOKING_API_PATH))
    
    config.add_route(MSC_BOOKING_VALIDATION_API_ROUTE,
                     settings.get(f'{MSC_BOOKING_VALIDATION_API_ROUTE}_route.path',
                                  MSC_BOOKING_VALIDATION_API_PATH))
    
    try:
        import pyams_zmi  # pylint: disable=import-outside-toplevel,unused-import
    except ImportError:
        config.scan(ignore=[re.compile(r'pyams_app_msc\..*\.zmi\.?.*').search])
    else:
        config.scan()
