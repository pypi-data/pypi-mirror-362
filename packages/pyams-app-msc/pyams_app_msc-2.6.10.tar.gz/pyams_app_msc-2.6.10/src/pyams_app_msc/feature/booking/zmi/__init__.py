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

import datetime
import json
from datetime import timezone

from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.response import Response
from pyramid.view import view_config
from pyramid_mailer.message import Attachment
from zope.interface import Interface, Invalid, alsoProvides, implementer
from zope.lifecycleevent import ObjectModifiedEvent
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility

from pyams_app_msc.feature.booking.interfaces import BOOKING_STATUS, BOOKING_STATUS_VOCABULARY, \
    IAcceptedBookingWorkflowInfo, IBookingAcceptInfo, IBookingContainer, IBookingInfo, IBookingTarget
from pyams_app_msc.feature.booking.message import get_booking_message, get_booking_message_values
from pyams_app_msc.feature.booking.zmi.dashboard import get_booking_element
from pyams_app_msc.feature.booking.zmi.interfaces import IBookingAcceptedStatusTable, IBookingContainerTable, \
    IBookingContainerView, IBookingForm, IBookingWaitingStatusTable
from pyams_app_msc.feature.messaging import IMessagingSettings
from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.feature.profile.interfaces import IOperatorProfile, IUserProfile, SEATS_DISPLAY_MODE, \
    USER_PROFILE_KEY
from pyams_app_msc.feature.profile.zmi.widget import PrincipalSelectFieldWidget
from pyams_app_msc.interfaces import MANAGE_BOOKING_PERMISSION, VIEW_BOOKING_PERMISSION
from pyams_app_msc.shared.theater.api.interfaces import MSC_PRICE_API_PATH, MSC_PRICE_API_ROUTE
from pyams_app_msc.shared.theater.interfaces import IMovieTheater, IMovieTheaterSettings
from pyams_app_msc.shared.theater.interfaces.mail import IMailTemplates
from pyams_app_msc.zmi import msc
from pyams_content.feature.history.interfaces import IHistoryContainer
from pyams_content.feature.history.zmi.viewlet import HistoryCommentsContentProvider
from pyams_content.zmi import content_js
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.form import apply_changes
from pyams_form.group import Group
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent, IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_mail.interfaces import IPrincipalMailInfo
from pyams_mail.message import HTMLMessage
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces import ISecurityManager
from pyams_security.utility import get_principal
from pyams_skin.interfaces.viewlet import IContentPrefixViewletManager, IFormHeaderViewletManager, IHelpViewletManager
from pyams_skin.schema.button import ActionButton, CloseButton, SubmitButton
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_skin.viewlet.help import AlertMessage
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.interfaces.form import NO_VALUE_STRING
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalDisplayForm, AdminModalEditForm, \
    FormGroupChecker, SimpleAddFormRenderer, SimpleEditFormRenderer
from pyams_zmi.helper.container import delete_container_element
from pyams_zmi.helper.event import get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle, IModalDisplayFormButtons, check_submit_button
from pyams_zmi.interfaces.table import ITableElementEditor, ITableWithActions
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager
from pyams_zmi.table import I18nColumnMixin, IconColumn, InnerTableAdminView, NameColumn, Table, TableElementEditor, \
    TrashColumn
from pyams_zmi.utils import get_object_hint, get_object_label

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@factory_config(IBookingContainerTable)
@implementer(ITableWithActions)
class BookingContainerTable(Table):
    """Booking target container table"""

    @reify
    def data_attributes(self):
        """Attributes getter"""
        attributes = super().data_attributes
        attributes.setdefault('table', {}).update({
            'data-ams-modules': json.dumps({
                'content': {
                    'src': get_resource_path(content_js)
                }
            })
        })
        return attributes

    display_if_empty = True


@adapter_config(required=(IBookingTarget, IAdminLayer, IBookingContainerTable),
                provides=IValues)
class BookingContainerTableValues(ContextRequestViewAdapter):
    """Booking container table values adapter"""

    @property
    def values(self):
        """Booking target container table values getter"""
        yield from IBookingContainer(self.context).values()


