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

from datetime import datetime

from persistent import Persistent
from pyramid.interfaces import IRequest
from zope.container.contained import Contained
from zope.copy.interfaces import ICopyHook, ResumeCopy
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_app_msc.feature.booking import IBookingContainer
from pyams_app_msc.feature.planning.interfaces import IPlanning, IPlanningTarget, ISession
from pyams_app_msc.feature.profile import IOperatorProfile
from pyams_app_msc.feature.profile.interfaces import SEATS_DISPLAY_MODE
from pyams_app_msc.interfaces import MANAGE_BOOKING_PERMISSION, MANAGE_PLANNING_PERMISSION, VIEW_PLANNING_PERMISSION
from pyams_app_msc.shared.catalog import ICatalogEntry
from pyams_app_msc.shared.theater import ICinemaRoomContainer, IMovieTheater
from pyams_app_msc.shared.theater.interfaces.audience import ICinemaAudienceContainer
from pyams_app_msc.shared.theater.interfaces.room import ROOMS_SEATS_VOCABULARY
from pyams_content.feature.filter.interfaces import IFilterValues
from pyams_content.interfaces import IObjectType
from pyams_content_api.feature.json import JSONBaseExporter
from pyams_content_api.feature.json.interfaces import IJSONExporter
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer, IPyAMSUserLayer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_sequence.workflow import get_visible_version
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.date import SH_TIME_FORMAT, format_date, format_time
from pyams_utils.factory import factory_config, get_interface_base_name
from pyams_utils.interfaces import ICacheKeyValue, MISSING_INFO
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_workflow.interfaces import IWorkflowVersions
from pyams_zmi.interfaces import IObjectLabel, SMALL_TITLE_SPAN_BREAK
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@factory_config(ISession)
class Session(Persistent, Contained):
    """Session persistent class"""

    label = FieldProperty(ISession['label'])
    _start_date = FieldProperty(ISession['start_date'])
    _duration = FieldProperty(ISession['duration'])
    _end_date = FieldProperty(ISession['end_date'])
    room = FieldProperty(ISession['room'])
    capacity = FieldProperty(ISession['capacity'])
    version = FieldProperty(ISession['version'])
    audiences = FieldProperty(ISession['audiences'])
    temporary = FieldProperty(ISession['temporary'])
    bookable = FieldProperty(ISession['bookable'])
    extern_bookable = FieldProperty(ISession['extern_bookable'])
    public_session = FieldProperty(ISession['public_session'])
    comments = FieldProperty(ISession['comments'])
    notepad = FieldProperty(ISession['notepad'])

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = tztime(value)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = tztime(value)
        self._duration = self._end_date - self._start_date

    def get_target(self):
        """Planning target getter"""
        target = get_parent(self, IPlanningTarget)
        versions = IWorkflowVersions(target, None)
        if versions is not None:
            target = versions.get_version(-1)
        return target

    def get_room(self):
        """Room getter"""
        parent = get_parent(self, IMovieTheater)
        return ICinemaRoomContainer(parent).get(self.room)

    def get_label(self):
        """Session label getter"""
        label = self.label
        if not label:
            target = self.get_target()
            if target is not None:
                label = II18n(target).query_attribute('title')
        return label or MISSING_INFO

    def get_contacts(self):
        if not self.audiences:
            return
        parent = get_parent(self, IMovieTheater)
        container = ICinemaAudienceContainer(parent)
        for audience_name in self.audiences:
            audience = container.get(audience_name)
            if audience and audience.contact:
                yield audience.contact


@adapter_config(required=ISession,
                provides=IObjectType)
def session_object_type(context):
    """Session object type getter"""
    return get_interface_base_name(ISession)


@adapter_config(name='audiences',
                required=ISession,
                provides=IFilterValues)
def session_filter_values(context):
    """Session filter values adapter"""
    yield from (
        f'audience:{audience}'
        for audience in context.audiences or ()
    )


@adapter_config(required=ISession,
                provides=ICopyHook)
class SessionCopyHook(ContextAdapter):
    """Session copy hook"""

    def __call__(self, toplevel, register):
        register(self._clean_bookings)
        raise ResumeCopy

    def _clean_bookings(self, translate):
        session = translate(self.context)
        # clear clone session bookings
        bookings = IBookingContainer(session)
        for name in list(bookings.keys()):
            del bookings[name]


