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

from persistent import Persistent
from pyramid.authorization import ALL_PERMISSIONS, Allow
from pyramid.events import subscriber
from pyramid.interfaces import IRequest, IView
from pyramid.renderers import render
from pyramid.response import Response
from zope.container.contained import Contained
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.feature.booking.interfaces import BOOKING_STATUS, IBookingContainer, IBookingInfo, \
    IBookingReminderTask, IBookingTarget
from pyams_app_msc.feature.booking.message import get_booking_message_values
from pyams_app_msc.feature.messaging.interfaces import IMessagingSettings
from pyams_app_msc.feature.planning.interfaces import IPlanning, ISession
from pyams_app_msc.feature.profile.interfaces import IUserProfile
from pyams_app_msc.feature.quotation import Quotation
from pyams_app_msc.interfaces import CANCEL_BOOKING_PERMISSION, MANAGE_BOOKING_PERMISSION
from pyams_app_msc.shared.catalog import ICatalogEntry
from pyams_app_msc.shared.theater.interfaces import BOOKING_CANCEL_MODE, IMovieTheater, IMovieTheaterSettings
from pyams_app_msc.shared.theater.interfaces.audience import ICinemaAudienceContainer
from pyams_app_msc.shared.theater.interfaces.mail import IMailTemplates
from pyams_app_msc.shared.theater.interfaces.price import ICinemaPriceContainer
from pyams_catalog.utils import index_object
from pyams_content.feature.history import IHistoryContainer
from pyams_content.feature.history.interfaces import IHistoryTarget
from pyams_content.interfaces import IObjectType
from pyams_content_api.feature.json import IJSONExporter, JSONBaseExporter
from pyams_file.property import FileProperty
from pyams_i18n.interfaces import II18n
from pyams_mail.interfaces import IPrincipalMailInfo
from pyams_mail.message import HTMLMessage
from pyams_scheduler.interfaces import IScheduler
from pyams_scheduler.interfaces.task import IDateTaskScheduling, SCHEDULER_TASK_DATE_MODE
from pyams_security.interfaces import ISecurityManager, IViewContextPermissionChecker
from pyams_security.interfaces.base import FORBIDDEN_PERMISSION
from pyams_security.interfaces.names import ADMIN_USER_ID
from pyams_security.interfaces.notification import INotificationSettings
from pyams_security.security import ProtectedObjectMixin
from pyams_security.utility import get_principal
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import create_object, factory_config, get_interface_base_name
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.registry import get_pyramid_registry, get_utility, query_utility
from pyams_utils.request import check_request
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.zodb import load_object, volatile_property
from pyams_workflow.interfaces import IWorkflowVersions
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@implementer(IView)
class FakeView:
    """Fake view"""

    def __call__(self, context, request):
        return Response('')

    