@adapter_config(name='creator',
                required=(IBookingContainer, IAdminLayer, IBookingContainerTable),
                provides=IColumn)
class BookingContainerCreatorColumn(NameColumn):
    """Booking container creator column"""

    i18n_header = _("Creator")
    weight = 10

    def get_value(self, obj):
        """Creator column value getter"""
        return get_principal(self.request, obj.creator).title


@adapter_config(name='recipient',
                required=(IBookingContainer, IAdminLayer, IBookingContainerTable),
                provides=IColumn)
class BookingContainerRecipientColumn(NameColumn):
    """Booking container recipient column"""

    i18n_header = _("Recipient")
    weight = 15

    def get_value(self, obj):
        """Recipient column value getter"""
        return get_principal(self.request, obj.recipient).title


@adapter_config(name='establishment',
                required=(IBookingContainer, IAdminLayer, IBookingContainerTable),
                provides=IColumn)
class BookingContainerEstablishmentColumn(NameColumn):
    """Booking container establishment column"""

    i18n_header = _("Establishment")
    weight = 20

    def get_value(self, obj):
        """Establishment column value getter"""
        principals = get_utility(IPrincipalAnnotationUtility)
        recipient = get_principal(self.request, obj.recipient)
        annotations = principals.getAnnotations(recipient)
        if annotations is None:
            return MISSING_INFO
        profile_info = IUserProfile(annotations.get(USER_PROFILE_KEY), None)
        if profile_info is None:
            return MISSING_INFO
        result = profile_info.establishment or MISSING_INFO
        if obj.cultural_pass:
            label = self.request.localizer.translate(_("Cultural pass"))
            result += (f' <img title="{label}" alt="" '
                       f'      class="mx-1 mt-n1 hint" '
                       f'      src="/--static--/msc/img/pass-culture.webp" '
                       f'      width="24" height="24" />')
        return result


@adapter_config(name='status',
                required=(IBookingContainer, IAdminLayer, IBookingContainerTable),
                provides=IColumn)
class BookingContainerStatusColumn(I18nColumnMixin, GetAttrColumn):
    """Booking container status column"""

    i18n_header = _("Status")
    weight = 30

    def get_value(self, obj):
        """Status column value getter"""
        translate = self.request.localizer.translate
        status = BOOKING_STATUS_VOCABULARY.by_value.get(obj.status)
        return translate(status.title) if status is not None else MISSING_INFO


@adapter_config(name='seats',
                required=(IBookingContainer, IAdminLayer, IBookingContainerTable),
                provides=IColumn)
class BookingContainerSeatsColumn(I18nColumnMixin, GetAttrColumn):
    """Booking container seats column"""

    i18n_header = _("Seats")
    weight = 40

    def get_value(self, obj):
        """Seats column value getter"""
        return f'{obj.nb_participants} + {obj.nb_accompanists}'


@adapter_config(name='quotation',
                required=(IBookingContainer, IAdminLayer, IBookingContainerTable),
                provides=IColumn)
class BookingContainerQuotationColumn(IconColumn):
    """Booking container quotation column"""

    icon_class = 'fas fa-file-pdf'
    hint = _("Quotation")
    weight = 45

    @staticmethod
    def checker(obj):
        return (obj.status == BOOKING_STATUS.ACCEPTED.value) and obj.quotation

    def render_cell(self, item):
        result = super().render_cell(item)
        if result:
            quotation = item.quotation
            return (f'<a href="{absolute_url(quotation, self.request)}"'
                    f'   target="_blank">{result}</a>')
        return result


@adapter_config(name='archive',
                required=(IBookingContainer, IAdminLayer, IBookingContainerTable),
                provides=IColumn)
class BookingContainerArchiveColumn(IconColumn):
    """Booking container archive column"""

    css_classes = {
        'th': 'action',
        'td': 'text-danger'
    }
    icon_class = 'fas fa-archive'
    hint = _("Archived booking")
    weight = 50

    def checker(self, item):
        return IBookingInfo(item).archived


@adapter_config(name='trash',
                required=(IBookingContainer, IAdminLayer, IBookingContainerTable),
                provides=IColumn)
