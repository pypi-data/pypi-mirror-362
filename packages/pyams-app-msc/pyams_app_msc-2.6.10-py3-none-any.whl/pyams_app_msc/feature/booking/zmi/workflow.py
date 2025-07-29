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

from datetime import datetime, timedelta, timezone

from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface, Invalid, alsoProvides, implementer
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary, getVocabularyRegistry

from pyams_app_msc.feature.booking.interfaces import BOOKING_ACCEPTABLE_STATUS, BOOKING_CANCELLABLE_STATUS, \
    BOOKING_OPTIONABLE_STATUS, BOOKING_REFUSABLE_STATUS, BOOKING_SESSIONS_VOCABULARY, BOOKING_STATUS, \
    IAcceptedBookingWorkflowInfo, IBaseBookingWorkflowInfo, IBookingContainer, IBookingInfo
from pyams_app_msc.feature.booking.message import get_booking_message, get_booking_message_values
from pyams_app_msc.feature.booking.zmi.dashboard import IBookingElement
from pyams_app_msc.feature.booking.zmi.interfaces import IBookingAcceptedStatusTable, IBookingContainerTable, \
    IBookingForm, IBookingStatusTable, IBookingWaitingStatusTable
from pyams_app_msc.feature.messaging.interfaces import IMessagingSettings
from pyams_app_msc.feature.planning.interfaces import IPlanning, ISession
from pyams_app_msc.feature.profile import IOperatorProfile
from pyams_app_msc.feature.profile.interfaces import SEATS_DISPLAY_MODE
from pyams_app_msc.interfaces import MANAGE_BOOKING_PERMISSION
from pyams_app_msc.shared.theater.api.interfaces import MSC_PRICE_API_PATH, MSC_PRICE_API_ROUTE
from pyams_app_msc.shared.theater.interfaces import IMovieTheater, IMovieTheaterSettings
from pyams_app_msc.shared.theater.interfaces.mail import IMailTemplates
from pyams_app_msc.shared.theater.interfaces.room import ROOMS_TITLE_VOCABULARY
from pyams_app_msc.zmi import msc
from pyams_content.feature.history.interfaces import IHistoryContainer
from pyams_content.feature.history.zmi.viewlet import HistoryCommentsContentProvider
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent, IFormContent, IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager, IHelpViewletManager
from pyams_skin.schema.button import ActionButton, CloseButton, SubmitButton
from pyams_skin.viewlet.help import AlertMessage
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_utils.adapter import adapter_config
from pyams_utils.date import SH_TIME_FORMAT, format_date, format_datetime, format_time
from pyams_utils.factory import create_object
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.interfaces.form import NO_VALUE_STRING
from pyams_utils.request import query_request
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_utils.vocabulary import vocabulary_config
from pyams_utils.zodb import load_object
from pyams_viewlet.viewlet import RawContentProvider, viewlet_config
from pyams_zmi.form import AdminModalAddForm, FormGroupChecker
from pyams_zmi.helper.event import get_json_table_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IModalAddFormButtons, check_submit_button
from pyams_zmi.interfaces.table import ITableActionsColumnMenu
from pyams_zmi.table import get_row_id
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


#
# Booking actions
#

class BaseBookingMenuItem(MenuItem):
    """Base booking menu item"""

    def __new__(cls, context, request, view, manager):
        booking = IBookingInfo(context)
        if booking.archived:
            return None
        return MenuItem.__new__(cls)

    modal_target = True
    view_name = None

    def get_href(self):
        return absolute_url(IBookingInfo(self.context), self.request, self.view_name)


class BaseBookingNotifyGroup(FormGroupChecker):
    """Base booking notification group"""

    fields = Fields(IBaseBookingWorkflowInfo).select('notify_recipient', 'notify_subject', 'notify_message')
    weight = 20

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        theater = get_parent(self.context, IMovieTheater)
        templates = IMailTemplates(theater)
        values = get_booking_message_values(self.context, self.request, self)
        # generate formatted messages
        subject = self.widgets.get('notify_subject')
        if subject is not None:
            template = getattr(templates, f'{self.parent_form.template_name}_subject')
            if template:
                subject.value = template.format(**values)
        message = self.widgets.get('notify_message')
        if (message is not None) and (self.parent_form.template_name is not None):
            template = getattr(templates, f'{self.parent_form.template_name}_template')
            if template:
                message.value = template.format(**values)


