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

from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.feature.seo import ISEOContentInfo, SEOContentInfo
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


class MovieTheaterSEOContentInfo(SEOContentInfo):
    """Movie theater SEO content info"""

    include_sitemap = True


@adapter_config(required=IMovieTheater,
                provides=ISEOContentInfo)
def movie_theater_seo_content_info(context):
    return MovieTheaterSEOContentInfo()