class BookingContainerTrashColumn(TrashColumn):
    """Booking container trash column"""

    object_data = {
        'ams-modules': 'container',
        'ams-delete-target': 'delete-booking.json'
    }


@view_config(name='delete-booking.json',
             context=IBookingContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_BOOKING_PERMISSION)
def delete_booking(request):
    """Delete booking"""
    return delete_container_element(request, container_factory=IBookingContainer)


@viewlet_config(name='bookings-table',
                context=IBookingTarget, layer=IAdminLayer,
                view=IBookingContainerView,
                manager=IContentPrefixViewletManager, weight=10)
class BookingContainerTableView(InnerTableAdminView):
    """Booking target container table view"""

    table_class = IBookingContainerTable
    table_label = _("Current session bookings")

    container_intf = IBookingContainer


@pagelet_config(name='bookings.html',
                context=IBookingTarget, layer=IPyAMSLayer,
                permission=VIEW_BOOKING_PERMISSION)
@implementer(IBookingContainerView)
class BookingContainerModalView(AdminModalDisplayForm):
    """Booking target container modal view"""

    @property
    def subtitle(self):
        """Subtitle getter"""
        translate = self.request.localizer.translate
        subtitle = translate(_("Session bookings"))
        profile = IOperatorProfile(self.request)
        if profile.session_seats_display_mode != SEATS_DISPLAY_MODE.NONE.value:
            container = IBookingContainer(self.context)
            if container is not None:
                subtitle += translate(_(" (Seats: {})")).format(container.get_seats(profile.session_seats_display_mode))
        return subtitle

    modal_class = 'modal-xl'


@adapter_config(required=(IBookingTarget, IAdminLayer, IBookingContainerView),
                provides=IFormTitle)
def booking_target_edit_form_title(context, request, form):
    """Booking target edit form title"""
    translate = request.localizer.translate
    theater = get_parent(context, IMovieTheater)
    hint = get_object_hint(context, request, form)
    label = get_object_label(context, request, form)
    return TITLE_SPAN_BREAK.format(
        get_object_label(theater, request, form),
        translate(_("{}: {}")).format(hint, label) if hint else label)


#
# Booking add and edit forms
#

@adapter_config(required=(IBookingInfo, IAdminLayer, Interface),
                provides=IObjectLabel)
def get_booking_label(context, request, view):
    """Booking label getter"""
    recipient = get_principal(request, context.recipient)
    result = recipient.title
    profile_info = IUserProfile(recipient, None)
    if (profile_info is None) or not profile_info.establishment:
        return result
    return (f'{result} ({profile_info.get_structure_type()} - '
            f'{profile_info.establishment}, {profile_info.establishment_address.city} - '
            f'{profile_info.phone_number})')


@viewlet_config(name='add-booking.action',
                context=IBookingTarget, layer=IAdminLayer,
                view=IBookingContainerTable,
                manager=IToolbarViewletManager, weigth=20,
                permission=MANAGE_BOOKING_PERMISSION)
class BookingAddAction(ContextAddAction):
    """Booking add action"""

    label = _("Add booking")
    href = 'add-booking.html'

    def __new__(cls, context, request, view, manager):
        session = ISession(context, None)
        if (session is not None) and not session.bookable:
            return None
        return ContextAddAction.__new__(cls)

    def get_href(self):
        return absolute_url(self.context, self.request, f'++booking++/{self.href}')


@ajax_form_config(name='add-booking.html',
                  context=IBookingContainer, layer=IPyAMSLayer,
                  permission=MANAGE_BOOKING_PERMISSION)
