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

"""PyAMS_content.shared.view.query module

This module defines adapters which are used to handle catalog-based
views queries. These adapters can be overriden, for example by packages
providing Elasticsearch support (see :py:mod:`pyams_content_es`).
"""

from datetime import datetime, timedelta, timezone

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import Any, Eq, Gt, Lt, NotAny, Or

from pyams_catalog.query import CatalogResultSet, or_
from pyams_content.shared.view import IViewQuery, IWfView
from pyams_content.shared.view.interfaces import RELEVANCE_ORDER, TITLE_ORDER
from pyams_content.shared.view.interfaces.query import END_PARAMS_MARKER, IViewQueryFilterExtension, \
    IViewQueryParamsExtension, IViewUserQuery
from pyams_i18n.interfaces import INegotiator
from pyams_utils.adapter import ContextAdapter, adapter_config, get_adapter_weight
from pyams_utils.list import unique_iter
from pyams_utils.registry import get_pyramid_registry, get_utility
from pyams_utils.timezone import tztime
from pyams_workflow.interfaces import IWorkflow

__docformat__ = 'restructuredtext'


@adapter_config(required=IWfView,
                provides=IViewQuery)
class ViewQuery(ContextAdapter):
    """View query"""

    def get_params(self, context, request=None, **kwargs):
        view = self.context
        catalog = get_utility(ICatalog)
        registry = get_pyramid_registry()
        # check publication dates
        now = tztime(datetime.now(timezone.utc))
        params = Lt(catalog['effective_date'], now)
        # check workflow states
        if 'state' in kwargs:
            state = kwargs['state']
            if not isinstance(state, (list, tuple, set)):
                state = (state,)
            params &= Any(catalog['workflow_state'], state)
        else:
            wf_params = None
            for workflow in registry.getAllUtilitiesRegisteredFor(IWorkflow):
                wf_params = or_(wf_params, Any(catalog['workflow_state'], workflow.visible_states))
            params &= wf_params
        # check custom extensions
        get_all_params = True
        for name, adapter in sorted(registry.getAdapters((view,), IViewQueryParamsExtension),
                                    key=get_adapter_weight):
            for new_params in adapter.get_params(context, request):
                if new_params is None:
                    return None
                elif new_params is END_PARAMS_MARKER:
                    get_all_params = False
                    break
                else:
                    params &= new_params
            else:
                continue
            break
        # activate search
        filters = Or(Eq(catalog['push_end_date'], None),
                     Gt(catalog['push_end_date'], now))
        if get_all_params:
            # check content path
            content_path = view.get_content_path(context)
            if content_path is not None:
                filters &= Eq(catalog['parents'], content_path)
            # check content types
            if 'content_type' in kwargs:
                filters &= Eq(catalog['content_type'], kwargs['content_type'])
            else:
                filters &= NotAny(catalog['content_type'], set(view.get_ignored_types()))
                content_types = view.get_content_types(context)
                if content_types:
                    filters &= Any(catalog['content_type'], content_types)
            # check data types
            data_types = view.get_data_types(context)
            if data_types:
                filters &= Any(catalog['data_type'], data_types)
            # check excluded content types
            content_types = view.get_excluded_content_types(context)
            if content_types:
                filters &= NotAny(catalog['content_type'], content_types)
            # check excluded data types
            data_types = view.get_excluded_data_types(context)
            if data_types:
                filters &= NotAny(catalog['data_type'], data_types)
            # check age limit
            age_limit = view.age_limit
            if age_limit:
                filters &= Gt(catalog['content_publication_date'],
                              now - timedelta(days=age_limit))
        params &= filters
        return params

    def get_results(self, context, sort_index, reverse, limit,
                    request=None, aggregates=None, settings=None, **kwargs):
        view = self.context
        catalog = get_utility(ICatalog)
        registry = get_pyramid_registry()
        params = self.get_params(context, request, **kwargs)
        if params is None:
            items = CatalogResultSet([])
            total_count = 0
        else:
            if (not sort_index) or (sort_index == RELEVANCE_ORDER):
                sort_index = None
            elif sort_index == TITLE_ORDER:
                negotiator = get_utility(INegotiator)
                sort_index = f'title:{negotiator.server_language}'
            query = CatalogQuery(catalog).query(params,
                                                sort_index=sort_index,
                                                reverse=reverse,
                                                limit=limit)
            total_count = query[0]
            items = CatalogResultSet(query)
        for name, adapter in sorted(registry.getAdapters((view,), IViewQueryFilterExtension),
                                    key=get_adapter_weight):
            items = adapter.filter(context, items, request)
        return unique_iter(items), total_count, {}


@adapter_config(name='user-params',
                required=IWfView,
                provides=IViewQueryParamsExtension)
class UserViewQueryParamsExtension(ContextAdapter):
    """User view query params extension"""

    weight = 999

    def __new__(cls, context):
        if not context.allow_user_params:
            return None
        return ContextAdapter.__new__(cls)

    def get_params(self, context, request=None):
        """User params getter"""
        registry = get_pyramid_registry()
        for name, adapter in sorted(registry.getAdapters((self.context,), IViewUserQuery),
                                    key=get_adapter_weight):
            yield from adapter.get_user_params(request)
