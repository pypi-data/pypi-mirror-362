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

__docformat__ = 'restructuredtext'

from pyams_content.feature.filter import IFilterAggregate
from pyams_content.feature.filter.interfaces import IAggregatedPortletRendererSettings, IFiltersContainer
from pyams_content.shared.view.portlet import IViewItemsAggregates
from pyams_utils.adapter import adapter_config


@adapter_config(required=IAggregatedPortletRendererSettings,
                provides=IViewItemsAggregates)
def aggregated_portlet_settings_aggregates(settings):
    """Aggregated portlet settings aggregates"""
    container = IFiltersContainer(settings, None)
    if container is None:
        return None
    for visible_filter in container.get_visible_filters():
        aggregate = IFilterAggregate(visible_filter, None)
        if aggregate is not None:
            yield aggregate