#
# Booking update form
#

@viewlet_config(name='properties.menu',
                context=IBookingElement, layer=IAdminLayer, view=IBookingStatusTable,
                manager=ITableActionsColumnMenu, weight=1,
                permission=MANAGE_BOOKING_PERMISSION)
class BookingPropertiesMenuItem(BaseBookingMenuItem):
    """Booking properties menu item"""

    def __new__(cls, context, request, view, manager):
        return MenuItem.__new__(cls)

    @property
    def label(self):
        if IBookingInfo(self.context).archived:
            return _("view-booking-menu", default="View booking")
        return _("modify-booking-menu", default="Modify booking")

    view_name = 'properties.html'


@viewlet_config(name='change-session.menu',
                context=IBookingInfo, layer=IAdminLayer, view=IBookingContainerTable,
                manager=ITableActionsColumnMenu, weight=2,
                permission=MANAGE_BOOKING_PERMISSION)
@viewlet_config(name='change-session.menu',
                context=IBookingElement, layer=IAdminLayer, view=IBookingStatusTable,
                manager=ITableActionsColumnMenu, weight=2,
                permission=MANAGE_BOOKING_PERMISSION)
class BookingSessionChangeMenuItem(BaseBookingMenuItem):
    """Booking session change menu item"""

    label = _("change-booking-session-menu", default=_("Change session"))
    view_name = 'change-session.html'


@vocabulary_config(name=BOOKING_SESSIONS_VOCABULARY)
class BookingSessionsVocabulary(SimpleVocabulary):
    """Booking session vocabulary"""

    def __init__(self, context):

        def get_session_label(session, request):
            translate = request.localizer.translate
            rooms = getVocabularyRegistry().get(session, ROOMS_TITLE_VOCABULARY)
            container = IBookingContainer(session)
            profile = IOperatorProfile(request)
            if profile.session_seats_display_mode == SEATS_DISPLAY_MODE.NONE.value:
                seats = rooms.get(session.room).capacity
            else:
                seats = container.get_seats(profile.session_seats_display_mode)
            return translate(_("{room} (seats: {seats}) - {date} from {start_time} to {end_time}")).format(
                room=rooms.by_value.get(session.room).title,
                seats=seats,
                date=format_date(session.start_date,
                                 format_string=translate(_("on %A %d/%m/%Y"))),
                start_time=format_time(session.start_date, SH_TIME_FORMAT),
                end_time=format_time(session.end_date, SH_TIME_FORMAT)
            )

        terms = []
        session = ISession(context, None)
        if session is not None:
            planning = IPlanning(session, None)
            if planning is not None:
                request = query_request()
                now = tztime(datetime.now(timezone.utc))
                terms = [
                    SimpleTerm(ICacheKeyValue(session),
                               title=get_session_label(session, request))
                    for session in sorted(planning.values(),
                                          key=lambda x: x.start_date)
                    if session.start_date > now
                ]
        super().__init__(terms)


class IBookingSessionChange(Interface):
    """Booking session change interface"""

    session = Choice(title=_("Booking session"),
                     description=_("Select the session for which this booking is applied"),
                     vocabulary=BOOKING_SESSIONS_VOCABULARY,
                     required=False)


class IBookingSessionChangeButtons(Interface):
    """Booking session change buttons interface"""

    change = SubmitButton(name='change',
                          title=_("Change session"),
                          condition=check_submit_button)

    cancel = CloseButton(name='cancel',
                         title=_("Cancel"))


@ajax_form_config(name='change-session.html',
                  context=IBookingInfo, layer=IPyAMSLayer,
                  permission=MANAGE_BOOKING_PERMISSION)