class BookingAddForm(AdminModalAddForm):
    """Booking add form"""

    modal_class = 'modal-xl'

    subtitle = _("New booking")
    legend = _("New booking properties")

    fields = Fields(IBookingInfo).select('recipient', 'status',
                                         'nb_participants', 'participants_age',
                                         'nb_accompanists', 'nb_seats',
                                         'nb_free_accompanists', 'accompanying_ratio',
                                         'nb_groups', 'price', 'cultural_pass',
                                         'comments', 'notepad')
    fields['recipient'].widget_factory = PrincipalSelectFieldWidget

    content_factory = IBookingInfo

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        status = self.widgets.get('status')
        if status is not None:
            status.mode = DISPLAY_MODE
        nb_seats = self.widgets.get('nb_seats')
        if nb_seats is not None:
            nb_seats.mode = DISPLAY_MODE
            seats_data = {
                'ams-change-handler': 'MyAMS.msc.booking.seatsChanged',
                'ams-change-handler-options': {
                    'target': nb_seats.id
                }
            }
            nb_participants = self.widgets.get('nb_participants')
            if nb_participants is not None:
                nb_participants.object_data = seats_data
                alsoProvides(nb_participants, IObjectData)
            nb_accompanists = self.widgets.get('nb_accompanists')
            if nb_accompanists is not None:
                nb_accompanists.object_data = seats_data
                alsoProvides(nb_accompanists, IObjectData)
        price = self.widgets.get('price')
        if price is not None:
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

    def update_actions(self):
        super().update_actions()
        validate = self.actions.get('validate')
        if validate is not None:
            validate.add_class('btn-info')

    def update_content(self, obj, data):
        request = self.request
        form_data = data.get(self, data)
        notepad = form_data.get('notepad')
        message = form_data.get('notify_message') if form_data.get('notify_recipient') else None
        if notepad or message:
            history = IHistoryContainer(obj, None)
            if history is not None:
                history.add_history(obj,
                                    comment=notepad,
                                    message=message,
                                    request=request)
        changes = apply_changes(self, obj, form_data)
        obj.creator = request.principal.id
        accepted = form_data.get('accepted', False)
        if accepted:
            obj.status = BOOKING_STATUS.ACCEPTED.value
            if 'quotation_message' in form_data:
                obj.quotation_message = form_data['quotation_message']
            request.registry.notify(ObjectModifiedEvent(obj))
            if message:
                settings = IMessagingSettings(request.root, None)
                if settings is None:
                    return changes
                mailer = settings.get_mailer()
                if mailer is None:
                    return changes
                html_message = get_booking_message(_("Booking accepted"), form_data,
                                                   obj, request, settings)
                if html_message is not None:
                    mailer.send(html_message)
        return changes

    def add(self, obj):
        IBookingContainer(self.context).append(obj)


@adapter_config(required=(IBookingContainer, IAdminLayer, BookingAddForm),
                provides=IFormTitle)
def booking_add_form_title(context, request, form):
    """Booking add form title"""
    session = get_parent(context, ISession)
    return booking_target_edit_form_title(session, request, form)


@adapter_config(name='validate.group',
                required=(IBookingContainer, IAdminLayer, BookingAddForm),
                provides=IGroup)
class BookingAddFormValidateGroup(FormGroupChecker):
    """Booking add form validate group"""

    fields = Fields(IBookingAcceptInfo).select('accepted')
    weight = 20


@subscriber(IDataExtractedEvent, form_selector=BookingAddFormValidateGroup)
def handle_validate_group_data(event):
    """Handle validate group data"""
    data = event.data
    if data.get('accepted'):
        parent_form = event.form.parent_form
        if NO_VALUE_STRING in parent_form.widgets['price'].value:
            event.form.widgets.errors += (Invalid(_("You must set a price to accept a booking!")),)


@adapter_config(name='notify.group',
                required=(IBookingContainer, IAdminLayer, BookingAddFormValidateGroup),
                provides=IGroup)
class BookingAddFormNotifyGroup(FormGroupChecker):
    """Booking add form notify group"""

    fields = Fields(IAcceptedBookingWorkflowInfo).select('notify_recipient', 'notify_subject',
                                                         'notify_message')
    weight = 20

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        notify = self.widgets.get('notify_recipient')
        if notify is not None:
            notify.value = ()
        # generate formatted messages
        theater = get_parent(self.context, IMovieTheater)
        templates = IMailTemplates(theater)
        values = get_booking_message_values(self.context, self.request, self)
        subject = self.widgets.get('notify_subject')
        if subject is not None:
            template = getattr(templates, 'accept_subject')
            if template:
                subject.value = template.format(**values)
        message = self.widgets.get('notify_message')
        if message is not None:
            template = getattr(templates, f'accept_template')
            if template:
                message.value = template.format(**values)


