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

from pyramid.view import view_config
from zope.interface import alsoProvides

from pyams_app_msc.feature.planning.interfaces import IPlanning, ISession
from pyams_app_msc.feature.planning.zmi.session import SessionAddForm
from pyams_app_msc.interfaces import MANAGE_CATALOG_PERMISSION
from pyams_app_msc.shared.catalog.interfaces import CATALOG_ENTRY_CONTENT_TYPE
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.session import IMovieTheaterSession
from pyams_app_msc.zmi import msc
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_sequence.api.rest import find_references
from pyams_sequence.reference import get_reference_target
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.interfaces.form import NO_VALUE_STRING
from pyams_utils.url import absolute_url

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


IMovieTheaterSession['activity'].content_type = CATALOG_ENTRY_CONTENT_TYPE


@view_config(name='find-references.json',
             context=IMovieTheater, request_type=IPyAMSLayer,
             permission=USE_INTERNAL_API_PERMISSION,
             renderer='json', xhr=True)
def find_theater_references(request):
    """Returns list of references matching given query inside theater context"""
    return find_references(request, parent=request.context, validate=False)


@ajax_form_config(name='add-session.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=MANAGE_CATALOG_PERMISSION)
class MovieTheaterSessionAddForm(SessionAddForm):
    """Movie theater session add form"""

    @property
    def fields(self):
        fields = Fields(ISession).omit('duration', 'bookable',
                                       'extern_bookable', 'comments',
                                       'notepad')
        if not self.request.POST:
            fields = Fields(IMovieTheaterSession).select('activity') + fields
        return fields

    content_factory = ISession

    planning_target = None

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        activity = self.widgets.get('activity')
        if activity is not None:
            activity.prompt = True
            activity.prompt_message = self.request.localizer.translate(_("Out of catalog activity"))
            activity.ajax_url = absolute_url(self.context, self.request, 'find-references.json')
            activity.object_data = {
                'ams-modules': {
                    'msc': {
                        'src': get_resource_path(msc)
                    }
                },
                'ams-change-handler': 'MyAMS.msc.session.changeActivity'
            }
            alsoProvides(activity, IObjectData)

    def create(self, data):
        self.planning_target = IPlanning(self.context, None)
        activity = self.request.params.get(f'{self.prefix}{self.widgets.prefix}activity')
        if activity != NO_VALUE_STRING:
            target = get_reference_target(activity)
            if target is not None:
                self.planning_target = IPlanning(target, None)
        return super().create(data)

    def add(self, obj):
        self.planning_target.add_session(obj)