@implementer(IBookingForm)
class BookingSessionChangeForm(AdminModalAddForm):
    """Booking session change form"""

    modal_class = 'modal-xl'

    @property
    def subtitle(self):
        translate = self.request.localizer.translate
        return translate(_("Booking: {}")).format(
            get_object_label(self.context, self.request, self))

    legend = _("Change booking session")
    fields = Fields(IBookingSessionChange)
    buttons = Buttons(IBookingSessionChangeButtons)
    template_name = 'update'

    no_changes_message = _("No session selected, booking was not changed.")

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        session = self.widgets.get('session')
        if session is not None:
            target_id = f'booking_{ICacheKeyValue(self.context)}_seats'
            session.object_data = {
                'ams-change-handler': 'MyAMS.helpers.select2ChangeHelper',
                'ams-select2-helper-type': 'html',
                'ams-select2-helper-url': absolute_url(self.context, self.request,
                                                       'get-free-seats.html'),
                'ams-select2-helper-argument': 'session',
                'ams-select2-helper-target': f'#{target_id}'
            }
            session.suffix = RawContentProvider(html=f'<div id="{target_id}" class="mt-2"></div>')
            alsoProvides(session, IObjectData)

    @handler(IBookingSessionChangeButtons['change'])
    def handle_change(self, action):
        old_session = self.context.session
        result = super().handle_add(self, action)
        self.finished_state.update({
            'old_session': old_session
        })
        return result

    def create_and_add(self, data):
        data = data.get(self, data)
        session_key = data.get('session')
        if session_key:
            result = self.context.set_session(session_key)
            if result is not None:
                message = data.get('notify_message') if data.get('notify_recipient') else None
                if message:
                    request = self.request
                    history = IHistoryContainer(result, None)
                    if history is not None:
                        history.add_history(result,
                                            message=message,
                                            request=request)
                    settings = IMessagingSettings(request.root, None)
                    if settings is None:
                        return result
                    mailer = settings.get_mailer()
                    if mailer is None:
                        return result
                    session = self.context.session
                    html_message = get_booking_message(_("Booking accepted"), data,
                                                       result, request, settings,
                                                       session_date=format_datetime(session.start_date))
                    if html_message is not None:
                        mailer.send(html_message)
            return result


@adapter_config(name='notify.group',
                required=(IBookingInfo, IAdminLayer, BookingSessionChangeForm),
                provides=IGroup)
class BookingSessionChangeFormNotifyGroup(BaseBookingNotifyGroup):
    """Booking session change form notify group"""

    fields = Fields(IBaseBookingWorkflowInfo).select('notify_recipient', 'notify_subject',
                                                     'notify_message')


@view_config(name='get-free-seats.html',
             context=IBookingInfo, request_type=IPyAMSLayer,
             permission=MANAGE_BOOKING_PERMISSION)
def get_free_booking_seats(request):
    """Get free booking seats"""
    new_session = request.params.get('session')
    if not new_session:
        raise HTTPBadRequest()
    if new_session == NO_VALUE_STRING:
        return Response('')
    old_session = ISession(request.context)
    booking = IBookingInfo(request.context)
    if not ISession.providedBy(new_session):
        try:
            new_session = load_object(new_session)
        except ValueError:
            raise HTTPBadRequest()
    if not ISession.providedBy(new_session):
        raise HTTPNotFound()
    translate = request.localizer.translate
    if old_session is new_session:
        message = translate(_("This booking is already registered for this session..."))
        return Response(f'<div class="alert alert-info">'
                        f'{message}'
                        f'</div>')
    booking_container = IBookingContainer(new_session)
    confirmed_seats = booking_container.get_confirmed_seats()
    if new_session.capacity < confirmed_seats + booking.nb_seats:
        message = translate(_("There are only {} free seats left in this session!")).format(
            new_session.capacity - confirmed_seats)
        return Response(f'<div class="alert alert-warning">'
                        f'{message}'
                        f'</div>')
    return Response('')


