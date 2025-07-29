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

from zope.interface import Interface

from pyams_content.feature.filter.interfaces import IFilterIndexInfo, IFilterValues
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import get_pyramid_registry

__docformat__ = 'restructuredtext'


@adapter_config(required=Interface,
                provides=IFilterIndexInfo)
class FilterInfo(ContextAdapter):
    """Filter index info adapter"""

    @property
    def facets(self):
        result = []
        registry = get_pyramid_registry()
        for name, values in registry.getAdapters((self.context,), IFilterValues):
            result.extend(list(values))
        return result
