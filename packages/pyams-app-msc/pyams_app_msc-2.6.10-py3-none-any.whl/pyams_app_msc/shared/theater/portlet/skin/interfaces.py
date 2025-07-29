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

from zope.interface import Interface
from zope.schema import TextLine, Choice, Bool
from pyams_file.interfaces.thumbnail import THUMBNAILERS_VOCABULARY_NAME

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class IMovieTheaterCarouselPortletRendererSettings(Interface):
    """Movie theater carousel portlet renderer settings interface"""

    css_class = TextLine(title=_("CSS class"),
                         description=_("Carousel container CSS class"),
                         required=False,
                         default='carousel')

    cards_css_class = TextLine(title=_("Cards CSS class"),
                               description=_("Inner cards CSS class"),
                               required=False,
                               default='col-md-4 mb-3')

    thumb_selection = Choice(title=_("Images selection"),
                             description=_("Carousel can use responsive selections, but you can "
                                           "also force selection of another specific selection"),
                             vocabulary=THUMBNAILERS_VOCABULARY_NAME,
                             required=False)

    automatic_slide = Bool(title=_("Automatic sliding"),
                           description=_("If 'no', sliding will only be activated manually"),
                           required=True,
                           default=True)

    fade_effect = Bool(title=_("Fade effect"),
                       description=_("If 'yes', slide to slide animation will use a fade effect "
                                     "instead of lateral sliding"),
                       required=True,
                       default=False)

    display_controls = Bool(title=_("Display controls"),
                            description=_("If 'yes', display arrows to navigate between slides"),
                            required=True,
                            default=False)

    enable_touch = Bool(title=_("Enable swiping"),
                        description=_("If 'no', touch events will be disabled on touchscreens"),
                        required=True,
                        default=True)
