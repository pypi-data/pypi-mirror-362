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
from pyams_content.feature.filter.interfaces import IAggregatedPortletRendererSettings, \
    IFilterProcessorAggregationsHandler, IFiltersContainer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_portal.interfaces import IPortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.dict import DotDict
from pyams_viewlet.viewlet import BaseContentProvider, contentprovider_config

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(IFilter, IPyAMSUserLayer, IAggregatedPortletRendererSettings),
                provides=IFilterProcessorAggregationsHandler)
class FilterProcessorAggregationsHandler:
    """"""

    def __init__(self, filter, request, renderer_settings):
        self.filter = filter
        self.request = request
        self.renderer_settings = renderer_settings

    def get_aggregations(self, aggr, filter_type):
        filter = self.filter
        request = self.request
        current_filters = [
            value
            for param in request.params.getall(filter_type)
            for value in param.split(',')
        ]
        initial_options = self.get_displayed_options(aggr, filter.displayed_entries)
        additional_options = [
            option
            for index, option in enumerate(aggr)
            if index >= filter.displayed_entries
        ]
        is_expanded_condition = any(
            item['key'] in current_filters
            for item in additional_options
        )
        show_more = len(aggr) > filter.displayed_entries
        is_expanded = show_more and is_expanded_condition
        translate = request.localizer.translate
        placeholder = II18n(filter).query_attribute("select_placeholder")
        if not placeholder:
            placeholder = translate(_("-- No selected option --"))
        return DotDict({
            'filter': filter,
            "filter_type": filter_type,
            'current_filters': current_filters,
            'initial_options': initial_options,
            'additional_options': additional_options,
            'all_options': aggr,
            'is_active': bool(current_filters),
            'show_more': show_more,
            "select_placeholder": placeholder,
            "is_expanded": is_expanded,
            "show_more_text": translate(_("Show more")),
            "show_less_text": translate(_("Show less"))
        })

    @staticmethod
    def get_displayed_options(options, num_entries):
        return options[:num_entries]


@contentprovider_config(name='filters_default',
                        layer=IPyAMSUserLayer, view=IPortletRenderer)
@template_config(template='templates/filters-default.pt',
                 layer=IPyAMSUserLayer)
class DefaultFiltersRenderer(BaseContentProvider):
    """Default filters renderer"""

    filters = None

    def update(self, renderer_settings=None, aggregations=None):
        super().update()
        container = IFiltersContainer(renderer_settings, None)
        if container is not None:
            self.filters = container.get_processed_filters(self.context, self.request, aggregations)