@factory_config(IBookingInfo)
@implementer(IHistoryTarget)
class BookingInfo(ProtectedObjectMixin, Persistent, Contained):
    """Booking information"""

    creator = FieldProperty(IBookingInfo['creator'])
    recipient = FieldProperty(IBookingInfo['recipient'])
    recipient_establishment = FieldProperty(IBookingInfo['recipient_establishment'])
    status = FieldProperty(IBookingInfo['status'])
    nb_participants = FieldProperty(IBookingInfo['nb_participants'])
    participants_age = FieldProperty(IBookingInfo['participants_age'])
    nb_accompanists = FieldProperty(IBookingInfo['nb_accompanists'])
    nb_free_accompanists = FieldProperty(IBookingInfo['nb_free_accompanists'])
    accompanying_ratio = FieldProperty(IBookingInfo['accompanying_ratio'])
    nb_groups = FieldProperty(IBookingInfo['nb_groups'])
    price = FieldProperty(IBookingInfo['price'])
    cultural_pass = FieldProperty(IBookingInfo['cultural_pass'])
    comments = FieldProperty(IBookingInfo['comments'])
    notepad = FieldProperty(IBookingInfo['notepad'])
    archived = FieldProperty(IBookingInfo['archived'])
    quotation_number = FieldProperty(IBookingInfo['quotation_number'])
    quotation_message = FieldProperty(IBookingInfo['quotation_message'])
    quotation = FileProperty(IBookingInfo['quotation'])
    send_update = FieldProperty(IBookingInfo['send_update'])
    update_subject = FieldProperty(IBookingInfo['update_subject'])
    update_message = FieldProperty(IBookingInfo['update_message'])
    send_reminder = FieldProperty(IBookingInfo['send_reminder'])
    reminder_subject = FieldProperty(IBookingInfo['reminder_subject'])
    reminder_message = FieldProperty(IBookingInfo['reminder_message'])
    reminder_date = FieldProperty(IBookingInfo['reminder_date'])

    def __acl__(self):
        result = [
            (Allow, ADMIN_USER_ID, ALL_PERMISSIONS)
        ]
        theater = get_parent(self, IMovieTheater)
        settings = IMovieTheaterSettings(theater)
        if settings.booking_cancel_mode != BOOKING_CANCEL_MODE.FORBIDDEN.value:
            result.append((Allow, self.recipient, CANCEL_BOOKING_PERMISSION))
        return result

    def get_recipient(self, with_info=True):
        """Recipient principal getter"""
        principal = get_principal(None, principal_id=self.recipient)
        if with_info:
            profile = IUserProfile(principal, None)
            return principal, profile
        return principal

    @property
    def nb_seats(self):
        """Total seats count"""
        return (self.nb_participants or 0) + (self.nb_accompanists or 0)

    def get_price(self):
        """Price getter"""
        if not self.price:
            return None
        theater = IMovieTheater(self)
        return ICinemaPriceContainer(theater).get(self.price)

    @volatile_property
    def session(self):
        """Booking session getter"""
        return get_parent(self, IBookingTarget)

    @property
    def session_index(self):
        """Booking session index value getter"""
        return ICacheKeyValue(self.session)

    def set_session(self, new_session):
        """Update booking session"""
        if not ISession.providedBy(new_session):
            new_session = load_object(new_session, self)
        if (new_session is self.session) or not ISession.providedBy(new_session):
            return
        old_bookings = self.__parent__
        new_bookings = IBookingContainer(new_session)
        new_bookings.append(self)
        index_object(self)
        del self.session
        if self.quotation is not None:
            del self.quotation
            self.get_quotation(force_refresh=True)
        del old_bookings[ICacheKeyValue(self)]
        registry = get_pyramid_registry()
        registry.notify(ObjectModifiedEvent(self))
        return self

    def get_quotation_number(self):
        theater = IMovieTheater(self)
        settings = IMovieTheaterSettings(theater)
        return settings.get_quotation_number()

    def get_quotation(self, force_refresh=False, store=True, **kwargs):
        quotation = self.quotation
        if force_refresh or (not quotation):
            quotation_number = self.quotation_number
            if not quotation_number:
                quotation_number = self.quotation_number = self.get_quotation_number()
            quotation = (f'{quotation_number}.pdf',
                         bytes(Quotation(self, quotation_number, **kwargs)))
            if store:
                self.quotation = quotation
        return quotation

    def send_request_notification_message(self, audience, view):
        """Send request confirmation message to recipient and to theater operator"""
        request = check_request()
        settings = IMessagingSettings(request.root, None)
        if settings is None:
            return None
        mailer = settings.get_mailer()
        if mailer is None:
            return None
        translate = request.localizer.translate
        # get target email
        sm = get_utility(ISecurityManager)
        target_email = None
        profile = IUserProfile(request.principal, None)
        if profile is not None:
            target_email = profile.email
        if not target_email:
            principal = sm.get_raw_principal(request.principal.id)
            mail_info = IPrincipalMailInfo(principal, None)
            if mail_info is not None:
                target_email = [
                    f'{name} <{address}>'
                    for name, address in mail_info.get_addresses()
                ]
                if len(target_email) > 0:
                    target_email = target_email[0]
        # get contact email
        theater = IMovieTheater(self)
        contact_email = None
        audience = ICinemaAudienceContainer(theater).get(audience)
        if audience is not None:
            contact = audience.contact
            if contact is not None:
                contact_email = f'{contact.name} <{contact.email_address}>' if contact.email_address else None
        if not contact_email:
            contact_email = theater.contact_email
        notifications_settings = INotificationSettings(sm)
        # send notification message
        if contact_email:
            message_body = render('templates/booking-new-notify.pt',
                                  request=request,
                                  value={
                                      'settings': notifications_settings,
                                      'theater': theater,
                                      'booking': self,
                                      'session': self.session,
                                      'title': get_object_label(self.session, request, view,
                                                                name='short-text'),
                                      'sender': sm.get_principal(request.principal.id)
                                  })
            message = HTMLMessage(subject=translate(_("{} Booking request notification"))
                                      .format(settings.subject_prefix),
                                  from_addr=f'{settings.source_name} <{settings.source_address}>',
                                  to_addr=contact_email,
                                  reply_to=target_email,
                                  html=message_body)
            mailer.send(message)
        # send confirmation message
        if getattr(self, 'send_confirmation', False):
            if target_email:
                # create inner message
                message_body = render('templates/booking-new-ack.pt',
                                      request=request,
                                      value={
                                          'settings': notifications_settings,
                                          'booking': self,
                                          'session': self.session,
                                          'title': get_object_label(self.session, request, view,
                                                                    name='short-text'),
                                          'sender': sm.get_principal(request.principal.id)
                                      })
                message = HTMLMessage(subject=translate(_("{} Booking request confirmation"))
                                          .format(settings.subject_prefix),
                                      from_addr=f'{settings.source_name} <{settings.source_address}>',
                                      to_addr=target_email,
                                      reply_to=contact_email,
                                      html=message_body)
                mailer.send(message)

    def send_reminder_message(self):
        """Send reminder message"""
        if not (self.send_reminder and self.reminder_message):
            return
        root = get_parent(self, ISiteRoot)
        settings = IMessagingSettings(root, None)
        if settings is None:
            return
        mailer = settings.get_mailer()
        if mailer is None:
            return
        sm = get_utility(ISecurityManager)
        principal = sm.get_raw_principal(self.recipient)
        mail_info = IPrincipalMailInfo(principal, None)
        if mail_info is None:
            return
        mail_addresses = [
            f'{name} <{address}>'
            for name, address in mail_info.get_addresses()
        ]
        message = HTMLMessage(f'{settings.subject_prefix} {self.reminder_subject}',
                              from_addr=f'{settings.source_name} <{settings.source_address}>',
                              to_addr=mail_addresses,
                              html=self.reminder_message)
        mailer.send(message)
        self.reminder_date = tztime(datetime.now(timezone.utc))