@adapter_config(name='quotation.group',
                required=(IBookingContainer, IAdminLayer, BookingAddFormNotifyGroup),
                provides=IGroup)
class BookingAddFormQuotationGroup(FormGroupChecker):
    """Booking add form quotation group"""

    fields = Fields(IAcceptedBookingWorkflowInfo).select('include_quotation', 'quotation_message')
    weight = 10

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        include_quotation = self.widgets.get('include_quotation')
        if include_quotation is not None:
            include_quotation.value = ()


@adapter_config(required=(IBookingContainer, IAdminLayer, BookingAddForm),
                provides=IAJAXFormRenderer)
class BookingAddFormRenderer(SimpleAddFormRenderer):
    """Booking add form renderer"""

    table_factory = IBookingContainerTable

    def render(self, changes):
        result = super().render(changes)
        if changes:
            result.setdefault('callbacks', []).append({
                'callback': 'MyAMS.msc.calendar.refresh',
                'options': {
                    'room_id': ISession(self.context).room
                }
            })
        return result


@adapter_config(required=(IBookingInfo, IAdminLayer, IBookingContainerTable),
                provides=ITableElementEditor)
class BookingInfoEditor(TableElementEditor):
    """Booking info editor"""


@adapter_config(required=(IBookingInfo, IAdminLayer, IBookingForm),
                provides=IFormTitle)
def booking_edit_form_title(context, request, form):
    """Booking workflow management form title"""
    theater = get_parent(context, IMovieTheater)
    session = get_parent(context, ISession)
    return TITLE_SPAN_BREAK.format(
        get_object_label(theater, request, form),
        get_object_label(session, request, form))


class IBookingEditFormButtons(Interface):
    """Booking edit form buttons"""

    preview_quotation = ActionButton(name='preview_quotation',
                                     title=_("Quotation preview"))

    reset_quotation = ActionButton(name='reset_quotation',
                                   title=_("Reset quotation"),
                                   condition=lambda form:
                                       (form.context.status == BOOKING_STATUS.ACCEPTED.value) and
                                       check_submit_button(form))

    apply = SubmitButton(name='apply',
                         title=_("Apply"),
                         condition=check_submit_button)

    close = CloseButton(name='close',
                        title=_("Cancel"))


@ajax_form_config(name='properties.html',
                  context=IBookingInfo, layer=IPyAMSLayer,
                  permission=VIEW_BOOKING_PERMISSION)
