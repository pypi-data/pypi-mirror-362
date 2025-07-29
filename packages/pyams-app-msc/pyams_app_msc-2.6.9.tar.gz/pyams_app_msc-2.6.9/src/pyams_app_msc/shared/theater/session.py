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

from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.shared.theater.interfaces.session import IMovieTheaterSession
from pyams_app_msc.feature.planning.session import Session
from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_sequence.reference import get_reference_target
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config


@factory_config(IMovieTheaterSession)
class MovieTheaterSession(Session):
    """Movie theater session persistent class"""

    activity = FieldProperty(IMovieTheaterSession['activity'])


@adapter_config(required=IMovieTheaterSession,
                provides=IWfCatalogEntry)
def session_catalog_entry(context):
    """Movie theater session catalog entry"""
    return get_reference_target(context.activity)
