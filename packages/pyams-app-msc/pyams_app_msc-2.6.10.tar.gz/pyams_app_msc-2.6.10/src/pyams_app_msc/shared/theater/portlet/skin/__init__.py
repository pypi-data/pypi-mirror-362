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

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.shared.theater.portlet import IMovieTheaterCarouselPortletSettings
from pyams_app_msc.shared.theater.portlet.skin.interfaces import IMovieTheaterCarouselPortletRendererSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_portal.skin import PortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@factory_config(provided=IMovieTheaterCarouselPortletRendererSettings)
class MovieTheaterCarouselPortletRendererSettings(Persistent, Contained):
    """Movie theater carousel portlet renderer settings"""

    css_class = FieldProperty(IMovieTheaterCarouselPortletRendererSettings['css_class'])
    cards_css_class = FieldProperty(IMovieTheaterCarouselPortletRendererSettings['cards_css_class'])
    thumb_selection = FieldProperty(IMovieTheaterCarouselPortletRendererSettings['thumb_selection'])
    automatic_slide = FieldProperty(IMovieTheaterCarouselPortletRendererSettings['automatic_slide'])
    fade_effect = FieldProperty(IMovieTheaterCarouselPortletRendererSettings['fade_effect'])
    display_controls = FieldProperty(IMovieTheaterCarouselPortletRendererSettings['display_controls'])
    enable_touch = FieldProperty(IMovieTheaterCarouselPortletRendererSettings['enable_touch'])


@adapter_config(required=(IPortalContext, IPyAMSLayer, Interface, IMovieTheaterCarouselPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/carousel-default.pt', layer=IPyAMSLayer)
class MovieTheaterCarouselPortletRenderer(PortletRenderer):
    """Movie theater carousel portlet renderer"""

    label = _("MSC: Movie theaters carousel (default)")
    weight = 1

    settings_interface = IMovieTheaterCarouselPortletRendererSettings

    @staticmethod
    def get_location(theater):
        address = theater.address
        return address.city if address is not None else None