@implementer(IBookingForm)
class BookingPropertiesEditForm(AdminModalEditForm):
    """Booking info properties edit form"""

    @property
    def subtitle(self):
        translate = self.request.localizer.translate
        return translate(_("Booking: {}")).format(
            get_object_label(self.context, self.request, self))

    modal_class = 'modal-xl'
    legend = _("Booking properties")

    fields = Fields(IBookingInfo).select('creator', 'recipient', 'status',
                                         'nb_participants', 'participants_age',
                                         'nb_accompanists', 'nb_seats',
                                         'nb_free_accompanists', 'accompanying_ratio',
                                         'nb_groups', 'price', 'cultural_pass',
                                         'comments', 'notepad')
    fields['recipient'].widget_factory = PrincipalSelectFieldWidget

    @reify
    def buttons(self):
        if self.mode == DISPLAY_MODE:
            return Buttons(IModalDisplayFormButtons)
        return Buttons(IBookingEditFormButtons)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        creator = self.widgets.get('creator')
        if creator is not None:
            creator.mode = DISPLAY_MODE
        status = self.widgets.get('status')
        if status is not None:
            status.mode = DISPLAY_MODE
        nb_seats = self.widgets.get('nb_seats')
        if nb_seats is not None:
            nb_seats.mode = DISPLAY_MODE
            seats_data = {
                'ams-change-handler': 'MyAMS.msc.booking.seatsChanged',
                'ams-change-handler-options': {
                    'target': nb_seats.id
                }
            }
            nb_participants = self.widgets.get('nb_participants')
            if nb_participants is not None:
                nb_participants.object_data = seats_data
                alsoProvides(nb_participants, IObjectData)
            nb_accompanists = self.widgets.get('nb_accompanists')
            if nb_accompanists is not None:
                nb_accompanists.object_data = seats_data
                alsoProvides(nb_accompanists, IObjectData)
        price = self.widgets.get('price')
        if price is not None:
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
        notepad = self.widgets.get('notepad')
        if notepad is not None:
            history = HistoryCommentsContentProvider(self.context, self.request, self)
            history.update()
            notepad.prefix = history
            if f'{self.prefix}{self.widgets.prefix}notepad' not in self.request.params:
                notepad.value = ''

    def update_actions(self):
        super().update_actions()
        preview_quotation = self.actions.get('preview_quotation')
        reset_quotation = self.actions.get('reset_quotation')
        if preview_quotation is not None:
            preview_quotation.add_class('btn-info')
            if reset_quotation is None:
                preview_quotation.add_class('mr-auto')
            preview_quotation.object_data = {
                'ams-click-handler': 'MyAMS.msc.booking.previewQuotation',
                'ams-click-handler-options': {
                    'target': absolute_url(self.context, self.request, 'preview-quotation.pdf')
                }
            }
            alsoProvides(preview_quotation, IObjectData)
        if reset_quotation is not None:
            reset_quotation.add_class('btn-info mr-auto')
            reset_quotation.object_data = {
                'ams-click-handler': 'MyAMS.msc.booking.resetQuotation',
                'ams-click-handler-options': {
                    'target': absolute_url(self.context, self.request, 'reset-quotation.json')
                }
            }
            alsoProvides(reset_quotation, IObjectData)

    @handler(IBookingEditFormButtons['apply'])
    def handle_apply(self, action):
        return super().handle_apply(self, action)

    def apply_changes(self, data):
        form_data = data.get(self, data)
        update_message = form_data.get('update_message') if form_data.get('send_update') else None
        history = IHistoryContainer(self.context, None)
        if history is not None:
            history.add_history(self.context,
                                comment=form_data.get('notepad'),
                                request=self.request)
        result = super().apply_changes(data)
        if result and update_message:
            settings = IMessagingSettings(self.request.root, None)
            if settings is None:
                return
            mailer = settings.get_mailer()
            if mailer is None:
                return
            html_message = self.get_message(form_data, self.context, self.request, settings)
            if html_message is not None:
                mailer.send(html_message)
        return result

    def get_message(self, data, context, request, settings):
        sm = get_utility(ISecurityManager)
        principal = sm.get_raw_principal(context.recipient)
        mail_info = IPrincipalMailInfo(principal, None)
        if mail_info is None:
            return
        mail_addresses = [
            f'{name} <{address}>'
            for name, address in mail_info.get_addresses()
        ]
        subject = data.get('update_subject') or context.update_subject
        cc = None
        theater = get_parent(context, IMovieTheater)
        templates = IMailTemplates(theater)
        if templates.send_copy_to_sender:
            principal = request.principal
            if principal is not None:
                mail_info = IPrincipalMailInfo(principal, None)
                if mail_info is not None:
                    cc = [
                        f'{name} <{address}>'
                        for name, address in mail_info.get_addresses()
                    ]
        message = HTMLMessage(f'{settings.subject_prefix} {subject}',
                              from_addr=f'{settings.source_name} <{settings.source_address}>',
                              to_addr=mail_addresses,
                              cc=cc,
                              html=data.get('update_message'))
        quotation = context.get_quotation(force_refresh=True)
        if quotation is not None:
            message.attach(Attachment(content_type='application/pdf',
                                      data=str(quotation),
                                      filename=f'{context.quotation_number}.pdf'))
        return message


@viewlet_config(name='booking-archive.warning',
                context=IBookingInfo, layer=IAdminLayer, view=BookingPropertiesEditForm,
                manager=IFormHeaderViewletManager, weight=10)
class BookingInfoArchiveWarning(AlertMessage):
    """Booking archive warning"""

    def __new__(cls, context, request, view, manager):
        if not context.archived:
            return None
        return AlertMessage.__new__(cls)

    status = 'warning'
    _message = _("This booking is archived and can't be modified anymore!")


@adapter_config(required=(IBookingInfo, IAdminLayer, BookingPropertiesEditForm),
                provides=IAJAXFormRenderer)
