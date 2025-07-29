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

"""PyAMS_content.feature.search.portlet module

"""

import math

from zope.schema.fieldproperty import FieldProperty

from pyams_content.feature.search import ISearchFolder
from pyams_content.feature.search.portlet.interfaces import ISearchResultsPortletSettings, SEARCH_RESULTS_ICON_CLASS, \
    SEARCH_RESULTS_PORTLET_FLAG, SEARCH_RESULTS_PORTLET_NAME
from pyams_content.shared.view.interfaces import RELEVANCE_ORDER, VISIBLE_PUBLICATION_DATE_ORDER
from pyams_content.shared.view.portlet import IViewItemsAggregates
from pyams_portal.interfaces import IPortletRendererSettings
from pyams_portal.portlet import Portlet, PortletSettings, portlet_config
from pyams_utils.factory import factory_config
from pyams_utils.list import boolean_iter
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(ISearchResultsPortletSettings)
class SearchResultsPortletSettings(PortletSettings):
    """Search results portlet settings"""

    title = FieldProperty(ISearchResultsPortletSettings['title'])
    allow_empty_query = FieldProperty(ISearchResultsPortletSettings['allow_empty_query'])
    force_canonical_url = FieldProperty(ISearchResultsPortletSettings['force_canonical_url'])

    @staticmethod
    def has_user_query(request):
        """User query checker"""
        return bool(request.params.get('user_search', '').strip())

    def _get_items(self, request=None, start=0, length=10, limit=None, ignore_cache=False):
        context = get_parent(request.context, ISearchFolder)
        if context is None:
            raise StopIteration
        else:
            if request is None:
                request = check_request()
            params = request.params
            order_by = params.get('order_by', context.order_by)
            if (order_by == RELEVANCE_ORDER) and \
                    not self.has_user_query(request):
                request.GET['order_by'] = order_by = VISIBLE_PUBLICATION_DATE_ORDER
            renderer_settings = IPortletRendererSettings(self)
            aggregates = IViewItemsAggregates(renderer_settings, None)
            if aggregates is not None:
                ignore_cache = True
            else:
                aggregates = {}
            yield from context.get_results(context, order_by,
                                           reverse=order_by != RELEVANCE_ORDER,
                                           limit=limit,
                                           start=int(start),
                                           length=int(length),
                                           ignore_cache=ignore_cache,
                                           get_count=True,
                                           request=request,
                                           aggregates=aggregates,
                                           settings=self)

    def get_items(self, request=None, start=0, length=10, limit=None, ignore_cache=False):
        """Search results getter"""
        if not (self.allow_empty_query or self.has_user_query(request)):
            yield from iter((0, {}, ()), )
        else:
            has_items, items = boolean_iter(self._get_items(request, start, length, limit,
                                                            ignore_cache))
            if not has_items:
                yield from iter((0, {}, ()), )
            else:
                # verify real items count
                count = next(items)
                aggregations = next(items)
                if count:
                    if request is None:
                        request = check_request()
                    request.annotations[SEARCH_RESULTS_PORTLET_FLAG] = True
                yield count
                yield aggregations
                yield from items

    @staticmethod
    def get_pages(start, length, count):
        start = int(start) + 1
        length = int(length)
        current = math.ceil(start / length)
        nb_pages = math.ceil(count / length)
        return current, nb_pages


@portlet_config(permission=None)
class SearchResultsPortlet(Portlet):
    """Search folder results portlet"""

    name = SEARCH_RESULTS_PORTLET_NAME
    label = _("Search results")

    settings_factory = ISearchResultsPortletSettings
    toolbar_css_class = SEARCH_RESULTS_ICON_CLASS
