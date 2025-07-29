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

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from zope.interface import Interface
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import Bool, Text, TextLine

from pyams_app_msc.feature.booking.interfaces import BOOKING_STATUS, IBookingContainer, IBookingInfo
from pyams_app_msc.feature.planning.interfaces import IPlanning, IPlanningTarget, ISession, VERSION_INFO_VOCABULARY
from pyams_app_msc.interfaces import CANCEL_BOOKING_PERMISSION, CREATE_BOOKING_PERMISSION, MSC_MANAGER_ROLE, \
    MSC_OPERATOR_ROLE
from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.audience import ICinemaAudienceContainer
from pyams_content.feature.history.interfaces import IHistoryContainer
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.form import AddForm
from pyams_form.interfaces import DISPLAY_MODE, HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_security.interfaces import IProtectedObject
from pyams_site.interfaces import ISiteRoot
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.schema.button import SubmitButton
from pyams_template.template import template_config
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.date import format_datetime
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url, canonical_url
from pyams_utils.zodb import load_object
from pyams_viewlet.viewlet import Viewlet, viewlet_config
from pyams_zmi.utils import get_object_label

try:
    from pyams_chat.interfaces import IChatMessage, IChatMessageHandler
    from pyams_chat.message import ChatMessage
except ImportError:
    ChatMessage = None


__docformat__ = 'restructuredtext'

from pyams_app_msc import _


#
# Booking add form
#

class IBookingAddFormInfo(IBookingInfo):
    """Booking add form interface"""

    session_id = TextLine(title=_("Session ID"),
                          required=True)

    audience = TextLine(title=_("Audience"),
                        required=True)

    comments = Text(title=_("Comments"),
                    description=_("You can add optional comments to your booking request"),
                    required=False)

    send_confirmation = Bool(title=_("Get confirmation message?"),
                             description=_("If 'yes', a confirmation message will be sent to you to "
                                           "acknowledge the booking"),
                             required=True,
                             default=True)


class IBookingAddFormButtons(Interface):
    """Booking add form buttons interface"""

    add = SubmitButton(name='add',
                       title=_("Add booking for this session"))


@ajax_form_config(name='booking-new.html',
                  context=IPlanningTarget, layer=IPyAMSLayer,
                  permission=CREATE_BOOKING_PERMISSION)
class BookingAddForm(AddForm, PortalContextIndexPage):
    """Booking add form"""

    legend = _("Your new booking properties")

    fields = Fields(IBookingAddFormInfo).select('session_id', 'nb_participants',
                                                'participants_age', 'nb_accompanists',
                                                'nb_groups', 'cultural_pass',
                                                'comments', 'send_confirmation')
    buttons = Buttons(IBookingAddFormButtons)

    content_factory = IBookingInfo
    _edit_permission = CREATE_BOOKING_PERMISSION

    def get_ajax_handler(self):
        return canonical_url(self.context, self.request, self.ajax_form_handler)

    @reify
    def session(self):
        """Session getter"""
        session_id_widget = self.widgets.get('session_id')
        if session_id_widget is not None:
            session_id = session_id_widget.value
        else:
            session_id = self.request.params.get('session_id')
        if session_id:
            planning = IPlanning(self.context)
            return planning.get(session_id)
        return None

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        session_id = self.widgets.get('session_id')
        if session_id is not None:
            session_id.mode = HIDDEN_MODE
            if 'session_id' in self.request.params:
                session_id.value = self.request.params['session_id']
        audience = self.widgets.get('audience')
        if audience is not None:
            audience.mode = HIDDEN_MODE
            if 'audience' in self.request.params:
                audience.value = self.request.params['audience']

    @handler(buttons['add'])
    def handle_add(self, action):
        super().handle_add(self, action)

    def update_content(self, obj, data):
        data = data.get(self, data)
        for name in ('nb_participants', 'participants_age', 'nb_accompanists', 'nb_groups', 
                     'cultural_pass', 'comments', 'send_confirmation'):
            setattr(obj, name, data.get(name))
        obj._v_audience = data.get('audience')
        obj.recipient = self.request.principal.id
        obj.creator = self.request.principal.id

    def add(self, obj):
        del obj.session
        container = IBookingContainer(self.session, None)
        if container is not None:
            container.append(obj)
            obj.send_request_notification_message(obj._v_audience, self)


@viewlet_config(name='booking-new.header',
                context=IPlanningTarget, layer=IPyAMSLayer, view=BookingAddForm,
                manager=IFormHeaderViewletManager, weight=10)
@template_config(template='templates/booking-new-header.pt',
                 layer=IPyAMSLayer)
class NewBookingHeader(Viewlet):
    """New booking header viewlet"""

    @property
    def catalog_entry(self):
        return get_parent(self.context, IWfCatalogEntry)

    @property
    def session(self):
        return self.view.session

    @property
    def start_date(self):
        start_date = self.view.session.start_date
        return format_datetime(start_date)

    def get_version(self):
        version = VERSION_INFO_VOCABULARY.by_value.get(self.view.session.version)
        if not version:
            return None
        return self.request.localizer.translate(version.title)

    def get_audiences(self):
        theater = get_parent(self.context, IMovieTheater)
        audiences = ICinemaAudienceContainer(theater)
        return ', '.join(map(lambda x: x.name,
                             filter(lambda x: x is not None,
                                    (
                                        audiences.get(audience)
                                        for audience in self.session.audiences
                                    ))))


@adapter_config(required=(IPlanningTarget, IPyAMSLayer, BookingAddForm),
                provides=IAJAXFormRenderer)
