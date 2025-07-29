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

from pyramid.httpexceptions import HTTPForbidden, HTTPInternalServerError
from pyramid.view import view_config
from zope.copy import copy
from zope.interface import Interface

from pyams_app_msc.component.gallery.zmi.interfaces import IGalleryIllustrationActionsMenu
from pyams_app_msc.zmi import msc
from pyams_content.component.gallery import IGalleryContainer, IGalleryFile
from pyams_content.component.gallery.zmi import GalleryMediasViewlet, GalleryView
from pyams_content.component.illustration import IIllustration, ILinkIllustration
from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION
from pyams_content.shared.common import IWfSharedContent
from pyams_i18n.interfaces import INegotiator
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.permission import get_edit_permission
from pyams_skin.interfaces.viewlet import IContextActionsViewletManager
from pyams_skin.viewlet.actions import ContextAction, ContextActionsMenu
from pyams_skin.viewlet.menu import MenuItem
from pyams_template.template import override_template
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewletmanager_config(name='set-content-illustration.menu',
                       context=IGalleryFile, layer=IAdminLayer, view=Interface,
                       manager=IContextActionsViewletManager, weight=100,
                       provides=IGalleryIllustrationActionsMenu,
                       permission=MANAGE_CONTENT_PERMISSION)
class GalleryFileIllustrationsGetter(ContextActionsMenu):
    """Gallery file illustrations getter"""

    def __new__(cls, context, request, view, manager):
        gallery = get_parent(context, IGalleryContainer)
        if gallery is not None:
            edit_permission = get_edit_permission(request, context=gallery, view=view)
            if not request.has_permission(edit_permission, context=context):
                return None
        return ContextActionsMenu.__new__(cls)

    # hint = _("Set content illustration")
    css_class = 'btn-sm px-1'
    icon_class = 'fas fa-file-image'

    def update(self):
        super().update()
        msc.need()


@viewlet_config(name='content-illustration.action',
                context=IGalleryFile, layer=IAdminLayer, view=Interface,
                manager=IGalleryIllustrationActionsMenu, weight=10,
                permission=MANAGE_CONTENT_PERMISSION)
class ContentIllustrationSetter(MenuItem):
    """Content illustration setter"""

    label = _("Set content illustration")

    def get_href(self):
        """Icon URL getter"""
        return None

    click_handler = 'MyAMS.msc.catalog.setContentIllustrationFromGallery'


@viewlet_config(name='link-illustration.action',
                context=IGalleryFile, layer=IAdminLayer, view=Interface,
                manager=IGalleryIllustrationActionsMenu, weight=20,
                permission=MANAGE_CONTENT_PERMISSION)
class LinkIllustrationSetter(MenuItem):
    """Link illustration setter"""

    label = _("Set navigation illustration")

    def get_href(self):
        """Icon URL getter"""
        return None

    click_handler = 'MyAMS.msc.catalog.setLinkIllustrationFromGallery'


def set_illustration(request, illustration_interface):
    """Set content illustration"""
    translate = request.localizer.translate
    name = request.params.get('object_name')
    if not name:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("No provided object_name argument!"))
            }
        }
    container = request.context
    if name not in container:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("Given element name doesn't exist!"))
            }
        }
    content = get_parent(container, IWfSharedContent)
    if content is None:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("Can't find illustration target!"))
            }
        }
    permission = get_edit_permission(request, content)
    if permission is None:
        raise HTTPInternalServerError("Missing permission definition!")
    if not request.has_permission(permission, context=content):
        raise HTTPForbidden()
    illustration = illustration_interface(content, None)
    if illustration is None:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("No illustration on content!"))
            }
        }
    media = container[name]
    negotiator = get_utility(INegotiator)
    illustration.title = media.title
    illustration.alt_title = media.alt_title
    illustration.description = media.description
    illustration.author = media.author
    illustration.data = {
        negotiator.server_language: copy(media.data)
    }
    return {
        'status': 'success',
        'message': translate(_("Illustration has been updated successfully."))
    }


@view_config(name='set-content-illustration.json',
             context=IGalleryContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def set_content_illustration(request):
    """Set content illustration from medias gallery file"""
    return set_illustration(request, IIllustration)


@view_config(name='set-link-illustration.json',
             context=IGalleryContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def set_link_illustration(request):
    """Set link illustration from medias gallery file"""
    return set_illustration(request, ILinkIllustration)


override_template(GalleryMediasViewlet,
                  template='templates/gallery-medias.pt',
                  layer=IAdminLayer)

override_template(GalleryView,
                  template='templates/gallery-view.pt',
                  layer=IAdminLayer)