@adapter_config(required=(IBookingInfo, IAdminLayer, BookingSessionChangeForm),
                provides=IAJAXFormRenderer)
class BookingSessionChangeFormRenderer(AJAXFormRenderer):
    """Booking session change form renderer"""

    def render(self, changes):
        if changes is None:
            return super().render(changes)
        session = self.form.finished_state.get('old_session')
        theater = get_parent(session, IMovieTheater)
        table = create_object(IBookingContainerTable,
                              context=IBookingContainer(session),
                              request=self.request)
        row_id = get_row_id(table, self.context)
        return {
            'status': 'success',
            'callbacks': [
                {
                    'callback': 'MyAMS.msc.booking.changeSession',
                    'options': {
                        'old_session': ICacheKeyValue(session),
                        'new_session': self.context.session_index,
                        'row_id': row_id
                    }
                },
                get_json_table_refresh_callback(theater, self.request,
                                                IBookingWaitingStatusTable),
                get_json_table_refresh_callback(theater, self.request,
                                                IBookingAcceptedStatusTable),
            ]
        }


@viewlet_config(name='properties.divider',
                context=IBookingInfo, layer=IAdminLayer, view=IBookingContainerTable,
                manager=ITableActionsColumnMenu, weight=5,
                permission=MANAGE_BOOKING_PERMISSION)
@viewlet_config(name='properties.divider',
                context=IBookingElement, layer=IAdminLayer, view=IBookingStatusTable,
                manager=ITableActionsColumnMenu, weight=5,
                permission=MANAGE_BOOKING_PERMISSION)
class BookingPropertiesMenuDivider(MenuDivider):
    """Booking properties menu divider"""

    def __new__(cls, context, request, view, manager):
        if IBookingInfo(context).archived:
            return None
        return MenuDivider.__new__(cls)


#
# Booking workflow forms
#

@implementer(IBookingForm)
class BaseBookingAdminForm(AdminModalAddForm):
    """Base booking admin form"""

    modal_class = 'modal-xl'

    @property
    def subtitle(self):
        translate = self.request.localizer.translate
        return translate(_("Booking: {}")).format(
            get_object_label(self.context, self.request, self))

    legend = _("Booking properties")

    target_status = None
    action_label = None
    email_subject = None
    template_name = None

    def update_actions(self):
        super().update_actions()
        add = self.actions.get('add')
        if add is not None:
            add.title = self.request.localizer.translate(self.action_label)

    def create_and_add(self, data):
        data = data.get(self, data)
        context = self.context
        request = self.request
        message = data.get('notify_message') if data.get('notify_recipient') else None
        history = IHistoryContainer(context, None)
        if history is not None:
            history.add_history(context,
                                comment=data.get('notepad'),
                                message=message,
                                request=request)
        context.status = self.target_status.value
        context.price = data.get('price')
        context.notepad = data.get('notepad')
        if 'quotation_message' in data:
            context.quotation_message = data['quotation_message']
        if 'send_reminder' in data:
            context.send_reminder = data['send_reminder']
            if context.send_reminder:
                context.reminder_subject = data['reminder_subject']
                context.reminder_message = data['reminder_message']
        else:
            context.send_reminder = False
            context.reminder_subject = None
            context.reminder_message = None
        context.reminder_date = None
        request.registry.notify(ObjectModifiedEvent(context))
        if message:
            settings = IMessagingSettings(request.root, None)
            if settings is None:
                return
            mailer = settings.get_mailer()
            if mailer is None:
                return
            html_message = get_booking_message(self.email_subject, data,
                                               context, request, settings)
            if html_message is not None:
                mailer.send(html_message)


@subscriber(IObjectModifiedEvent, context_selector=IBookingInfo)
def update_booking_quotation(event):
    """Update booking quotation"""
    booking = event.object
    if booking.status == BOOKING_STATUS.ACCEPTED.value:
        booking.get_quotation(force_refresh=True)


@adapter_config(name='session.group',
                required=(IBookingInfo, IAdminLayer, BaseBookingAdminForm),
                provides=IGroup)
