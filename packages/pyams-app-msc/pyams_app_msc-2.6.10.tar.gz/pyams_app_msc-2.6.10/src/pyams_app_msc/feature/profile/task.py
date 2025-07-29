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

"""PyAMS_app_psc.feature.profile.task module

This module provides a custom scheduler task which is used to remove
user profiles which have not been activated.
"""

import logging
from datetime import datetime, timedelta, timezone

from pyramid.events import subscriber
from transaction.interfaces import ITransactionManager
from zope.interface import implementer
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility

from pyams_app_msc.feature.profile.interfaces import IActivatedPrincipalEvent, IRegisteredPrincipalEvent, \
    IUserProfileCleanerTask
from pyams_scheduler.interfaces import IScheduler, ISchedulerProcess, SCHEDULER_NAME
from pyams_scheduler.interfaces.task import IDateTaskScheduling, SCHEDULER_TASK_DATE_MODE, TASK_STATUS_OK
from pyams_scheduler.process import TaskResettingThread
from pyams_scheduler.task import Task
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import IUnknownPrincipalInfo
from pyams_security.interfaces.names import INTERNAL_USER_ID
from pyams_security_views.interfaces.login import ILoginConfiguration
from pyams_site.interfaces import ISiteRoot, PYAMS_APPLICATION_DEFAULT_NAME, PYAMS_APPLICATION_SETTINGS_KEY
from pyams_utils.factory import create_object, factory_config
from pyams_utils.registry import get_pyramid_registry, get_utility, query_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.zodb import ZODBConnection
from pyams_zmq.interfaces import IZMQProcessStartedEvent

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


LOGGER = logging.getLogger('PyAMS (msc)')


@factory_config(IUserProfileCleanerTask)
class UserProfileCleanerTask(Task):
    """User profile cleaner task"""

    label = _("User profile cleaner")
    icon_class = 'fas fa-user'

    principal_id = INTERNAL_USER_ID
    is_zodb_task = True

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def run(self, report, **kwargs):
        """Run user profile cleaner task"""
        # check principal annotations
        utility = get_utility(IPrincipalAnnotationUtility)
        if self.user_id in utility.annotations:
            del utility.annotations[self.user_id]
        # check user profile
        sm = get_utility(ISecurityManager)
        principal = sm.get_raw_principal(self.user_id)
        if principal is not None:
            del principal.__parent__[principal.__name__]
        # remove task after execution
        if self.__parent__ is not None:
            del self.__parent__[self.__name__]
        return TASK_STATUS_OK, None


@subscriber(IZMQProcessStartedEvent, context_selector=ISchedulerProcess)
def handle_scheduler_start(event):
    """Check for profiles cleaner tasks

    Profile cleaner tasks are typically automatically deleted after their execution.
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
                if not IUserProfileCleanerTask.providedBy(task):
                    continue
                schedule_info = IDateTaskScheduling(task, None)
                if schedule_info is None:  # no date scheduling
                    continue
                now = datetime.now(timezone.utc)
                if schedule_info.active and (schedule_info.start_date < now):
                    # we add a small amount of time to be sure that scheduler and indexer
                    # processes are started...
                    schedule_info.start_date = now + timedelta(minutes=1)
                    # commit update for reset thread to get updated data!!
                    ITransactionManager(task).commit()
                    # start task resetting thread
                    LOGGER.debug(" - restarting task « {} »".format(task.name))
                    TaskResettingThread(event.object, task).start()


@subscriber(IRegisteredPrincipalEvent)
def handle_registered_profile(event):
    """Handle registered profile event"""
    scheduler = query_utility(IScheduler)
    if scheduler is None:
        return
    sm = get_utility(ISecurityManager)
    principal_id = event.object.id
    principal = sm.get_raw_principal(principal_id)
    if IUnknownPrincipalInfo.providedBy(principal):
        return
    task_id = f'profile_cleaner::{principal_id}'
    if task_id in scheduler:
        del scheduler[task_id]
    root = get_parent(scheduler, ISiteRoot)
    configuration = ILoginConfiguration(root)
    task = create_object(IUserProfileCleanerTask, user_id=principal_id)
    task.name = f'Profile cleaner: {principal_id}'
    task.schedule_mode = SCHEDULER_TASK_DATE_MODE
    scheduler_info = IDateTaskScheduling(task)
    scheduler_info.start_date = (tztime(datetime.now(timezone.utc)) +
                                 timedelta(days=configuration.activation_delay))
    scheduler_info.active = True
    scheduler[task_id] = task


@subscriber(IActivatedPrincipalEvent)
def handle_activated_profile(event):
    """Handle activated profile event"""
    scheduler = query_utility(IScheduler)
    if scheduler is None:
        return
    principal_id = event.object.id
    task_id = f'profile_cleaner::{principal_id}'
    if task_id in scheduler:
        del scheduler[task_id]
