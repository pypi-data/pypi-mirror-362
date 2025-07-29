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

"""PyAMS_content.shared.view module

This module defines views persistent classes.
"""

import logging
from itertools import islice, tee

from pyramid.events import subscriber
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_catalog.query import CatalogResultSet
from pyams_content.feature.preview.interfaces import IPreviewTarget
from pyams_content.shared.common import ISharedContent, IWfSharedContent, SharedContent, WfSharedContent
from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_content.shared.view.interfaces import IView, IWfView, VIEW_CONTENT_NAME, VIEW_CONTENT_TYPE
from pyams_content.shared.view.interfaces.query import IViewQuery
from pyams_content.shared.view.interfaces.settings import IViewSettings
from pyams_utils.cache import get_cache
from pyams_utils.factory import factory_config, get_all_factories
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.registry import get_pyramid_registry, get_utility
from pyams_utils.request import check_request


LOGGER = logging.getLogger('PyAMS (content)')

VIEWS_CACHE_NAME = 'views'
VIEWS_CACHE_REGION = 'views'
VIEWS_CACHE_NAMESPACE = 'PyAMS::views'

VIEW_CACHE_KEY = 'view::{view}'
VIEW_CONTEXT_CACHE_KEY = 'view::{view}.context::{context}'

_MARKER = object()


@factory_config(IWfView)
@factory_config(IWfSharedContent, name=VIEW_CONTENT_TYPE)
@implementer(IPreviewTarget)
class WfView(WfSharedContent):
    """View persistent class"""

    content_type = VIEW_CONTENT_TYPE
    content_name = VIEW_CONTENT_NAME
    content_intf = IWfView
    content_view = False

    handle_content_url = False
    handle_header = False
    handle_description = False

    select_context_path = FieldProperty(IWfView['select_context_path'])
    select_context_type = FieldProperty(IWfView['select_context_type'])
    selected_content_types = FieldProperty(IWfView['selected_content_types'])
    select_context_datatype = FieldProperty(IWfView['select_context_datatype'])
    selected_datatypes = FieldProperty(IWfView['selected_datatypes'])
    excluded_content_types = FieldProperty(IWfView['excluded_content_types'])
    excluded_datatypes = FieldProperty(IWfView['excluded_datatypes'])
    allow_user_params = FieldProperty(IWfView['allow_user_params'])
    order_by = FieldProperty(IWfView['order_by'])
    reversed_order = FieldProperty(IWfView['reversed_order'])
    limit = FieldProperty(IWfView['limit'])
    age_limit = FieldProperty(IWfView['age_limit'])

    @property
    def is_using_context(self):
        """Check to know if view is using any context properties"""
        if self.select_context_path or self.select_context_type:
            return True
        registry = get_pyramid_registry()
        for name, adapter in registry.getAdapters((self,), IViewSettings):
            if not name:
                continue
            if adapter.is_using_context:
                return True
        return False

    def get_content_path(self, context):
        """Get path value of provided context"""
        if self.select_context_path:
            intids = get_utility(IIntIds)
            return intids.queryId(context)

    @staticmethod
    def get_ignored_types():
        """Get content types ignored from views, except if specified explicitly at runtime"""
        yield from (
            content_type
            for content_type, factory in get_all_factories(IWfSharedContent)
            if not factory.content_view
        )

    def get_content_types(self, context):
        """Get selected content types"""
        content_types = set()
        if self.select_context_type and IWfSharedContent.providedBy(context):
            content_types.add(context.content_type)
        if self.selected_content_types:
            content_types |= set(self.selected_content_types)
        return list(content_types)

    def get_data_types(self, context):
        """Get selected data types"""
        data_types = set()
        if self.select_context_datatype:
            content = IWfTypedSharedContent(context, None)
            if content is not None:
                data_types.add(content.data_type)
        if self.selected_datatypes:
            data_types |= set(self.selected_datatypes)
        return list(data_types)

    def get_excluded_content_types(self, context):
        """Get excluded content types"""
        return list(self.excluded_content_types or ())

    def get_excluded_data_types(self, context):
        """Get excluded data types"""
        return list(self.excluded_datatypes or ())

    def get_results(self, context, sort_index=None, reverse=None, limit=None,
                    start=0, length=999, ignore_cache=False, get_count=False, request=None,
                    aggregates=None, settings=None, **kwargs):
        """Get query results"""
        count, aggregations, results = 0, {}, _MARKER
        if (not ignore_cache) and self.allow_user_params:
            if request is None:
                request = check_request()
            ignore_cache = bool(request.params)
        if not ignore_cache:
            # check for cache
            views_cache = get_cache(VIEWS_CACHE_NAME, VIEWS_CACHE_REGION, VIEWS_CACHE_NAMESPACE)
            if self.is_using_context:
                cache_key = VIEW_CONTEXT_CACHE_KEY.format(view=ICacheKeyValue(self),
                                                          context=ICacheKeyValue(context))
            else:
                cache_key = VIEW_CACHE_KEY.format(view=ICacheKeyValue(self))
            try:
                results = views_cache.get_value(cache_key)
                count = views_cache.get_value(f'{cache_key}::count')
                aggregations = views_cache.get_value(f'{cache_key}::aggregations')
            except KeyError:
                pass
        # Execute query
        if results is _MARKER:
            registry = get_pyramid_registry()
            adapter = registry.getAdapter(self, IViewQuery)
            if not sort_index:
                sort_index = self.order_by
            # Get query results
            count, aggregations, results = adapter.get_results(context,
                                                               sort_index,
                                                               reverse if reverse is not None
                                                                   else self.reversed_order,
                                                               limit or self.limit,
                                                               request=request,
                                                               aggregates=aggregates,
                                                               settings=settings,
                                                               **kwargs)
            count = min(count, limit or self.limit or 999)
            cache, results = tee(islice(results, start, start + length))
            if not ignore_cache:
                intids = get_utility(IIntIds)
                views_cache.set_value(cache_key, [intids.queryId(item) for item in cache])
                views_cache.set_value(f'{cache_key}::count', count)
                views_cache.set_value(f'{cache_key}::aggregations', aggregations)
                LOGGER.debug(f"Storing view items to cache key {cache_key}")
        else:
            results = CatalogResultSet(results)
            LOGGER.debug(f"Retrieving view items from cache key {cache_key}")
        return (count, aggregations, results) if get_count else results


@subscriber(IObjectModifiedEvent, context_selector=IWfView)
def handle_modified_view(event):
    """Invalidate views cache when a view is modified"""
    view = event.object
    views_cache = get_cache(VIEWS_CACHE_NAME, VIEWS_CACHE_REGION, VIEWS_CACHE_NAMESPACE)
    if view.is_using_context:
        views_cache.clear()
    else:
        intids = get_utility(IIntIds)
        cache_key = VIEW_CACHE_KEY.format(view=intids.queryId(view))
        views_cache.remove(cache_key)


@factory_config(IView)
@factory_config(ISharedContent, name=VIEW_CONTENT_TYPE)
class View(SharedContent):
    """Workflow managed view class"""

    content_type = VIEW_CONTENT_TYPE
    content_name = VIEW_CONTENT_NAME
    content_view = False
