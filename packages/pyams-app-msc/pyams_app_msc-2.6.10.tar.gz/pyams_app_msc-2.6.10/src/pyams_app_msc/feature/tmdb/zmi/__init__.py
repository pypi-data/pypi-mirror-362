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

from zope.interface import Interface

from pyams_app_msc.feature.tmdb import ITMDBConfiguration
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormContent, IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.zmi.viewlet.menu import NavigationMenuDivider, NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='tmdb-configuration.divider',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=899,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class TMDBConfigurationMenuDivider(NavigationMenuDivider):
    """TMDB configuration menu divider"""


@viewlet_config(name='tmdb-configuration.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=900,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class TMDBConfigurationMenu(NavigationMenuItem):
    """TMDB configuration menu"""

    label = _("TMDB configuration")
    href = '#tmdb-configuration.html'


@ajax_form_config(name='tmdb-configuration.html',
                  context=ISiteRoot, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class TMDBConfigurationEditForm(AdminEditForm):
    """TMDB configuration edit form"""

    title = _("TMDB service configuration")
    legend = _("TMDB service properties")

    fields = Fields(Interface)


@adapter_config(required=(ISiteRoot, IPyAMSLayer, TMDBConfigurationEditForm),
                provides=IFormContent)
def site_root_tmdb_configuration_edit_form_content(context, request, form):
    """Site root TMDB configuration edit form content getter"""
    return ITMDBConfiguration(context)


@adapter_config(name='tmdb-configuration',
                required=(ISiteRoot, IAdminLayer, TMDBConfigurationEditForm),
                provides=IGroup)
class TMDBConfigurationGroup(FormGroupChecker):
    """TMDB configuration group"""

    fields = Fields(ITMDBConfiguration).omit('proxy_info',
                                             'download_main_poster', 'main_poster_size',
                                             'download_pictures', 'pictures_size',
                                             'download_posters', 'posters_size',
                                             'download_videos', 'restrict_videos_language') + \
        Fields(ITMDBConfiguration).select('proxy_info')


@adapter_config(name='tmdb-main-poster-configuration',
                required=(ISiteRoot, IAdminLayer, TMDBConfigurationGroup),
                provides=IGroup)
class TMDBMainPosterConfiguration(FormGroupChecker):
    """TMDB main poster configuration group"""

    weight = 10

    fields = Fields(ITMDBConfiguration).select('download_main_poster', 'main_poster_size')


@adapter_config(name='tmdb-pictures-configuration',
                required=(ISiteRoot, IAdminLayer, TMDBConfigurationGroup),
                provides=IGroup)
class TMDBPicturesConfiguration(FormGroupChecker):
    """TMDB pictures configuration group"""

    weight = 20

    fields = Fields(ITMDBConfiguration).select('download_pictures', 'pictures_size')


@adapter_config(name='tmdb-posters-configuration',
                required=(ISiteRoot, IAdminLayer, TMDBConfigurationGroup),
                provides=IGroup)
class TMDBPostersConfiguration(FormGroupChecker):
    """TMDB pictures configuration group"""

    weight = 30

    fields = Fields(ITMDBConfiguration).select('download_posters', 'posters_size')


@adapter_config(name='tmdb-videos-configuration',
                required=(ISiteRoot, IAdminLayer, TMDBConfigurationGroup),
                provides=IGroup)
class TMDBVideosConfiguration(FormGroupChecker):
    """TMDB videos configuration group"""

    weight = 40

    fields = Fields(ITMDBConfiguration).select('download_videos', 'restrict_videos_language')