class BookingPropertiesEditFormRenderer(SimpleEditFormRenderer):
    """Booking properties edit form renderer"""

    parent_interface = IBookingContainer
    table_factory = IBookingContainerTable

    def render(self, changes):
        result = super().render(changes)
        if changes:
            theater = get_parent(self.context, IMovieTheater)
            result.setdefault('callbacks', []).extend([
                get_json_table_row_refresh_callback(theater, self.request,
                                                    IBookingWaitingStatusTable, get_booking_element(self.context)),
                get_json_table_row_refresh_callback(theater, self.request,
                                                    IBookingAcceptedStatusTable, get_booking_element(self.context)),
                {
                    'callback': 'MyAMS.msc.calendar.refresh',
                    'options': {
                        'room_id': ISession(self.context).room
                    }
                }
            ])
        return result


@subscriber(IDataExtractedEvent, form_selector=BookingAddForm)
@subscriber(IDataExtractedEvent, form_selector=BookingPropertiesEditForm)
def handle_accepted_booking_data(event):
    """Handle accepted booking form data"""
    data = event.data
    if (data.get('status') == BOOKING_STATUS.ACCEPTED.value) and not data.get('price'):
        event.form.widgets.errors += (Invalid(_("You must set a price to accept a booking!")),)


@adapter_config(name='session.group',
                required=(IBookingContainer, IAdminLayer, BookingAddForm),
                provides=IGroup)
@adapter_config(name='session.group',
                required=(IBookingInfo, IAdminLayer, BookingPropertiesEditForm),
                provides=IGroup)
class BookingFormSessionGroup(Group):
    """Session info display form"""

    legend = _("Session properties")
    fields = Fields(ISession).select('capacity') + Fields(IBookingContainer).select('free_seats')

    _mode = DISPLAY_MODE
    weight = 10

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        session = get_parent(self.context, ISession)
        capacity = self.widgets.get('capacity')
        if capacity is not None:
            capacity.value = ISession(session).capacity
        free_seats = self.widgets.get('free_seats')
        if free_seats is not None:
            free_seats.value = IBookingContainer(session).free_seats


@adapter_config(name='quotation.group',
                required=(IBookingInfo, IAdminLayer, BookingPropertiesEditForm),
                provides=IGroup)
class BookingEditFormQuotationGroup(Group):
    """Quotation info display form"""

    def __new__(cls, context, request, form):
        if context.status != BOOKING_STATUS.ACCEPTED.value:
            return None
        return Group.__new__(cls)

    legend = _("Booking quotation")
    fields = Fields(IBookingInfo).select('quotation_number', 'quotation_message', 'quotation')

    _mode = DISPLAY_MODE
    weight = 20


@adapter_config(name='update-group',
                required=(IBookingInfo, IAdminLayer, BookingPropertiesEditForm),
                provides=IGroup)
class BookingEditFormUpdateGroup(FormGroupChecker):
    """Booking edit form update group"""

    def __new__(cls, context, request, form):
        if context.status != BOOKING_STATUS.ACCEPTED.value:
            return None
        return FormGroupChecker.__new__(cls)

    legend = _("Booking update")
    fields = Fields(IBookingInfo).select('send_update', 'update_subject', 'update_message')

    checker_fieldname = 'send_update'

    weight = 30

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        send_update = self.widgets.get('send_update')
        if send_update is not None:
            send_update.value = ()
        theater = get_parent(self.context, IMovieTheater)
        templates = IMailTemplates(theater)
        values = get_booking_message_values(self.context, self.request, self)
        # generate formatted messages
        subject = self.widgets.get('update_subject')
        if (subject is not None) and not subject.value:
            template = getattr(templates, 'update_subject')
            if template:
                subject.value = template.format(**values)
        message = self.widgets.get('update_message')
        if (message is not None) and not message.value:
            template = getattr(templates, 'update_template')
            if template:
                message.value = template.format(**values)


@viewlet_config(name='update-group.help',
                context=IBookingInfo, layer=IAdminLayer, view=BookingEditFormUpdateGroup,
                manager=IHelpViewletManager, weight=10)