@adapter_config(required=IBookingInfo,
                provides=IObjectType)
def booking_object_type(context):
    """Booking object type value adapter"""
    return get_interface_base_name(IBookingInfo)


@adapter_config(required=IBookingInfo,
                provides=IViewContextPermissionChecker)
class BookingInfoPermissionChecker(ContextAdapter):
    """Booking permission checker"""

    @property
    def edit_permission(self):
        if self.context.archived:
            return FORBIDDEN_PERMISSION
        return MANAGE_BOOKING_PERMISSION


@adapter_config(name='delete',
                required=IBookingInfo,
                provides=IViewContextPermissionChecker)
class BookingInfoDeletePermissionChecker(ContextAdapter):
    """Booking delete permission checker"""

    @property
    def edit_permission(self):
        if self.context.archived or (self.context.status == BOOKING_STATUS.ACCEPTED.value):
            return FORBIDDEN_PERMISSION
        return MANAGE_BOOKING_PERMISSION


@adapter_config(required=IBookingInfo,
                provides=IBookingContainer)
def booking_container_adapter(context):
    """Booking container adapter"""
    return context.__parent__


@adapter_config(required=IBookingInfo,
                provides=ISession)
def booking_session_adapter(context):
    """Booking session adapter"""
    return context.session


@adapter_config(required=IBookingInfo,
                provides=IPlanning)
def booking_planning_adapter(context):
    """Booking planning adapter"""
    return get_parent(context, IPlanning)


@adapter_config(required=IBookingInfo,
                provides=IMovieTheater)
def booking_theater_adapter(context):
    """Booking theater adapter"""
    return get_parent(context, IMovieTheater)


@adapter_config(required=IBookingInfo,
                provides=IUserProfile)
def booking_user_profile_adapter(context):
    """Booking user profile adapter"""
    _, profile = context.get_recipient()
    return profile


@subscriber(IObjectModifiedEvent, context_selector=IBookingInfo)
def handle_modified_booking(event):
    """Handle modified booking"""
    scheduler = query_utility(IScheduler)
    if scheduler is None:
        return
    booking = IBookingInfo(event.object)
    theater = IMovieTheater(booking)
    task_id = f'reminder::{ICacheKeyValue(booking)}'
    if task_id in scheduler:
        del scheduler[task_id]
    settings = IMovieTheaterSettings(theater)
    if not settings.reminder_delay:
        return
    reminder_date = booking.session.start_date - timedelta(days=settings.reminder_delay)
    if reminder_date < tztime(datetime.now(timezone.utc)):
        return
    if booking.send_reminder and not booking.reminder_date:
        task = create_object(IBookingReminderTask, booking=booking)
        task.name = f'Booking {task_id}'
        task.schedule_mode = SCHEDULER_TASK_DATE_MODE
        scheduler_info = IDateTaskScheduling(task)
        scheduler_info.start_date = reminder_date
        scheduler_info.active = True
        scheduler[task_id] = task


