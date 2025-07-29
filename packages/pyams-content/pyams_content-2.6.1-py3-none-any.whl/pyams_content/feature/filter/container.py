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

from zope.location.interfaces import ISublocations
from zope.traversing.interfaces import ITraversable

from pyams_content.feature.filter.interfaces import FILTER_CONTAINER_ANNOTATION_KEY, IFilterProcessor, \
    IFiltersContainer, IFiltersContainerTarget
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'


#
# Filters container
#

@factory_config(IFiltersContainer)
class FilterContainer(BTreeOrderedContainer):
    """Filter container"""

    def get_visible_filters(self):
        yield from filter(lambda x: x.visible, self.values())

    def get_processed_filters(self, context, request, aggregations):
        registry = request.registry
        for filter in self.get_visible_filters():
            processor = registry.queryMultiAdapter((filter, request, self),
                                                   IFilterProcessor)
            if processor is not None:
                yield processor.process(aggregations)


@adapter_config(required=IFiltersContainer,
                provides=IViewContextPermissionChecker)
class FilterContainerPermissionChecker(ContextAdapter):
    """Filter container permission checker"""

    edit_permission = MANAGE_TEMPLATE_PERMISSION


@adapter_config(required=IFiltersContainerTarget,
                provides=IFiltersContainer)
def filter_container(context):
    """Filter container adapter"""
    return get_annotation_adapter(context, FILTER_CONTAINER_ANNOTATION_KEY,
                                  IFiltersContainer, name='++filter++')


@adapter_config(name='filter',
                required=IFiltersContainerTarget,
                provides=ITraversable)
class FilterContainerTraverser(ContextAdapter):
    """Filter container traverser"""

    def traverse(self, name, furtherPath=None):
        container = IFiltersContainer(self.context, None)
        if name:
            return container.get(name)
        return container


@adapter_config(name='filter',
                required=IFiltersContainerTarget,
                provides=ISublocations)
class FilterContainerSublocations(ContextAdapter):
    """Filter container sublocations"""

    def sublocations(self):
        return IFiltersContainer(self.context).values()