class BookingAddFormRenderer(ContextRequestViewAdapter):
    """Booking add form renderer"""

    def render(self, changes):
        if changes is None:
            return
        if ChatMessage is not None:
            request = self.request
            session = self.view.session
            booking = self.view.finished_state.get('changes')
            translate = request.localizer.translate
            message = ChatMessage(request=request,
                                  context=session,
                                  action='notify',
                                  category='booking.created',
                                  source=request.principal,
                                  title=translate(_("New booking request")),
                                  message=translate(_("{principal}: {session}")).format(
                                      principal=request.principal.title,
                                      session=get_object_label(session, request, self.view, name='text')),
                                  url=absolute_url(session, request, 'bookings.html'),
                                  modal=True,
                                  comment=booking.comments)
            message.send()
        return {
            'status': 'redirect',
            'location': canonical_url(self.context, self.request, 'booking-ok.html')
        }


@pagelet_config(name='booking-ok.html',
                context=IPlanningTarget, layer=IPyAMSLayer)
@template_config(template='templates/booking-ok.pt',
                 layer=IPyAMSLayer)
class BookingOKView(PortalContextIndexPage):
    """Booking acknowledge view"""


#
# Booking cancel form
#

class IBookingCancelFormInfo(Interface):
    """Booking cancel form interface"""

    booking_id = TextLine(title=_("Booking ID"),
                          required=True)

    session_label = TextLine(title=_("Session"),
                             required=False,
                             readonly=True)

    comments = Text(title=_("Comments"),
                    description=_("Please add optional comments to cancel your booking"),
                    required=True)


class IBookingCancelFormButtons(Interface):
    """Booking cancel form buttons"""

    cancel = SubmitButton(name='cancel',
                          title=_("Cancel booking"))


@ajax_form_config(name='cancel-booking.html',
                  context=ISiteRoot, layer=IPyAMSLayer)
class BookingCancelForm(AddForm, PortalContextIndexPage):
    """Booking cancel form"""

    legend = _("Cancel booking")

    fields = Fields(IBookingCancelFormInfo)
    buttons = Buttons(IBookingCancelFormButtons)

    content_factory = None
    _edit_permission = CANCEL_BOOKING_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        content = self.get_content()
        session = ISession(content)
        booking_id = self.widgets.get('booking_id')
        if booking_id is not None:
            booking_id.value = ICacheKeyValue(content)
            booking_id.mode = HIDDEN_MODE
        session_label = self.widgets.get('session_label')
        if session_label is not None:
            session_label.value = get_object_label(session, self.request, self, 'text')
            session_label.mode = DISPLAY_MODE

    @handler(buttons['cancel'])
    def handle_cancel(self, action):
        super().handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        booking = self.get_content()
        request = self.request
        comments = data.get('comments')
        history = IHistoryContainer(booking, None)
        if history is not None:
            history.add_history(booking,
                                comment=comments,
                                request=request)
        booking.status = BOOKING_STATUS.CANCELLED.value
        request.registry.notify(ObjectModifiedEvent(booking))
        return booking


@adapter_config(required=(ISiteRoot, IPyAMSLayer, BookingCancelForm),
                provides=IFormContent)
def booking_cancel_form_content(context, request, form):
    """Booking cancel form content getter"""
    booking_id = request.params.get('booking_id')
    if not booking_id:
        booking_id = request.params.get('form.widgets.booking_id')
    if not booking_id:
        raise HTTPNotFound()
    booking = load_object(booking_id, context)
    if not IBookingInfo.providedBy(booking):
        raise HTTPNotFound()
    if booking.recipient != request.principal.id:
        raise HTTPForbidden()
    return booking


@adapter_config(required=(ISiteRoot, IPyAMSLayer, BookingCancelForm),
                provides=IAJAXFormRenderer)
class BookingCancelFormRenderer(ContextRequestViewAdapter):
    """Booking cancel form renderer"""

    def render(self, changes):
        if changes is None:
            return None
        if ChatMessage is not None:
            request = self.request
            booking = IBookingInfo(changes)
            session = get_parent(booking, ISession)
            translate = request.localizer.translate
            history = IHistoryContainer(booking)
            message = ChatMessage(request=request,
                                  context=session,
                                  action='notify',
                                  category='booking.cancelled',
                                  source=request.principal,
                                  title=translate(_("Cancelled booking request")),
                                  message=translate(_("{principal}: {session}")).format(
                                      principal=request.principal.title,
                                      session=get_object_label(session, request, self.view, 'text')),
                                  url=absolute_url(session, request, 'bookings.html'),
                                  modal=True,
                                  comment=list(history.values())[-1].comment)
            message.send()
        return {
            'status': 'redirect',
            'location': absolute_url(self.context, self.request, 'my-dashboard.html')
        }


if ChatMessage is not None:

    @adapter_config(name='booking.created',
                    required=IChatMessage,
                    provides=IChatMessageHandler)
    @adapter_config(name='booking.cancelled',
                    required=IChatMessage,
                    provides=IChatMessageHandler)
    class BookingChatMessageHandler(ContextAdapter):
        """Booking chat message handler"""

        def get_target(self):
            """Chat message targets getter"""
            theater = get_parent(self.context.context, IMovieTheater)
            protection = IProtectedObject(theater)
            principals = set()
            for role_id in (MSC_MANAGER_ROLE, MSC_OPERATOR_ROLE):
                for principal_id in protection.get_principals(role_id):
                    principals.add(principal_id)
            return {
                'principals': tuple(principals)
            }
