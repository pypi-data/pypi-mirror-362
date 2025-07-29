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

import math
import os.path
from datetime import datetime, timezone
from io import BytesIO

from PIL import Image
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Flowable, Frame, PageTemplate, Paragraph, Table, TableStyle

from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.feature.profile import IUserProfile
from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_app_msc.shared.theater import IMovieTheater, IMovieTheaterSettings
from pyams_app_msc.shared.theater.interfaces.price import ICinemaPriceContainer
from pyams_i18n.interfaces import II18n
from pyams_security.utility import get_principal
from pyams_utils.date import SH_DATE_FORMAT, format_date, format_datetime
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.request import query_request
from pyams_utils.text import get_text_parts

__docformat__ = 'restructuredtext'

from pyams_app_msc import _
from pyams_utils.timezone import tztime

dirname = os.path.dirname(__file__)
registerFont(TTFont('Roboto-Light', f"{dirname}/fonts/Roboto-Light.ttf"))
registerFont(TTFont('Roboto-Medium', f"{dirname}/fonts/Roboto-Medium.ttf"))
registerFont(TTFont('Roboto-Bold', f"{dirname}/fonts/Roboto-Bold.ttf"))


STYLESHEET = getSampleStyleSheet()
STYLESHEET.add(ParagraphStyle(name='header',
                              fontName='Roboto-Light',
                              fontSize=11,
                              leading=15,
                              alignment=TA_RIGHT,
                              alias='header'))
STYLESHEET.add(ParagraphStyle(name='banner',
                              fontName='Roboto-Bold',
                              fontSize=15,
                              leading=24,
                              alignment=TA_CENTER,
                              alias='banner'))
STYLESHEET.add(ParagraphStyle(name='frame',
                              fontName='Roboto-Medium',
                              fontSize=12,
                              leading=16,
                              alignment=TA_CENTER,
                              alias='frame'))
STYLESHEET.add(ParagraphStyle(name='p',
                              fontName='Roboto-Light',
                              fontSize=10,
                              leading=15,
                              alias='p'))
STYLESHEET.add(ParagraphStyle(name='small',
                              fontName='Roboto-Light',
                              fontSize=8,
                              leading=9,
                              alias='small'))
STYLESHEET.add(ParagraphStyle(name='tiny',
                              fontName='Roboto-Light',
                              fontSize=7,
                              leading=8,
                              alias='tiny'))