@adapter_config(name='msc_mobile_api',
                required=(IBookingInfo, IRequest),
                provides=IJSONExporter)
class JSONBookingInfoSessionExporter(JSONBaseExporter):
    """JSON booking info session exporter"""
    
    conversion_target = None
    
    def convert_content(self, **params):
        result = super().convert_content(**params)
        context = self.context
        result['id'] = ICacheKeyValue(context)
        recipient = get_principal(principal_id=context.recipient)
        session = ISession(context)
        if params.get('with_session_info'):
            request = self.request
            registry = request.registry
            exporter = registry.queryMultiAdapter((session, request), IJSONExporter,
                                                  name='msc_mobile_api')
            if exporter is not None:
                result['session'] = exporter.to_json()
        entry = get_parent(session, ICatalogEntry)
        if entry is not None:
            version = IWorkflowVersions(entry).get_last_versions()[0]
            self.get_attribute(result,
                               name='activity',
                               context=version,
                               getter=lambda x, _attr: II18n(x).query_attribute('title'))
        else:
            self.get_attribute(result,
                               name='activity',
                               context=session,
                               getter=lambda x, _attr: x.label)
        theater = get_parent(session, IMovieTheater)
        self.get_attribute(result,
                           name='theater',
                           context=theater,
                           getter=lambda x, _attr: II18n(x).query_attribute('title'))
        self.get_attribute(result, 'recipient',
                           context=recipient,
                           getter=lambda x, _attr: x.title)
        profile = IUserProfile(recipient, None)
        if profile is not None:
            self.get_attribute(result,
                               name='establishment',
                               context=profile,
                               getter=lambda x, _attr: x.establishment)
        self.get_attribute(result, 'status')
        self.get_attribute(result, 'nb_participants')
        self.get_attribute(result, 'participants_age')
        self.get_attribute(result, 'nb_accompanists')
        self.get_attribute(result, 'accompanying_ratio')
        self.get_attribute(result, 'nb_groups')
        self.get_attribute(result, 'cultural_pass')
        self.get_attribute(result, 'price')
        self.get_attribute(result,
                           name='price_label',
                           context=context.get_price(),
                           getter=lambda x, _attr: II18n(x).query_attribute('name') if x is not None else None)
        self.get_attribute(result, 'comments')
        history = IHistoryContainer(context, None)
        if history is not None:
            result['notepads'] = [
                comment.comment
                for comment in history.values()
                if comment.comment
            ]
        self.get_attribute(result,
                           name='can_update',
                           getter=lambda x, _attr: self.request.has_permission(MANAGE_BOOKING_PERMISSION,
                                                                               context=x))
        return result


@adapter_config(name='msc_mobile_validation_api',
                required=(IBookingInfo, IRequest),
                provides=IJSONExporter)
class JSONBookingInfoValidationExporter(JSONBookingInfoSessionExporter):
    """JSON booking info validation exporter"""
    
    conversion_target = None

    def get_prices(self, _context, _attr):
        """Available prices getter"""
        theater = IMovieTheater(self.context)
        return [
            {
                'value': price.__name__,
                'label': price.name
            }
            for price in ICinemaPriceContainer(theater).get_active_items()
        ]

    def convert_content(self, **params):
        result = super().convert_content(**params)
        context = self.context
        self.get_attribute(result,
                           name='available_prices',
                           getter=self.get_prices)
        values = get_booking_message_values(context, self.request, FakeView())
        theater = IMovieTheater(context)
        templates = IMailTemplates(theater)
        template = templates.accept_subject
        if template:
            result['notify_subject'] = template.format(**values)
        template = templates.accept_template
        if template:
            result['notify_message'] = template.format(**values)
        settings = IMovieTheaterSettings(theater)
        if settings.reminder_delay:
            session = ISession(context)
            reminder_date = session.start_date - timedelta(days=settings.reminder_delay)
            can_send_reminder = result['can_send_reminder'] = reminder_date >= tztime(datetime.now(timezone.utc))
            if can_send_reminder:
                template = templates.reminder_subject
                if template:
                    result['reminder_subject'] = template.format(**values)
                template = templates.reminder_template
                if template:
                    result['reminder_message'] = template.format(**values)
        else:
            result['can_send_reminder'] = False
        return result
    