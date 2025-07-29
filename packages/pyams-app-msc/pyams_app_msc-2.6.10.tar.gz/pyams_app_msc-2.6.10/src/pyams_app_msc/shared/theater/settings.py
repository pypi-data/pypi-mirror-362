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

from datetime import date
from io import BytesIO

from PIL import Image, ImageStat
from persistent import Persistent
from persistent.mapping import PersistentMapping
from zope.container.contained import Contained
from zope.location.interfaces import ISublocations
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.interfaces import ITraversable

from pyams_app_msc.interfaces import MANAGE_THEATER_PERMISSION
from pyams_app_msc.shared.theater import IMovieTheater, IMovieTheaterSettings, MOVIE_THEATER_SETTINGS_KEY
from pyams_file.property import FileProperty
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.request import query_request


@factory_config(IMovieTheaterSettings)
class MovieTheaterSettings(Persistent, Contained):
    """Movie theater settings persistent class"""

    calendar_first_day = FieldProperty(IMovieTheaterSettings['calendar_first_day'])
    calendar_slot_duration = FieldProperty(IMovieTheaterSettings['calendar_slot_duration'])
    default_session_duration = FieldProperty(IMovieTheaterSettings['default_session_duration'])
    session_duration_delta = FieldProperty(IMovieTheaterSettings['session_duration_delta'])

    allow_session_request = FieldProperty(IMovieTheaterSettings['allow_session_request'])
    session_request_mode = FieldProperty(IMovieTheaterSettings['session_request_mode'])

    reminder_delay = FieldProperty(IMovieTheaterSettings['reminder_delay'])

    booking_cancel_mode = FieldProperty(IMovieTheaterSettings['booking_cancel_mode'])
    booking_cancel_max_delay = FieldProperty(IMovieTheaterSettings['booking_cancel_max_delay'])
    booking_cancel_notice_period = FieldProperty(IMovieTheaterSettings['booking_cancel_notice_period'])
    booking_retention_duration = FieldProperty(IMovieTheaterSettings['booking_retention_duration'])

    quotation_number_format = FieldProperty(IMovieTheaterSettings['quotation_number_format'])
    quotation_email = FieldProperty(IMovieTheaterSettings['quotation_email'])
    quotation_logo = FileProperty(IMovieTheaterSettings['quotation_logo'])
    quotation_color = FieldProperty(IMovieTheaterSettings['quotation_color'])
    currency = FieldProperty(IMovieTheaterSettings['currency'])
    vat_rate = FieldProperty(IMovieTheaterSettings['vat_rate'])

    _year_quotations = None
    _month_quotations = None

    def get_logo_color(self):
        """Extract median color from logo"""
        logo = self.quotation_logo
        if not logo:
            return None
        image = Image.open(BytesIO(logo.data))
        median = ImageStat.Stat(image).median
        return "{:02x}{:02x}{:02x}".format(*median)

    def get_quotation_number(self):
        """Get new quotation number"""
        request = query_request()
        principal = request.principal
        initials = ''.join(map(lambda x: x[0].upper(), principal.title.split()))
        now = date.today()
        year_quotations = self._year_quotations
        if year_quotations is None:
            year_quotations = self._year_quotations = PersistentMapping()
        year_inc = year_quotations.get(now.year, 0) + 1
        year_quotations[now.year] = year_inc
        month_quotations = self._month_quotations
        if month_quotations is None:
            month_quotations = self._month_quotations = PersistentMapping()
        month_inc = month_quotations.get(now.year, {}).get(now.month, 0) + 1
        month_quotations.setdefault(now.year, PersistentMapping())[now.month] = month_inc
        args = {
            'yyyy': now.year,
            'yy': int(str(now.year)[2:]),
            'mm': now.month,
            'dd': now.day,
            'yinc': year_inc,
            'minc': month_inc,
            'operator': initials
        }
        return self.quotation_number_format.format(**args)

    def get_quotation_color(self):
        return f'#{self.quotation_color or self.get_logo_color() or "D5D5D5"}'


@adapter_config(required=IMovieTheaterSettings,
                provides=IViewContextPermissionChecker)
class MovieTheaterSettingsPermissionChecker(ContextAdapter):
    """Movie theater settings permission checker"""

    edit_permission = MANAGE_THEATER_PERMISSION


@adapter_config(required=IMovieTheater,
                provides=IMovieTheaterSettings)
def movie_theater_settings(context):
    """Movie theater settings adapter"""
    return get_annotation_adapter(context, MOVIE_THEATER_SETTINGS_KEY, IMovieTheaterSettings,
                                  name='++settings++')


@adapter_config(name='settings',
                required=IMovieTheater,
                provides=ITraversable)
class MovieTheaterSettingsTraverser(ContextAdapter):
    """Movie theater settings traverser"""

    def traverse(self, name, furtherpath=None):
        return IMovieTheaterSettings(self.context, None)


@adapter_config(name='settings',
                required=IMovieTheater,
                provides=ISublocations)
class MovieTheaterSettingsSublocations(ContextAdapter):
    """Movie theater settings sub-locations adapter"""

    def sublocations(self):
        settings = IMovieTheaterSettings(self.context, None)
        if settings is not None:
            yield settings