class Quotation:
    """Quotation document"""

    class Template(PageTemplate):
        """Base quotation template"""

        def __init__(self, parent):
            self.parent = parent
            content = Frame(2.*cm,
                            2.*cm,
                            parent.document.pagesize[0] - 4.*cm,
                            parent.document.pagesize[1] - 4.*cm)
            super().__init__("Document", [content])

        def beforeDrawPage(self, canvas, document):
            canvas.saveState()
            try:
                pass
            finally:
                canvas.restoreState()

    class Header(Flowable):
        """Custom flowable header"""

        def __init__(self, parent, request):
            super().__init__()
            self.parent = parent
            self.request = request

        def draw(self):
            self.canv.saveState()
            try:
                theater = self.parent.theater
                settings = IMovieTheaterSettings(theater)
                logo = settings.quotation_logo
                if logo:
                    image = Image.open(BytesIO(logo.data))
                    self.canv.drawImage(ImageReader(image), 0, -4*cm, width=8*cm, height=5*cm,
                                        preserveAspectRatio=True)
                header = [II18n(theater).query_attribute('title', request=self.request)]
                address = theater.address
                if address:
                    if address.street:
                        header.append(address.street)
                    if address.locality:
                        header.append(address.locality)
                    header.append(f"{address.postal_code or ''} {address.city or ''}")
                header.append('')
                if theater.phone_number:
                    header.append(theater.phone_number)
                if theater.web_address:
                    header.append(theater.web_address)
                if theater.contact_email:
                    header.append(settings.quotation_email or theater.contact_email)
                paragraph = Paragraph(f"{'<br />'.join(header)}", STYLESHEET['header'])
                paragraph.wrap(9*cm, 5*cm)
                paragraph.drawOn(self.canv, 8*cm, -4*cm)
            finally:
                self.canv.restoreState()

    class SubHeader(Flowable):
        """Custom sub-header"""

        def __init__(self, parent, request):
            super().__init__()
            self.parent = parent
            self.request = request

        def draw(self):
            self.canv.saveState()
            try:
                settings = IMovieTheaterSettings(self.parent.theater)
                self.canv.setFillColor(settings.get_quotation_color())
                self.canv.setStrokeColor(settings.get_quotation_color())
                self.canv.rect(0, -6*cm, 17*cm, 1*cm, stroke=1, fill=1)
                paragraph = Paragraph(self.parent.translate(_("QUOTATION")), STYLESHEET['banner'])
                paragraph.wrap(17*cm, 1*cm)
                paragraph.drawOn(self.canv, 0, -6*cm)
            finally:
                self.canv.restoreState()

    class RecipientInfo(Flowable):
        """Recipient info"""

        def __init__(self, parent, request):
            super().__init__()
            self.parent = parent
            self.request = request

        def draw(self):
            self.canv.saveState()
            try:
                session = self.parent.session
                translate = self.parent.translate
                now = tztime(datetime.now(timezone.utc))
                target = session.get_target()
                quotation_object = session.label
                if IWfCatalogEntry.providedBy(target):
                    data_type = target.get_data_type()
                    if data_type is not None:
                        quotation_object = II18n(data_type).query_attribute('label', request=self.request)
                formatter = '{} <font name="Roboto-Medium">{}</font>'
                header = [
                    formatter.format(translate(_('#Quotation:')),
                                     self.parent.booking.quotation_number),
                    formatter.format(translate(_("Date:")),
                                     format_date(now, SH_DATE_FORMAT)),
                    formatter.format(translate(_("Object:")),
                                     quotation_object or MISSING_INFO)
                ]
                paragraph = Paragraph(f"{'<br />'.join(header)}", STYLESHEET['p'])
                paragraph.wrap(8*cm, 4*cm)
                paragraph.drawOn(self.canv, 0*cm, -8*cm)
                recipient = get_principal(None, self.parent.booking.recipient)
                recipient_info = IUserProfile(recipient)
                frame = [
                    recipient_info.establishment
                ]
                recipient_address = recipient_info.establishment_address
                if recipient_address:
                    frame.extend([
                        recipient_address.street,
                        recipient_address.locality,
                        f'{recipient_address.postal_code}  {recipient_address.city}'
                    ])
                paragraph = Paragraph(f"{'<br />'.join(filter(bool, frame))}", STYLESHEET['frame'])
                paragraph.wrap(8*cm, 4*cm)
                height = paragraph.height
                paragraph.drawOn(self.canv, 8.5*cm, -7.85*cm - height/2)
                settings = IMovieTheaterSettings(self.parent.theater)
                self.canv.setStrokeColor(settings.get_quotation_color())
                self.canv.rect(8*cm, -9.5*cm, 9*cm, 3.25*cm, stroke=1, fill=0)
            finally:
                self.canv.restoreState()

    class QuotationDetail(Flowable):
        """Quotations details"""

        def __init__(self, parent, request):
            super().__init__()
            self.parent = parent
            self.request = request

        def draw(self):
            self.canv.saveState()
            try:
                booking = self.parent.booking
                session = self.parent.session
                settings = IMovieTheaterSettings(self.parent.theater)
                color = settings.get_quotation_color()
                translate = self.parent.translate
                style = TableStyle([
                    ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
                    ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                    ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                    ('ALIGN', (-3, -3), (-2, -1), 'RIGHT'),
                    ('BOX', (0, 0), (-1, 0), 0.5, color),
                    ('BOX', (0, 0), (-1, -4), 0.5, color),
                    ('BOX', (-3, -3), (-1, -1), 0.5, color),
                    ('LINEBEFORE', (0, 0), (-1, -4), 0.5, color),
                    ('SPAN', (-3, -3), (-2, -3)),
                    ('SPAN', (-3, -2), (-2, -2)),
                    ('SPAN', (-3, -1), (-2, -1))
                ])
                preview_args = self.parent.kwargs
                price_id = preview_args.get('price')
                if price_id:
                    price = ICinemaPriceContainer(self.parent.theater).get(price_id)
                else:
                    price = booking.get_price()
                nb_participants = preview_args.get('nb_participants')
                if nb_participants is None:
                    nb_participants = booking.nb_participants
                else:
                    nb_participants = int(nb_participants or 0)
                nb_accompanists = preview_args.get('nb_accompanists')
                if nb_accompanists is None:
                    nb_accompanists = booking.nb_accompanists
                else:
                    nb_accompanists = int(nb_accompanists or 0)
                nb_free_accompanists = preview_args.get('nb_free_accompanists')
                if nb_free_accompanists is None:
                    nb_free_accompanists = booking.nb_free_accompanists
                else:
                    nb_free_accompanists = int(nb_free_accompanists or 0)
                nb_paid_accompanists = nb_accompanists - nb_free_accompanists
                if price is not None:
                    if price.accompanying_price == 0.:
                        free_accompanists = nb_accompanists
                        paid_accompanists = 0
                    else:
                        ratio = preview_args.get('ratio')
                        if ratio is None:
                            ratio = booking.accompanying_ratio
                        else:
                            ratio = float(ratio or 0)
                        if ratio:
                            max_accompanists = math.ceil(nb_participants / ratio)
                            free_accompanists = min(max_accompanists, nb_paid_accompanists) + nb_free_accompanists
                            paid_accompanists = nb_accompanists - free_accompanists
                        else:
                            free_accompanists = nb_free_accompanists
                            paid_accompanists = nb_paid_accompanists
                    participants_amount = price.participant_price * nb_participants
                    accompanying_amount = price.accompanying_price * paid_accompanists
                else:
                    free_accompanists = nb_accompanists
                    paid_accompanists = 0
                    participants_amount = 0.
                    accompanying_amount = 0.
                total_amount = round(participants_amount + accompanying_amount, 2)
                base_amount = round(total_amount / (1. + settings.vat_rate/100), 2)
                vat_amount = total_amount - base_amount
                data = [
                    (translate(_("Activity")),
                     translate(_("Units")),
                     translate(_("Unit price")),
                     translate(_("Total"))),
                    (f'{session.get_label()}, {format_datetime(session.start_date)}',
                     '',
                     '',
                     ''),
                    (translate(_("   - Entries ({})")).format(
                        translate(_("1 group")) if booking.nb_groups == 1
                        else translate(_("{} groups")).format(booking.nb_groups)),
                     booking.nb_participants,
                     f'{price.participant_price:.2f} {settings.currency}',
                     f'{participants_amount:.2f} {settings.currency}')
                ]
                if free_accompanists:
                    data.append(
                        (translate(_("   - Free accompanists")),
                         free_accompanists or '--',
                         f'{0:.2f} {settings.currency}',
                         f'{0:.2f} {settings.currency}')
                    )
                if paid_accompanists:
                    data.append(
                        (translate(_("   - Paying accompanists")),
                         paid_accompanists or '--',
                         f'{price.accompanying_price:.2f} {settings.currency}',
                         f'{accompanying_amount:.2f} {settings.currency}')
                    )
                message = booking.quotation_message
                if message:
                    data.append(('', '', '', ''))
                    data.append((Paragraph(message.replace('\r', '')), '', '', ''))
                data.extend([
                    ('',
                     translate(_("Base amount")),
                     '',
                     f'{base_amount:.2f} {settings.currency}'),
                    ('',
                     '{} {:.2f}%'.format(translate(_("VAT")), settings.vat_rate),
                     '',
                     f'{vat_amount:.2f} {settings.currency}'),
                    ('',
                     translate(_("Total amount")),
                     '',
                     f'{total_amount:.2f} {settings.currency}')
                ])
                table = Table(data,
                              colWidths=(10*cm, 2*cm, 2*cm, 3*cm),
                              style=style)
                table.wrap(17*cm, 20*cm)
                height = sum(table._rowHeights)
                table.drawOn(self.canv, 0*cm, -10*cm - height)
            finally:
                self.canv.restoreState()

    class BankInfo(Flowable):
        """Bank info"""

        def __init__(self, parent, request):
            super().__init__()
            self.parent = parent
            self.request = request

        def draw(self):
            self.canv.saveState()
            try:
                settings = self.parent.theater.banking_account
                translate = self.request.localizer.translate
                style = TableStyle([
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 0.5, black),
                    ('SPAN', (0, 0), (-1, 0)),
                    ('SPAN', (0, -1), (1, -1)),
                    ('SPAN', (2, -1), (-1, -1))
                ])
                data = [
                    (translate(_("Bank location: {}")).format(settings.company_name),),
                    (translate(_("Bank code")),
                     translate(_("Counter code")),
                     translate(_("Account number")),
                     translate(_("Key"))),
                    (settings.bank_code,
                     settings.counter_code,
                     settings.account_number,
                     settings.account_key),
                    (translate(_("IBAN: {}")).format(
                        get_text_parts(settings.iban_number, 0, 4, 8, 12, 16, 20, 24, -1)),
                     None,
                     translate(_("BIC: {}")).format(settings.bic_code),
                     None)
                ]
                table = Table(data,
                              colWidths=(5*cm, 5*cm, 5*cm, 2*cm),
                              style=style)
                table.wrap(17*cm, 4*cm)
                table.drawOn(self.canv, 0*cm, -25*cm)
            finally:
                self.canv.restoreState()

    class GeneralTheaterInfo(Flowable):
        """General theater info"""

        def __init__(self, parent, request):
            super().__init__()
            self.parent = parent
            self.request = request

        def draw(self):
            self.canv.saveState()
            try:
                settings = IMovieTheaterSettings(self.parent.theater)
                admin_info = self.parent.theater.admin_info
                translate = self.request.localizer.translate
                style = TableStyle([
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('LINEABOVE', (0, 0), (-1, 0), 1, settings.get_quotation_color())
                ])
                data = [
                    (translate(_("APE: {}")).format(admin_info.ape_code),
                     translate(_("SIRET: {}")).format(
                         get_text_parts(admin_info.siret_code, 0, 3, 6, 9, -1)),
                     translate(_("VAT: {}")).format(
                         get_text_parts(admin_info.vat_number, 0, 4, 7, 10, -1)))
                ]
                table = Table(data,
                              colWidths=(5*cm, 7*cm, 5*cm),
                              style=style)
                table.wrap(17*cm, 1*cm)
                table.drawOn(self.canv, 0*cm, -27*cm)
            finally:
                self.canv.restoreState()

    def __init__(self, booking, quotation_number, **kwargs):
        self.built = False
        self.booking = booking
        self.session = ISession(booking)
        self.theater = IMovieTheater(booking)
        self.kwargs = kwargs
        self.report = BytesIO()
        self.elements = []
        request = query_request()
        if request is not None:
            translate = request.localizer.translate
        else:
            translate = str
        self.translate = translate
        self.document = BaseDocTemplate(self.report,
                                        title=translate(_("Quotation: {}")).format(quotation_number),
                                        author=II18n(self.theater).query_attribute('title', request=request),
                                        subject=self.session.label,
                                        creator=request.principal.title,
                                        pagesize=A4,
                                        leftMargin=2.*cm,
                                        rightMargin=2.*cm,
                                        topMargin=2.*cm,
                                        bottomMargin=2.*cm,
                                        pageCompression=1)
        self.document.addPageTemplates(Quotation.Template(self))
        self.append(Quotation.Header(self, request))
        self.append(Quotation.SubHeader(self, request))
        self.append(Quotation.RecipientInfo(self, request))
        self.append(Quotation.QuotationDetail(self, request))
        self.append(Quotation.BankInfo(self, request))
        self.append(Quotation.GeneralTheaterInfo(self, request))
        self.build()

    def __bytes__(self):
        if self.built:
            return self.report.getvalue()
        return None

    def append(self, flowable: Flowable):
        self.elements.append(flowable)

    def build(self):
        self.document.build(self.elements)
        self.built = True