@adapter_config(required=(ISession, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def get_session_label(context, request, view, formatter='html'):
    """Session label getter"""
    translate = request.localizer.translate
    target = context.get_target()
    if IMovieTheater.providedBy(target):
        label = f'({context.label})' or translate(_("Out of catalog activity"))
    else:
        label = get_object_label(target, request, view)
    rooms = getVocabularyRegistry().get(context, ROOMS_SEATS_VOCABULARY)
    return (SMALL_TITLE_SPAN_BREAK if formatter == 'html' else '{} - {}').format(
        label,
        translate(_("{room} - {date} at {start_time}")).format(
            room=rooms.by_value.get(context.room).title,
            date=format_date(context.start_date),
            start_time=format_time(context.start_date, SH_TIME_FORMAT)
        ))


@adapter_config(name='text',
                required=(ISession, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def get_session_text_label(context, request, view):
    """Session text label getter"""
    return get_session_label(context, request, view, 'text')


@adapter_config(required=(ISession, IPyAMSUserLayer, Interface),
                provides=IObjectLabel)
def get_session_user_label(context, request, view, formatter='html'):
    """Session user label getter"""
    translate = request.localizer.translate
    target = context.get_target()
    if IMovieTheater.providedBy(target):
        label = context.label or '--'
    else:
        label = get_object_label(target, request, view, formatter)
    return (SMALL_TITLE_SPAN_BREAK if formatter == 'html' else '{} - {}').format(
        label,
        translate(_("{date} at {start_time}")).format(
            date=format_date(context.start_date),
            start_time=format_time(context.start_date, SH_TIME_FORMAT)
        ))


@adapter_config(name='text',
                required=(ISession, IPyAMSUserLayer, Interface),
                provides=IObjectLabel)
def get_session_user_text_label(context, request, view):
    """Session user text label getter"""
    return get_session_user_label(context, request, view, 'text')


@adapter_config(name='short',
                required=(ISession, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def get_session_short_label(context, request, view, formatter='html'):
    """Session short label getter"""
    translate = request.localizer.translate
    label = None
    target = get_parent(context, IPlanningTarget)
    if IMovieTheater.providedBy(target):
        label = context.label
    if not label:
        versions = IWorkflowVersions(target, None)
        if versions is not None:
            target = versions.get_version(-1)
        label = get_object_label(target, request, view)
    return ('<small>{}</small><br />{}' if formatter == 'html' else '{} - {}').format(
        label,
        translate(_(" {date} at {start_time}")).format(
            date=format_date(context.start_date),
            start_time=format_time(context.start_date, SH_TIME_FORMAT)
        ))


@adapter_config(name='short-text',
                required=(ISession, IPyAMSLayer, Interface),
                provides=IObjectLabel)
def get_session_short_text_label(context, request, view):
    """Session short text label getter"""
    return get_session_short_label(context, request, view, 'text')


@adapter_config(required=ISession,
                provides=IViewContextPermissionChecker)
class SessionPermissionChecker(ContextAdapter):
    """Session permission checker"""

    edit_permission = MANAGE_PLANNING_PERMISSION


@adapter_config(required=ISession,
                provides=IPlanning)
def session_planning(context):
    """Session planning adapter"""
    target = get_parent(context, IPlanningTarget)
    return IPlanning(target, None)


@adapter_config(required=ISession,
                provides=IMovieTheater)
def session_movie_theater(context):
    """Session movie theater adapter"""
    return get_parent(context, IMovieTheater)


@adapter_config(required=(ISession, IRequest),
                provides=IJSONExporter)
class JSONSessionExporter(JSONBaseExporter):
    """JSON session exporter"""

    conversion_target = None

    def _add_seats(self, value):
        """Add capacity and confirmed seats to label"""
        if not self.context.bookable:
            return f'{value} \n'
        profile = IOperatorProfile(self.request)
        if profile.session_seats_display_mode == SEATS_DISPLAY_MODE.NONE.value:
            return f'{value} \n'
        else:
            container = IBookingContainer(self.context)
            return f'{value} \n({container.get_seats(profile.session_seats_display_mode)})'

    def convert_content(self, **params):
        result = super().convert_content(**params)
        context = self.context
        request = self.request
        result['id'] = ICacheKeyValue(context)
        result['href'] = absolute_url(context, request)
        target = get_parent(context, IPlanningTarget)
        if self.context.label:
            self.get_attribute(result, 'label', name='title', converter=self._add_seats)
        else:
            versions = IWorkflowVersions(target, None)
            if versions is not None:
                last_entry = versions.get_version()
                self.get_i18n_attribute(result, 'title', params.get('lang'),
                                        context=last_entry, converter=self._add_seats)
        self.get_attribute(result, 'start_date', 'start', converter=datetime.isoformat)
        self.get_attribute(result, 'end_date', 'end', converter=datetime.isoformat)
        self.get_attribute(result, 'room')
        self.get_attribute(result, 'capacity')
        self.get_attribute(result, 'temporary')
        self.get_attribute(result, 'bookable')
        self.get_attribute(result, 'notepad')
        if params.get('with_edit_info'):
            planning = IPlanning(target)
            edit_context = params.get('edit_context')
            if edit_context is None:
                edit_context = self.request.context
            editable = bool((planning is edit_context) and
                            request.has_permission(MANAGE_PLANNING_PERMISSION, context=planning))
            result['editable'] = editable
            result['visible'] = bool(request.has_permission(VIEW_PLANNING_PERMISSION, context=planning))
            if self.context.temporary:
                result['borderWidth'] = '3'
                result['borderStyle'] = 'dashed'
            if self.context.public_session:
                result['backgroundImage'] = 'gradient'
            if planning is edit_context:
                if not self.context.bookable:
                    if 'textColor' not in result:
                        result['textColor'] = 'var(--fc-nobookable-text)'
                        result['backgroundColor'] = 'var(--fc-nobookable-bg)'
                        result['borderColor'] = 'var(--fc-nobookable-border)'
                else:
                    if self.context.extern_bookable:
                        result['borderWidth'] = 3
                    container = IBookingContainer(context)
                    if container.free_seats < 0:
                        result['textColor'] = 'var(--fc-warning-text)'
                        result['backgroundColor'] = 'var(--fc-warning-bg)'
                        result['borderColor'] = 'var(--fc-warning-border)'
                    elif container.get_confirmed_seats() > 0:
                        result['textColor'] = 'var(--fc-accepted-text)'
                        result['backgroundColor'] = 'var(--fc-accepted-bg)'
                        result['borderColor'] = 'var(--fc-accepted-border)'
                    else:
                        result['textColor'] = 'var(--fc-enabled-text)'
                        result['backgroundColor'] = 'var(--fc-enabled-bg)'
                        result['borderColor'] = 'var(--fc-enabled-border)'
            else:
                result['textColor'] = 'var(--fc-disabled-text)'
                result['backgroundColor'] = 'var(--fc-disabled-bg)'
                result['borderColor'] = 'var(--fc-disabled-border)'
        return result


@adapter_config(name='msc_mobile_api',
                required=(ISession, IRequest),
                provides=IJSONExporter)
class JSONSessionPlanningExporter(JSONBaseExporter):
    """JSON session planning exporter"""

    conversion_target = None
    
    def convert_content(self, **params):
        result = super().convert_content(**params)
        context = self.context
        result['id'] = ICacheKeyValue(context)
        target = get_parent(context, IPlanningTarget)
        if self.context.label:
            self.get_attribute(result, 'label', name='title')
        else:
            versions = IWorkflowVersions(target, None)
            if versions is not None:
                last_entry = versions.get_version()
                self.get_i18n_attribute(result, 'title',
                                        params.get('lang'),
                                        context=last_entry)
        self.get_attribute(result, 'start_date', 'start', converter=datetime.isoformat)
        self.get_attribute(result, 'end_date', 'end', converter=datetime.isoformat)
        self.get_attribute(result,
                           name='theater',
                           context=IMovieTheater(context),
                           getter=lambda x, _attr: II18n(x).query_attribute('title', request=self.request))
        self.get_attribute(result, 'room',
                           getter=lambda x, _attr: x.get_room().name)
        self.get_attribute(result, 'capacity')
        self.get_attribute(result, 'temporary')
        self.get_attribute(result, 'bookable')
        self.get_attribute(result, 'public_session', name='public')
        self.get_attribute(result, 'notepad')
        container = IBookingContainer(context)
        self.get_attribute(result, 'session',
                           name='requested_seats',
                           context=container,
                           getter=lambda x, _attr: x.get_requested_seats())
        self.get_attribute(result, 'session',
                           name='confirmed_seats',
                           context=container,
                           getter=lambda x, _attr: x.get_confirmed_seats())
        return result


@adapter_config(name='msc_mobile_session_api',
                required=(ISession, IRequest),
                provides=IJSONExporter)
class JSONSessionFullExporter(JSONSessionPlanningExporter):
    """JSON session full exporter"""
    
    def convert_content(self, **params):
        result = super().convert_content(**params)
        context = self.context
        request = self.request
        registry = request.registry
        activity = get_parent(context, ICatalogEntry)
        if activity is not None:
            version = get_visible_version(activity)
            if version is not None:
                exporter = registry.queryMultiAdapter((version, request), IJSONExporter,
                                                      name='illustration')
                if exporter is not None:
                    result['illustration'] = exporter.to_json(**params)
        bookings = []
        append_booking = bookings.append
        booking_container = IBookingContainer(context)
        for booking in booking_container.values():
            exporter = registry.queryMultiAdapter((booking, request), IJSONExporter, name='msc_mobile_api')
            if exporter is not None:
                append_booking(exporter.to_json(**params))
        result['bookings'] = bookings
        return result
