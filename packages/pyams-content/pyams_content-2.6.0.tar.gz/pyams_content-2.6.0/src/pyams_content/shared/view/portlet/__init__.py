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

"""PyAMS_content.shared.view.portlet module

This module defines a portlet used to render view items.
"""

from itertools import islice, tee

from zope.schema.fieldproperty import FieldProperty

from pyams_content.shared.view.interfaces.query import IViewsMerger
from pyams_content.shared.view.portlet.interfaces import IViewItemsAggregates, \
    IViewItemsPortletSettings, SEARCH_EXCLUDED_ITEMS, VIEW_DISPLAY_CONTEXT, VIEW_ITEMS_PORTLET_NAME
from pyams_portal.interfaces import IPortletRendererSettings, PREVIEW_MODE
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_sequence.workflow import get_last_version, get_sequence_target, get_visible_version
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import DISPLAY_CONTEXT_KEY_NAME
from pyams_utils.list import unique_iter
from pyams_utils.request import check_request, get_annotations

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IViewItemsPortletSettings)
class ViewItemsPortletSettings(PortletSettings):
    """View items portlet settings persistent class"""

    title = FieldProperty(IViewItemsPortletSettings['title'])
    views = FieldProperty(IViewItemsPortletSettings['views'])
    views_context = FieldProperty(IViewItemsPortletSettings['views_context'])
    views_merge_mode = FieldProperty(IViewItemsPortletSettings['views_merge_mode'])
    limit = FieldProperty(IViewItemsPortletSettings['limit'])
    start = FieldProperty(IViewItemsPortletSettings['start'])
    force_canonical_url = FieldProperty(IViewItemsPortletSettings['force_canonical_url'])
    exclude_from_search = FieldProperty(IViewItemsPortletSettings['exclude_from_search'])
    first_page_only = FieldProperty(IViewItemsPortletSettings['first_page_only'])

    def get_views(self):
        """Portlet published views getter"""
        request = check_request()
        preview_mode = get_annotations(request).get(PREVIEW_MODE)
        for oid in self.views or ():
            view = get_sequence_target(oid, state=None)
            if view is not None:
                if preview_mode:
                    view = get_last_version(view)
                else:
                    view = get_visible_version(view)
            if view is not None:
                yield view

    def get_merger(self, request=None):
        """Views merger getter"""
        if request is None:
            request = check_request()
        return request.registry.queryUtility(IViewsMerger, name=self.views_merge_mode)

    def get_items(self, request=None, start=0, length=999, limit=None, ignore_cache=False):
        """Merged view items iterator"""
        if request is None:
            request = check_request()
        if self.views_context == VIEW_DISPLAY_CONTEXT:
            context = request.annotations.get(DISPLAY_CONTEXT_KEY_NAME, request.root)
        else:
            context = request.context
        if not ignore_cache:
            ignore_cache = request.annotations.get(PREVIEW_MODE, False)
        merger = self.get_merger(request)
        if merger is not None:
            renderer_settings = IPortletRendererSettings(self)
            aggregates = IViewItemsAggregates(renderer_settings, None)
            if aggregates is not None:
                ignore_cache = True
            else:
                aggregates = {}
            get_count = aggregates is not None
            results = merger.get_results(self.get_views(),
                                         context,
                                         ignore_cache=ignore_cache,
                                         request=request,
                                         aggregates=aggregates,
                                         settings=self,
                                         get_count=get_count)
            if get_count:
                count = next(results)
                aggregations = next(results)
            items = islice(unique_iter(results),
                           start + (self.start or 1) - 1,
                           limit or self.limit or 999)
            if (request is not None) and self.exclude_from_search:
                (excluded, items) = tee(items)
                excluded_items = request.annotations.get(SEARCH_EXCLUDED_ITEMS) or set()
                excluded_items |= set((ISequentialIdInfo(item).hex_oid for item in excluded))
                request.annotations[SEARCH_EXCLUDED_ITEMS] = excluded_items
            if get_count:
                yield count
                yield aggregations
            yield from items


@portlet_config(permission=None)
class ViewItemsPortlet(Portlet):
    """View items portlet"""

    name = VIEW_ITEMS_PORTLET_NAME
    label = _("View items")

    settings_factory = IViewItemsPortletSettings
    toolbar_css_class = 'fas fa-search'