class BookingEditFormUpdateGroupHelp(AlertMessage):
    """Booking edit form update group help"""

    status = 'info'
    _message = _("Update message can be sent to booking recipient when a booking "
                 "is modified after being validated.")


@adapter_config(name='reminder.group',
                required=(IBookingInfo, IAdminLayer, BookingPropertiesEditForm),
                provides=IGroup)
class BookingEditFormReminderGroup(FormGroupChecker):
    """Booking edit form reminder group"""

    def __new__(cls, context, request, form):
        if context.status != BOOKING_STATUS.ACCEPTED.value:
            return None
        theater = IMovieTheater(context)
        settings = IMovieTheaterSettings(theater)
        if not settings.reminder_delay:
            return None
        reminder_date = (context.session.start_date -
                         datetime.timedelta(days=settings.reminder_delay))
        if reminder_date < tztime(datetime.datetime.now(timezone.utc)):
            return None
        return FormGroupChecker.__new__(cls)

    legend = _("Booking reminder")
    fields = Fields(IBookingInfo).select('send_reminder', 'reminder_subject',
                                         'reminder_message')
    checker_fieldname = 'send_reminder'

    weight = 40

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


@subscriber(IDataExtractedEvent, form_selector=BookingEditFormReminderGroup)
def extract_booking_reminder_data(event):
    """Booking reminder data extract event"""
    data = event.data
    if data.get('send_reminder') and not data.get('reminder_message'):
        event.form.widgets.errors += (Invalid(_("You must set message content to be able to "
                                                "send a reminder message!")),)


@viewlet_config(name='reminder-group.help',
                context=IBookingInfo, layer=IAdminLayer, view=BookingEditFormReminderGroup,
                manager=IHelpViewletManager, weight=10)
class BookingEditFormReminderGroupHelp(AlertMessage):
    """Booking edit form reminder group help"""

    status = 'info'

    @property
    def message(self):
        translate = self.request.localizer.translate
        theater = IMovieTheater(self.context)
        settings = IMovieTheaterSettings(theater)
        return translate(_("Reminder message will be sent to booking recipient {} days before "
                           "session begin date...")).format(settings.reminder_delay)


@view_config(name='reset-quotation.json',
             context=IBookingInfo, request_type=IPyAMSLayer, request_method='POST',
             renderer='json', xhr=True,
             permission=MANAGE_BOOKING_PERMISSION)
def reset_quotation(request):
    """Reset booking quotation"""
    booking = IBookingInfo(request.context)
    booking.get_quotation(force_refresh=True)
    translate = request.localizer.translate
    return {
        'status': "success",
        'message': translate(_("Quotation has been reset!"))
    }


@view_config(name='reset-quotation.pdf',
             context=IBookingInfo, request_type=IPyAMSLayer,
             permission=MANAGE_BOOKING_PERMISSION)
def reset_quotation_pdf(request):
    """Get and store new PDF from booking quotation"""
    booking = IBookingInfo(request.context)
    quotation = booking.get_quotation(force_refresh=True)
    if isinstance(quotation, tuple):
        filename, quotation = quotation
    else:
        filename = 'quotation.pdf'
    return Response(content_type='application/pdf',
                    content_disposition=f'inline; filename={filename}',
                    body=quotation)


@view_config(name='preview-quotation.pdf',
             context=IBookingInfo, request_type=IPyAMSLayer,
             permission=MANAGE_BOOKING_PERMISSION)
def preview_quotation_pdf(request):
    """Preview new PDF from booking quotation"""
    booking = IBookingInfo(request.context)
    params = request.params
    quotation = booking.get_quotation(force_refresh=True,
                                      store=False,
                                      nb_participants=params.get('nb_participants'),
                                      nb_accompanists=params.get('nb_accompanists'),
                                      nb_free_accompanists=params.get('nb_free_accompanists'),
                                      price=params.get('price'),
                                      ratio=params.get('ratio'))
    if isinstance(quotation, tuple):
        filename, quotation = quotation
    else:
        filename = 'quotation.pdf'
    return Response(content_type='application/pdf',
                    content_disposition=f'inline; filename={filename}',
                    body=quotation)
