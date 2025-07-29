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

"""PyAMS MSC application.interfaces module

"""


#
# Custom permissions
#

MANAGE_THEATER_PERMISSION = 'msc.ManageTheater'
'''Permission required to manage theater properties and configuration'''

VIEW_THEATER_PERMISSION = 'msc.ViewTheater'
'''Permission required to view theater properties'''

MANAGE_CATALOG_PERMISSION = 'msc.ManageCatalog'
'''Permission required to manage theater activities catalog and reservations'''

VIEW_CATALOG_PERMISSION = 'msc.ViewCatalog'
'''Permission required to read theater activities catalog and reservations'''

CREATE_BOOKING_PERMISSION = 'msc.CreateBooking'
'''Permission required to create a booking request for a theater activity'''

VIEW_PLANNING_PERMISSION = 'msc.ViewPlanning'
'''Permission required to view sessions planning'''

MANAGE_PLANNING_PERMISSION = 'msc.ManagePlanning'
'''Permission required to manage sessions planning'''

VIEW_BOOKING_PERMISSION = 'msc.ViewBooking'
'''Permission required to view booking information for a theater activity'''

MANAGE_BOOKING_PERMISSION = 'msc.ManageBooking'
'''Permission required to manage bookings on a theater activity'''

CANCEL_BOOKING_PERMISSION = 'msc.CancelBooking'
'''Permission required to cancel a booking on a theater activity'''


#
# Custom roles
#

MSC_SITES_MANAGER_ROLE = 'msc.SitesManager'
'''Site manager role can create and manage sites and theaters'''

MSC_MANAGER_ROLE = 'msc.Manager'
'''Manager role has all permissions on a theater'''

MSC_OPERATOR_ROLE = 'msc.Operator'
'''Operator role can manage theater activities catalog and reservations'''

MSC_CONTRIBUTOR_ROLE = 'msc.Contributor'
'''Contributor role can prepare activities for catalog, but can't publish them'''

MSC_READER_ROLE = 'msc.Reader'
'''Reader role have read-only access to theater catalog and reservations'''

MSC_CLIENT_ROLE = 'msc.Client'
'''Client role can ask for reservations on planned theater activities'''

MSC_OWNER_ROLE = 'msc.Owner'
'''Owner role can manage it's reservations on planned theater activities'''
