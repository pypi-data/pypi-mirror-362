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

from elasticsearch_dsl import Q
from hypatia.interfaces import ICatalog
from hypatia.query import Any

from pyams_content.shared.view.interfaces import IWfView
from pyams_content.shared.view.interfaces.query import IViewUserQuery
from pyams_content_es.shared.view.interfaces import IEsViewUserQuery
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import get_utility


#
# Audience query adapters
#

@adapter_config(name='audience',
                required=IWfView,
                provides=IViewUserQuery)
class CatalogAudienceQuery(ContextAdapter):
    """Catalog audience query"""

    @staticmethod
    def get_user_params(request):
        """User params getter"""
        audiences = request.params.getall('audience')
        if not audiences:
            return
        catalog = get_utility(ICatalog)
        yield Any(catalog['catalog_audience'], [
            value
            for audience in audiences
            for value in audience.split(',')
        ])


@adapter_config(name='audience',
                required=IWfView,
                provides=IEsViewUserQuery)
class EsIndexAudienceQuery(ContextAdapter):
    """Elasticsearch index audience query"""

    @staticmethod
    def get_user_params(request):
        """User params getter"""
        audiences = request.params.getall('audience')
        if not audiences:
            return
        yield Q('terms',
                **{'catalog_info.audiences': [
                    value
                    for audience in audiences
                    for value in audience.split(',')
                ]})


#
# Duration query adapters
#

@adapter_config(name='duration',
                required=IWfView,
                provides=IEsViewUserQuery)
class EsCatalogDurationQuery(ContextAdapter):
    """Elasticsearch index duration query"""

    @staticmethod
    def get_user_params(request):
        """User params getter"""
        duration = request.params.get('duration')
        if not duration:
            return
        min, max = duration.split('-')
        settings = {}
        if min:
            settings['gte'] = min
        if max:
            settings['lt'] = max
        yield Q('range',
                **{'catalog_info.duration': settings})
