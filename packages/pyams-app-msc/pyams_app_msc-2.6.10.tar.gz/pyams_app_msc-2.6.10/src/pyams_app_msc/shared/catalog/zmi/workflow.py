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

from pyams_app_msc.shared.catalog.interfaces import ICatalogManager
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.shared.common.zmi.interfaces import IWorkflowDeleteFormTarget
from pyams_content.shared.common.zmi.workflow import SharedContentDeleteForm
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_zmi.interfaces import IAdminLayer


@adapter_config(required=(ICatalogManager, IAdminLayer, SharedContentDeleteForm),
                provides=IWorkflowDeleteFormTarget)
def catalog_entry_workflow_delete_form_target(context, request, form):
    """Catalog entry workflow delete form target"""
    return get_parent(context, IMovieTheater)
