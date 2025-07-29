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

from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.shared.catalog.interfaces import IAudienceFilter, IDurationFilter
from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.interfaces.audience import ICinemaAudienceContainer
from pyams_content.feature.filter import Filter
from pyams_content.feature.filter.interfaces import IAggregatedPortletRendererSettings, IFilterAggregate, \
    IFilterProcessor
from pyams_content_es.filter import get_sorting_params
from pyams_content_es.filter.processor import EsBaseFilterProcessor
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry
from pyams_utils.request import query_request
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


#
# Activity audience filter
#

@factory_config(IAudienceFilter)
class AudienceFilter(Filter):
    """Audience filter"""

    filter_type = 'audience'


@adapter_config(required=IAudienceFilter,
                provides=IFilterAggregate)
def audience_filter_aggregate(context):
    """Audience filter aggregate"""
    registry = get_pyramid_registry()
    return {
        'name': context.filter_name,
        'type': 'terms',
        'params': {
            'field': registry.settings.get('pyams_content_es.filter.audience.field_name',
                                           'catalog_info.audiences'),
            'size': 100,
            'order': get_sorting_params(context.sorting_mode)
        }
    }


@adapter_config(required=(IAudienceFilter, IPyAMSLayer, IAggregatedPortletRendererSettings),
                provides=IFilterProcessor)
class AudienceFilterProcessor(EsBaseFilterProcessor):
    """Audience filter processor"""

    def convert_aggregations(self, aggregations):
        result = []
        request = query_request()
        theater = get_parent(request.context, IMovieTheater)
        if theater is None:
            return result
        audiences = ICinemaAudienceContainer(theater, {})
        for item in aggregations:
            audience = audiences.get(item['key'])
            if audience is not None:
                result.append({
                    'key': audience.__name__,
                    'label': audience.name,
                    'doc_count': item['doc_count']
                })
        return result


#
# Activity duration filter
#

DURATION_FILTER_LABEL = {
    '-30': _("< 30 min."),
    '30-60': _("30 to 60 min."),
    '60-90': _("60 to 90 min."),
    '90-': _("> 90 min.")
}


@factory_config(IDurationFilter)
class DurationFilter(Filter):
    """Duration filter"""

    filter_type = 'duration'
    sorting_mode = FieldProperty(IDurationFilter['sorting_mode'])


@adapter_config(required=IDurationFilter,
                provides=IFilterAggregate)
def duration_filter_aggregate(context):
    """Duration filter aggregate"""
    registry = get_pyramid_registry()
    return {
        'name': context.filter_name,
        'type': 'range',
        'params': {
            'field': registry.settings.get('pyams_content_es.filter.duration.field_name',
                                           'catalog_info.duration'),
            'keyed': True,
            'ranges': [{
                'key': '-30',
                'to': 30
            }, {
                'key': '30-60',
                'from': 30,
                'to': 60
            }, {
                'key': '60-90',
                'from': 60,
                'to': 90
            }, {
                'key': '90-',
                'from': 90
            }]
        }
    }


@adapter_config(required=(IDurationFilter, IPyAMSLayer, IAggregatedPortletRendererSettings),
                provides=IFilterProcessor)
class DurationFilterProcessor(EsBaseFilterProcessor):
    """Duration filter processor"""

    def convert_aggregations(self, aggregations):
        result = []
        for key in aggregations:
            result.append({
                'key': key,
                'label': self.request.localizer.translate(DURATION_FILTER_LABEL[key]),
                'doc_count': aggregations.buckets[key].doc_count
            })
        return result