class SessionInfoDisplayForm(Group):
    """Session info display form"""

    _mode = DISPLAY_MODE

    legend = _("Session properties")
    fields = Fields(ISession).select('capacity') + Fields(IBookingContainer).select('free_seats')
    weight = 1

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode=False)


@adapter_config(required=(IBookingInfo, IAdminLayer, SessionInfoDisplayForm),
                provides=IFormContent)
def booking_info_display_form_content(context, request, group):
    """Booking info display form group content getter"""
    return ISession(context)


@adapter_config(name='booking.group',
                required=(IBookingInfo, IAdminLayer, BaseBookingAdminForm),
                provides=IGroup)
class BookingWorkflowInfoGroup(Group):
    """Booking info group"""

    legend = _("Booking properties")
    fields = Fields(IBaseBookingWorkflowInfo).select('created', 'nb_participants',
                                                     'participants_age', 'nb_accompanists', 
                                                     'nb_free_accompanists', 'nb_groups', 
                                                     'price', 'accompanying_ratio',
                                                     'comments', 'notepad')
    weight = 10

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        created = self.widgets.get('created')
        if created is not None:
            created.mode = DISPLAY_MODE
            created.value = format_datetime(IZopeDublinCore(self.context).created)
        participants = self.widgets.get('nb_participants')
        if participants is not None:
            participants.mode = DISPLAY_MODE
            participants.value = self.context.nb_participants
        participants_age = self.widgets.get('participants_age')
        if participants_age is not None:
            participants_age.mode = DISPLAY_MODE
            participants_age.value = self.context.participants_age
        accompanists = self.widgets.get('nb_accompanists')
        if accompanists is not None:
            accompanists.mode = DISPLAY_MODE
            accompanists.value = self.context.nb_accompanists
        free_accompanists = self.widgets.get('nb_free_accompanists')
        if free_accompanists is not None:
            free_accompanists.mode = DISPLAY_MODE
            free_accompanists.value = self.context.nb_free_accompanists
        groups = self.widgets.get('nb_groups')
        if groups is not None:
            groups.mode = DISPLAY_MODE
            groups.value = self.context.nb_groups
        price = self.widgets.get('price')
        if price is not None:
            price.value = self.context.price or ()
            theater = get_parent(self.context, IMovieTheater)
            price.object_data = {
                'ams-modules': {
                    'msc': {
                        'src': get_resource_path(msc)
                    }
                },
                'ams-change-handler': 'MyAMS.helpers.select2ChangeHelper',
                'ams-select2-helper-url':
                    absolute_url(self.request.root, self.request) +
                    self.request.registry.settings.get(f'{MSC_PRICE_API_ROUTE}_route.path',
                                                       MSC_PRICE_API_PATH).format(
                        theater_name=theater.__name__),
                'ams-select2-helper-argument': 'price_id',
                'ams-select2-helper-callback': 'MyAMS.msc.booking.priceChanged'
            }
            alsoProvides(price, IObjectData)
        ratio = self.widgets.get('accompanying_ratio')
        if ratio is not None:
            ratio.value = self.context.accompanying_ratio
        comments = self.widgets.get('comments')
        if comments is not None:
            comments.mode = DISPLAY_MODE
            comments.value = self.context.comments
        notepad = self.widgets.get('notepad')
        if notepad is not None:
            history = HistoryCommentsContentProvider(self.context, self.request, self)
            history.update()
            notepad.prefix = history


@adapter_config(name='notify.group',
                required=(IBookingInfo, IAdminLayer, BaseBookingAdminForm),
                provides=IGroup)
class BookingWorkflowNotifyGroup(BaseBookingNotifyGroup):
    """Booking workflow notification group"""

    def __new__(cls, context, request, view):
        if not view.template_name:
            return None
        return FormGroupChecker.__new__(cls)


@adapter_config(required=(IBookingInfo, IAdminLayer, BaseBookingAdminForm),
                provides=IAJAXFormRenderer)
