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

__docformat__ = 'restructuredtext'

from pyams_app_msc.feature.booking.interfaces import IBookingArchiverTask
from pyams_app_msc.feature.booking.task import BookingArchiverTask
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_scheduler.interfaces import MANAGE_TASKS_PERMISSION
from pyams_scheduler.interfaces.folder import ITaskContainer
from pyams_scheduler.task.zmi import BaseTaskAddForm, BaseTaskEditForm
from pyams_scheduler.zmi import TaskContainerTable
from pyams_skin.viewlet.menu import MenuItem
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager

from pyams_app_msc import _


@viewlet_config(name='add-booking-archiver-task.menu',
                context=ITaskContainer, layer=IAdminLayer, view=TaskContainerTable,
                manager=IContextAddingsViewletManager, weight=220,
                permission=MANAGE_TASKS_PERMISSION)
class BookingArchiverTaskAddMenu(MenuItem):
    """Booking archiver task add menu"""

    label = _("Add booking archiver task...")
    href = 'add-booking-archiver-task.html'
    modal_target = True


@ajax_form_config(name='add-booking-archiver-task.html',
                  context=ITaskContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TASKS_PERMISSION)
class BookingArchiverTaskAddForm(BaseTaskAddForm):
    """Booking archiver task add form"""

    content_factory = IBookingArchiverTask
    content_label = BookingArchiverTask.label


@ajax_form_config(name='properties.html',
                  context=IBookingArchiverTask, layer=IPyAMSLayer,
                  permission=MANAGE_TASKS_PERMISSION)
class BookingArchiverTaskEditForm(BaseTaskEditForm):
    """Booking archiver task edit form"""
