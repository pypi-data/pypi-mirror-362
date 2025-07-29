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

from pyams_content.feature.filter import IFilter
from pyams_content.feature.filter.interfaces import IAggregatedPortletRendererSettings, IFilterProcessor, \
    IFilterProcessorAggregationsHandler
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import adapter_config

__docformat__ = 'restructuredtext'


@adapter_config(required=(IFilter, IPyAMSLayer, IAggregatedPortletRendererSettings),
                provides=IFilterProcessor)
class BaseFilterProcessor:
    """Base filter processor"""

    def __init__(self, filter, request, renderer_settings):
        self.filter = filter
        self.request = request
        self.renderer_settings = renderer_settings

    def process(self, aggregations, filter_type=None):
        filter = self.filter
        request = self.request
        aggr = None
        filter_name = filter.filter_name
        if filter_name in aggregations:
            aggr = self.get_aggregations(aggregations[filter_name])
        if not aggr:
            return None
        handler = request.registry.queryMultiAdapter((filter, request, self.renderer_settings),
                                                     IFilterProcessorAggregationsHandler)
        if handler is not None:
            return handler.get_aggregations(aggr, filter_type or filter.filter_type)

    def get_aggregations(self, aggregations):
        raise NotImplementedError