class BaseBookingAdminFormRenderer(AJAXFormRenderer):
    """Base booking admin form renderer"""

    def render(self, changes):
        theater = get_parent(self.context, IMovieTheater)
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_refresh_callback(IBookingContainer(self.context), self.request,
                                                IBookingContainerTable),
                get_json_table_refresh_callback(theater, self.request,
                                                IBookingWaitingStatusTable),
                get_json_table_refresh_callback(theater, self.request,
                                                IBookingAcceptedStatusTable),
                {
                    'callback': 'MyAMS.msc.calendar.refreshAll'
                }
            ]
        }


#
# Cancelled booking
#

@viewlet_config(name='booking-cancel.menu',
                context=IBookingInfo, layer=IAdminLayer, view=IBookingContainerTable,
                manager=ITableActionsColumnMenu, weight=10,
                permission=MANAGE_BOOKING_PERMISSION)
@viewlet_config(name='booking-cancel.menu',
                context=IBookingElement, layer=IAdminLayer, view=IBookingStatusTable,
                manager=ITableActionsColumnMenu, weight=10,
                permission=MANAGE_BOOKING_PERMISSION)
class BookingCancelMenuItem(BaseBookingMenuItem):
    """Booking cancel menu item"""

    def __new__(cls, context, request, view, manager):
        if IBookingInfo(context).status not in BOOKING_CANCELLABLE_STATUS:
            return None
        return BaseBookingMenuItem.__new__(cls, context, request, view, manager)

    label = _("cancel-booking-menu", default="Cancel booking")
    view_name = 'booking-cancel.html'


@ajax_form_config(name='booking-cancel.html',
                  context=IBookingInfo, layer=IPyAMSLayer,
                  permission=MANAGE_BOOKING_PERMISSION)
class BookingCancelForm(BaseBookingAdminForm):
    """Booking cancel form"""

    action_label = _("Cancel booking")
    email_subject = _("Booking cancelled")
    target_status = BOOKING_STATUS.CANCELLED
    template_name = 'cancel'


#
# Refused booking
#

@viewlet_config(name='booking-refuse.menu',
                context=IBookingInfo, layer=IAdminLayer, view=IBookingContainerTable,
                manager=ITableActionsColumnMenu, weight=20,
                permission=MANAGE_BOOKING_PERMISSION)
@viewlet_config(name='booking-refuse.menu',
                context=IBookingElement, layer=IAdminLayer, view=IBookingStatusTable,
                manager=ITableActionsColumnMenu, weight=20,
                permission=MANAGE_BOOKING_PERMISSION)
class BookingRefuseMenuItem(BaseBookingMenuItem):
    """Booking refuse menu item"""

    def __new__(cls, context, request, view, manager):
        if IBookingInfo(context).status not in BOOKING_REFUSABLE_STATUS:
            return None
        return BaseBookingMenuItem.__new__(cls, context, request, view, manager)

    label = _("refuse-booking-menu", default="Refuse booking")
    view_name = 'booking-refuse.html'


@ajax_form_config(name='booking-refuse.html',
                  context=IBookingInfo, layer=IPyAMSLayer,
                  permission=MANAGE_BOOKING_PERMISSION)
class BookingRefuseForm(BaseBookingAdminForm):
    """Booking refuse form"""

    action_label = _("Refuse booking")
    email_subject = _("Booking refused")
    target_status = BOOKING_STATUS.REFUSED
    template_name = 'refuse'


#
# Temporary accepted booking
#

class IAcceptedBookingButtons(IModalAddFormButtons):
    """Accepted booking buttons interface"""

    preview_quotation = ActionButton(name='preview_quotation',
                                     title=_("Quotation preview"))


@viewlet_config(name='booking-option.menu',
                context=IBookingInfo, layer=IAdminLayer, view=IBookingContainerTable,
                manager=ITableActionsColumnMenu, weight=30,
                permission=MANAGE_BOOKING_PERMISSION)
@viewlet_config(name='booking-option.menu',
                context=IBookingElement, layer=IAdminLayer, view=IBookingStatusTable,
                manager=ITableActionsColumnMenu, weight=30,
                permission=MANAGE_BOOKING_PERMISSION)
