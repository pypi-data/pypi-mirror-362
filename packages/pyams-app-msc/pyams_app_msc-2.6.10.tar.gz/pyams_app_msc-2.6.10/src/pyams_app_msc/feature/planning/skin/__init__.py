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

from pyramid.renderers import render
from zope.interface import Interface
from zope.schema import Bool, Choice, Datetime, Int, Text, TextLine

from pyams_app_msc.feature.messaging import IMessagingSettings
from pyams_app_msc.feature.profile import IUserProfile
from pyams_app_msc.interfaces import CREATE_BOOKING_PERMISSION, MSC_MANAGER_ROLE, MSC_OPERATOR_ROLE
from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.audience import AUDIENCES_VOCABULARY, ICinemaAudienceContainer
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.form import AddForm
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_mail.interfaces import IPrincipalMailInfo
from pyams_mail.message import HTMLMessage
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_security.interfaces import IProtectedObject, ISecurityManager
from pyams_security.interfaces.notification import INotificationSettings
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.schema.button import SubmitButton
from pyams_skin.viewlet.help import AlertMessage
from pyams_template.template import template_config
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.dict import DotDict
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import canonical_url
from pyams_viewlet.viewlet import viewlet_config

try:
    from pyams_chat.interfaces import IChatMessage, IChatMessageHandler
    from pyams_chat.message import ChatMessage
except ImportError:
    ChatMessage = None

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class ISessionRequestFormInfo(Interface):
    """Session request form interface"""

    movie_title = TextLine(title=_("Movie title"),
                           description=_("Title of the movie or activity for which you request a new session"),
                           required=True)

    start_date_1 = Datetime(title=_("Start date of the session"),
                            description=_("First proposed date for this session"),
                            required=True)

    start_date_2 = Datetime(title="",
                            description=_("Second proposed date for this session"),
                            required=False)

    start_date_3 = Datetime(title="",
                            description=_("Third proposed date for this session"),
                            required=False)

    audience = Choice(title=_("Target audience"),
                      description=_("Target audience selected for this session"),
                      vocabulary=AUDIENCES_VOCABULARY,
                      required=True)

    nb_participants = Int(title=_("Participants"),
                          description=_("Number of participants seats reserved for this session"),
                          required=True,
                          min=0)

    nb_accompanists = Int(title=_("Accompanists"),
                          description=_("Total number of accompanists seats reserved for this session"),
                          required=True,
                          min=0)

    nb_groups = Int(title=_("Groups count"),
                    description=_("Number of groups or classrooms attending this session"),
                    required=True,
                    min=1,
                    default=1)

    cultural_pass = Bool(title=_("Cultural pass"),
                         description=_("Check this option if payment is done using cultural pass"),
                         required=True,
                         default=False)

    comments = Text(title=_("Comments"),
                    description=_("You can add optional comments to your session request"),
                    required=False)

    send_confirmation = Bool(title=_("Get confirmation message?"),
                             description=_("If 'yes', a confirmation message will be sent to you to "
                                           "acknowledge the session request"),
                             required=True,
                             default=True)


class ISessionRequestFormButtons(Interface):
    """Session request form buttons interface"""

    add = SubmitButton(name='add',
                       title=_("Ask for new session"))


