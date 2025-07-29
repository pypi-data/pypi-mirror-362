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

"""PyAMS_app_msc.feature.booking.reminder module

This module provides components used to handle booking reminders.
"""

import logging
from datetime import datetime, timedelta, timezone

from pyramid.events import subscriber
from transaction.interfaces import ITransactionManager

from pyams_app_msc.feature.booking.interfaces import IBookingReminderTask
from pyams_scheduler.interfaces import ISchedulerProcess, SCHEDULER_NAME
from pyams_scheduler.interfaces.task import IDateTaskScheduling, TASK_STATUS_OK
from pyams_scheduler.process import TaskResettingThread
from pyams_scheduler.task import Task
from pyams_security.interfaces.names import INTERNAL_USER_ID
from pyams_site.interfaces import PYAMS_APPLICATION_DEFAULT_NAME, PYAMS_APPLICATION_SETTINGS_KEY
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.registry import get_pyramid_registry
from pyams_utils.timezone import gmtime
from pyams_utils.zodb import ZODBConnection, load_object
from pyams_zmq.interfaces import IZMQProcessStartedEvent

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


LOGGER = logging.getLogger('PyAMS (msc)')


@factory_config(IBookingReminderTask)
class BookingReminderTask(Task):
    """Booking reminder task"""

    label = _("Booking reminder")
    icon_class = 'fas fa-envelope'

    principal_id = INTERNAL_USER_ID
    is_zodb_task = True

    def __init__(self, booking):
        super().__init__()
        self.booking_oid = ICacheKeyValue(booking)

    def run(self, report, **kwargs):
        booking = load_object(self.booking_oid, self)
        if booking is None:
            LOGGER.debug(f">>> can't find booking with OID {self.booking_oid}")
        else:
            booking.send_reminder_message()
        # remove task after execution!
        if self.__parent__ is not None:
            del self.__parent__[self.__name__]
        return TASK_STATUS_OK, None


@subscriber(IZMQProcessStartedEvent, context_selector=ISchedulerProcess)
def handle_scheduler_start(event):
    """Check for scheduler reminder tasks

    Booking reminders tasks are typically automatically deleted after their execution.
    If tasks with passed execution date are still present in the scheduler, this is generally
    because scheduler was stopped at task execution time; so tasks which where not run are
    re-scheduled at process startup in a very near future...
    """
    with ZODBConnection() as root:
        registry = get_pyramid_registry()
        application_name = registry.settings.get(PYAMS_APPLICATION_SETTINGS_KEY,
                                                 PYAMS_APPLICATION_DEFAULT_NAME)
        application = root.get(application_name)
        sm = application.getSiteManager()  # pylint: disable=invalid-name
        scheduler = sm.get(SCHEDULER_NAME)
        if scheduler is not None:
            LOGGER.debug("Checking pending scheduler tasks on {!r}".format(scheduler))
            for task in scheduler.values():
                if not IBookingReminderTask.providedBy(task):
                    continue
                schedule_info = IDateTaskScheduling(task, None)
                if schedule_info is None:  # no date scheduling
                    continue
                now = gmtime(datetime.now(timezone.utc))
                if schedule_info.active and (schedule_info.start_date < now):
                    # we add a small amount of time to be sure that scheduler and indexer
                    # processes are started...
                    schedule_info.start_date = now + timedelta(minutes=1)
                    # commit update for reset thread to get updated data!!
                    ITransactionManager(task).commit()
                    # start task resetting thread
                    LOGGER.debug(" - restarting task « {} »".format(task.name))
                    TaskResettingThread(event.object, task).start()