class BookingOptionMenuItem(BaseBookingMenuItem):
    """Booking option menu item"""

    def __new__(cls, context, request, view, manager):
        if IBookingInfo(context).status not in BOOKING_OPTIONABLE_STATUS:
            return None
        return BaseBookingMenuItem.__new__(cls, context, request, view, manager)

    label = _("option-booking-menu", default="Optional booking")
    view_name = 'booking-option.html'


@ajax_form_config(name='booking-option.html',
                  context=IBookingInfo, layer=IPyAMSLayer,
                  permission=MANAGE_BOOKING_PERMISSION)
class BookingOptionForm(BaseBookingAdminForm):
    """Booking option form"""

    action_label = _("Optional booking")
    email_subject = _("Booking temporarily accepted")
    target_status = BOOKING_STATUS.OPTION
    template_name = 'option'

    buttons = Buttons(IAcceptedBookingButtons).select('preview_quotation', 'add', 'close')

    def update_actions(self):
        super().update_actions()
        preview_quotation = self.actions.get('preview_quotation')
        if preview_quotation is not None:
            preview_quotation.add_class('btn-info mr-auto')
            preview_quotation.object_data = {
                'ams-click-handler': 'MyAMS.msc.booking.previewQuotation',
                'ams-click-handler-options': {
                    'target': absolute_url(self.context, self.request, 'preview-quotation.pdf')
                }
            }
            alsoProvides(preview_quotation, IObjectData)

    @handler(IAcceptedBookingButtons['add'])
    def handle_add(self, action):
        super().handle_add(self, action)


#
# Accepted booking
#


@viewlet_config(name='booking-accept.menu',
                context=IBookingInfo, layer=IAdminLayer, view=IBookingContainerTable,
                manager=ITableActionsColumnMenu, weight=40,
                permission=MANAGE_BOOKING_PERMISSION)
@viewlet_config(name='booking-accept.menu',
                context=IBookingElement, layer=IAdminLayer, view=IBookingStatusTable,
                manager=ITableActionsColumnMenu, weight=40,
                permission=MANAGE_BOOKING_PERMISSION)
class BookingAcceptMenuItem(BaseBookingMenuItem):
    """Booking accept menu item"""

    def __new__(cls, context, request, view, manager):
        if IBookingInfo(context).status not in BOOKING_ACCEPTABLE_STATUS:
            return None
        return BaseBookingMenuItem.__new__(cls, context, request, view, manager)

    label = _("accept-booking-menu", default="Accept booking")
    view_name = 'booking-accept.html'


@ajax_form_config(name='booking-accept.html',
                  context=IBookingInfo, layer=IPyAMSLayer,
                  permission=MANAGE_BOOKING_PERMISSION)
class BookingAcceptForm(BaseBookingAdminForm):
    """Booking accept form"""

    action_label = _("Accept booking")
    email_subject = _("Booking accepted")
    target_status = BOOKING_STATUS.ACCEPTED
    template_name = 'accept'

    buttons = Buttons(IAcceptedBookingButtons).select('preview_quotation', 'add', 'close')

    def update_actions(self):
        super().update_actions()
        preview_quotation = self.actions.get('preview_quotation')
        if preview_quotation is not None:
            preview_quotation.add_class('btn-info mr-auto')
            preview_quotation.object_data = {
                'ams-click-handler': 'MyAMS.msc.booking.previewQuotation',
                'ams-click-handler-options': {
                    'target': absolute_url(self.context, self.request, 'preview-quotation.pdf')
                }
            }
            alsoProvides(preview_quotation, IObjectData)

    @handler(IAcceptedBookingButtons['add'])
    def handle_add(self, action):
        super().handle_add(self, action)


@adapter_config(name='booking.group',
                required=(IBookingInfo, IAdminLayer, BookingAcceptForm),
                provides=IGroup)
class BookingAcceptWorkflowInfoGroup(BookingWorkflowInfoGroup):
    """Booking accept workflow info group"""