@ajax_form_config(name='session-request.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=CREATE_BOOKING_PERMISSION)
class SessionRequestForm(AddForm, PortalContextIndexPage):
    """Session request form"""

    legend = _("Request new session")

    fields = Fields(ISessionRequestFormInfo)
    buttons = Buttons(ISessionRequestFormButtons)

    _edit_permission = CREATE_BOOKING_PERMISSION

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        audience = self.widgets.get('audience')
        if audience is not None:
            audience.prompt = True
            audience.prompt_message = self.request.localizer.translate(_("Please select target audience..."))
            selected_audience = self.request.params.get('audience')
            if selected_audience:
                audience.value = selected_audience

    @handler(buttons['add'])
    def handle_add(self, action):
        super().handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        request = self.request
        settings = IMessagingSettings(request.root, None)
        if settings is None:
            return None
        mailer = settings.get_mailer()
        if mailer is None:
            return None
        translate = request.localizer.translate
        # get source email
        sm = get_utility(ISecurityManager)
        source_email = None
        raw_principal = sm.get_raw_principal(request.principal.id)
        mail_info = IPrincipalMailInfo(raw_principal, None)
        if mail_info is not None:
            source_email = [
                f'{name} <{address}>'
                for name, address in mail_info.get_addresses()
            ]
            if len(source_email) > 0:
                source_email = source_email[0]
        # create inner message
        message = None
        theater = get_parent(self.context, IMovieTheater)
        contact_email = None
        audience = ICinemaAudienceContainer(theater).get(data.get('audience'))
        if audience is not None:
            contact = audience.contact
            if contact is not None:
                contact_email = f'{contact.name} <{contact.email_address}>' if contact.email_address else None
        if not contact_email:
            contact_email = theater.contact_email
        if contact_email:
            notifications_settings = INotificationSettings(sm)
            principal = sm.get_principal(request.principal.id)
            message_body = render('templates/session-request-message.pt',
                                  request=request,
                                  value={
                                      'settings': notifications_settings,
                                      'data': DotDict(data),
                                      'audience': audience,
                                      'sender': principal,
                                      'profile': IUserProfile(principal)
                                  })
            message = HTMLMessage(subject=translate(_("{} New session request"))
                                      .format(settings.subject_prefix),
                                  from_addr=f'{settings.source_name} <{settings.source_address}>',
                                  to_addr=contact_email,
                                  reply_to=source_email,
                                  html=message_body)
            mailer.send(message)
            # create acknowledge message
            if data.get('send_confirmation') and source_email:
                ack_message_body = render('templates/session-request-ack.pt',
                                          request=request,
                                          value={
                                              'settings': notifications_settings,
                                              'theater': theater,
                                              'data': data,
                                              'audience': audience
                                          })
                ack_message = HTMLMessage(subject=translate(_("{} Your session request"))
                                              .format(settings.subject_prefix),
                                          from_addr=f'{settings.source_name} <{settings.source_address}>',
                                          to_addr=source_email,
                                          html=ack_message_body)
                mailer.send(ack_message)
        self.finished_state.update({
            'movie_title': data.get('movie_title')
        })
        return message


@viewlet_config(name='session-request.help',
                context=IMovieTheater, layer=IPyAMSLayer, view=SessionRequestForm,
                manager=IFormHeaderViewletManager, weight=20)
class SessionRequestInfo(AlertMessage):
    """Session request info"""

    status = 'info'
    _message = _("If the proposed activities do not meet your needs, you can request an additional session.\n"
                 "We'll get back to you as soon as possible, depending on the films in the cinema's catalog "
                 "and available slots.")


@ajax_form_config(name='session-request.html',
                  context=IWfCatalogEntry, layer=IPyAMSLayer,
                  permission=CREATE_BOOKING_PERMISSION)
class CatalogEntrySessionRequestForm(SessionRequestForm):
    """Catalog entry session request form"""

    def get_ajax_handler(self):
        return canonical_url(self.context, self.request, self.ajax_form_handler)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        movie_title = self.widgets.get('movie_title')
        if movie_title is not None:
            movie_title.value = II18n(self.context).query_attribute('title', request=self.request)


@viewlet_config(name='session-request.activity.link',
                context=IWfCatalogEntry, layer=IPyAMSLayer, view=CatalogEntrySessionRequestForm,
                manager=IFormHeaderViewletManager, weight=10)
class CatalogEntrySessionRequestActivityLink(AlertMessage):
    """Catalog entry session request activity link"""

    status = 'info'
    message_renderer = 'markdown'

    @property
    def message(self):
        link_url = canonical_url(self.context, self.request,
                                 query={'audience': self.request.params.get('audience')})
        link_text = self.request.localizer.translate(_("Display movie info"))
        return f'''<a href="{link_url}" target="_blank">{link_text}</a>''' + \
               ''' <i class="fa fas fa-external-link"></i>'''


@viewlet_config(name='session-request.help',
                context=IWfCatalogEntry, layer=IPyAMSLayer, view=CatalogEntrySessionRequestForm,
                manager=IFormHeaderViewletManager, weight=20)
class CatalogEntrySessionRequestInfo(SessionRequestInfo):
    """Catalog entry session request info"""

    _message = _("If the proposed sessions do not meet your needs, you can request an additional session.\n"
                 "We'll get back to you as soon as possible, depending on the cinema's available slots.")


@adapter_config(required=(IMovieTheater, IPyAMSLayer, SessionRequestForm),
                provides=IAJAXFormRenderer)
@adapter_config(required=(IWfCatalogEntry, IPyAMSLayer, SessionRequestForm),
                provides=IAJAXFormRenderer)
class SessionRequestFormRenderer(ContextRequestViewAdapter):
    """Session request form renderer"""

    def render(self, changes):
        if changes is None:
            return
        if ChatMessage is not None:
            request = self.request
            translate = request.localizer.translate
            movie_title = self.view.finished_state.get('movie_title')
            message = ChatMessage(request=request,
                                  context=changes,
                                  action='notify',
                                  category='session.request',
                                  source=request.principal,
                                  title=translate(_("New session request")),
                                  message=translate(_("{principal}: {title}")).format(
                                      principal=request.principal.title,
                                      title=movie_title))
            message.send()
        return {
            'status': 'redirect',
            'location': canonical_url(self.context, self.request, 'session-request-ok.html')
        }


@pagelet_config(name='session-request-ok.html',
                layer=IPyAMSLayer)
@template_config(template='templates/session-request-ok.pt',
                 layer=IPyAMSLayer)
class SessionRequestOKView(PortalContextIndexPage):
    """Session request acknowledge view"""


if ChatMessage is not None:

    @adapter_config(name='session.request',
                    required=IChatMessage,
                    provides=IChatMessageHandler)
    class SessionRequestChatMessageHandler(ContextAdapter):
        """Session request chat message handler"""

        def get_target(self):
            """Chat message targets getter"""
            theater = get_parent(self.context.request.context, IMovieTheater)
            if theater is None:
                return None
            protection = IProtectedObject(theater)
            principals = set()
            for role_id in (MSC_MANAGER_ROLE, MSC_OPERATOR_ROLE):
                for principal_id in protection.get_principals(role_id):
                    principals.add(principal_id)
            return {
                'principals': tuple(principals)
            }
