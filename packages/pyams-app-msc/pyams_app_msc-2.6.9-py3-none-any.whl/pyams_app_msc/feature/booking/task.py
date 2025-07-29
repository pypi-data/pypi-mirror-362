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

import sys
import traceback
from datetime import datetime, timedelta

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Le

from pyams_app_msc.feature.booking import IBookingInfo
from pyams_app_msc.feature.booking.interfaces import IBookingArchiverTask
from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.feature.profile import IUserProfile
from pyams_app_msc.shared.theater import IMovieTheater, IMovieTheaterSettings
from pyams_catalog.query import CatalogResultSet
from pyams_layer.skin import apply_skin
from pyams_scheduler.interfaces.task import TASK_STATUS_FAIL, TASK_STATUS_OK
from pyams_scheduler.task import Task
from pyams_security.utility import get_principal
from pyams_site.interfaces import ISiteRoot
from pyams_utils.factory import factory_config, get_interface_base_name
from pyams_utils.registry import get_local_registry, get_utility, set_local_registry
from pyams_utils.request import check_request
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_zmi.skin import AdminSkin
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@factory_config(IBookingArchiverTask)
class BookingArchiverTask(Task):
    """Bookings archiver task"""

    label = _("Bookings archiver task")
    icon_class = 'fas fa-lock'
    
    is_zodb_task = True

    def run(self, report, **kwargs):
        """Run sessions archiver task"""
        try:
            report.writeln('Sessions archiver task', prefix='### ')
            old_registry = get_local_registry()
            try:
                request = check_request()
                apply_skin(request, AdminSkin)
                root = get_parent(self, ISiteRoot)
                set_local_registry(root)
                catalog = get_utility(ICatalog)
                now = tztime(datetime.now())
                query = And(Eq(catalog['object_types'], get_interface_base_name(IBookingInfo)),
                            Le(catalog['planning_end_date'], now))
                for booking in CatalogResultSet(CatalogQuery(catalog).query(query,
                                                                            sort_index='planning_start_date')):
                    if booking.archived:
                        continue
                    theater = IMovieTheater(booking, None)
                    if theater is None:
                        continue
                    settings = IMovieTheaterSettings(theater)
                    session = ISession(booking, None)
                    if session.start_date < (now - timedelta(hours=settings.booking_retention_duration)):
                        report.writeln(f" - {get_object_label(session, request, self, name='text')}"
                                       f" - {get_object_label(booking, request, self)}")
                        recipient = get_principal(principal_id=booking.recipient)
                        if recipient is not None:
                            recipient_profile = IUserProfile(recipient, None)
                            if recipient_profile is not None:
                                booking.recipient_establishment = recipient_profile.establishment
                        booking.archived = True
            finally:
                set_local_registry(old_registry)
            return TASK_STATUS_OK, None
        except Exception:
            report.writeln('**An error occurred**', suffix='\n')
            report.write_exception(*sys.exc_info())
            return TASK_STATUS_FAIL, None
