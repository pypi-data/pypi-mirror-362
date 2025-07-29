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

from zope.interface import Interface, implementer
from zope.schema import Bool
from zope.schema.interfaces import IBool

from pyams_app_msc.shared.catalog import IWfCatalogEntry
from pyams_form.datamanager import AttributeField
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import IDataManager

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class ITMDBLookupField(IBool):
    """TMDB lookup field interface"""


@implementer(ITMDBLookupField)
class TMDBLookupField(Bool):
    """TMDB lookup field"""


@adapter_config(required=(IWfCatalogEntry, ITMDBLookupField),
                provides=IDataManager)
class TMDBSearchDataManager(AttributeField):
    """TMDB search field data manager"""

    def can_access(self):
        return True

    def can_write(self):
        return True

    def get(self):
        return False

    def set(self, value):
        pass


class ITMDBSearchInterface(Interface):
    """TMDB search interface"""

    tmdb_lookup = TMDBLookupField(title=_("TMDB lookup"),
                                  description=_("If 'yes', a lookup is done in TMDB database to find "
                                                "movie properties"),
                                  required=True,
                                  default=True)
