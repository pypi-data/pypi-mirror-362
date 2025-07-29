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

from pyams_app_msc.feature.booking.interfaces import IBookingReminderTask
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_scheduler.interfaces import MANAGE_TASKS_PERMISSION
from pyams_scheduler.task.zmi import BaseTaskEditForm

__docformat__ = 'restructuredtext'


@ajax_form_config(name='properties.html',
                  context=IBookingReminderTask, layer=IPyAMSLayer,
                  permission=MANAGE_TASKS_PERMISSION)
class BookingReminderTaskEditForm(BaseTaskEditForm):
    """Booking reminder task edit form"""