@subscriber(IDataExtractedEvent, form_selector=BookingAcceptWorkflowInfoGroup)
def handle_accepted_booking_data(event):
    """Handle accepted booking form data"""
    data = event.data
    if not data.get('price'):
        event.form.widgets.errors += (Invalid(_("You must set a price to accept a booking!")),)


@adapter_config(name='notify.group',
                required=(IBookingInfo, IAdminLayer, BookingAcceptForm),
                provides=IGroup)
class BookingAcceptWorkflowNotifyGroup(BookingWorkflowNotifyGroup):
    """Booking accept workflow notification group"""

    fields = Fields(IAcceptedBookingWorkflowInfo).select('notify_recipient', 'notify_subject',
                                                         'notify_message')


@adapter_config(name='quotation.group',
                required=(IBookingInfo, IAdminLayer, BookingAcceptWorkflowNotifyGroup),
                provides=IGroup)
class BookingAcceptWorkflowQuotationGroup(FormGroupChecker):
    """Booking accept workflow quotation group"""

    fields = Fields(IAcceptedBookingWorkflowInfo).select('include_quotation', 'quotation_message')
    weight = 10

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        message = self.widgets.get('quotation_message')
        if message is not None:
            message.value = self.context.quotation_message


@adapter_config(name='reminder.group',
                required=(IBookingInfo, IAdminLayer, BookingAcceptForm),
                provides=IGroup)
class BookingAcceptWorkflowReminderGroup(FormGroupChecker):
    """Booking accept workflow reminder group"""

    def __new__(cls, context, request, view):
        theater = IMovieTheater(context)
        settings = IMovieTheaterSettings(theater)
        if not settings.reminder_delay:
            return None
        reminder_date = context.session.start_date - timedelta(days=settings.reminder_delay)
        if reminder_date < tztime(datetime.now(timezone.utc)):
            return None
        return FormGroupChecker.__new__(cls)

    fields = Fields(IBookingInfo).select('send_reminder', 'reminder_subject',
                                         'reminder_message')
    weight = 20

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        values = get_booking_message_values(self.context, self.request, self)
        theater = get_parent(self.context, IMovieTheater)
        templates = IMailTemplates(theater)
        # generate formatted messages
        subject = self.widgets.get('reminder_subject')
        if (subject is not None) and not subject.value:
            template = getattr(templates, 'reminder_subject')
            if template:
                subject.value = template.format(**values)
        message = self.widgets.get('reminder_message')
        if (message is not None) and not message.value:
            template = getattr(templates, 'reminder_template')
            if template:
                message.value = template.format(**values)


@viewlet_config(name='booking-accept.warning',
                context=IBookingInfo, layer=IAdminLayer, view=BookingAcceptForm,
                manager=IFormHeaderViewletManager, weight=10)
class BookingCapacityWarning(AlertMessage):
    """Booking capacity warning"""

    def __new__(cls, context, request, view, manager):
        capacity = ISession(context).capacity
        confirmed_seats = IBookingContainer(context).get_confirmed_seats()
        requested_seats = context.nb_participants + context.nb_accompanists
        if (confirmed_seats + requested_seats) <= capacity:
            return None
        return AlertMessage.__new__(cls)

    status = 'danger'
    _message = _("**WARNING**<br />"
                 "The session capacity is too low to accept this booking!")
    message_renderer = 'markdown'


@viewlet_config(name='booking-reminder.warning',
                context=IBookingInfo, layer=IAdminLayer, view=BookingAcceptWorkflowReminderGroup,
                manager=IHelpViewletManager, weight=10)
class BookingReminderWarning(AlertMessage):
    """Booking reminder warning"""

    status = 'info'
    message_renderer = 'markdown'

    @property
    def message(self):
        translate = self.request.localizer.translate
        theater = IMovieTheater(self.context)
        settings = IMovieTheaterSettings(theater)
        return translate(_("The reminder delay is set to {} days before session start.")).format(
            settings.reminder_delay)
