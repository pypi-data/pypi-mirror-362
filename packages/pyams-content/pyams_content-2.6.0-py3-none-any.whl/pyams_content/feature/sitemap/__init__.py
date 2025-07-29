#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.feature.sitemap module

This module defines main sitemap management components.
"""

from datetime import datetime, timezone
from itertools import product

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import Any, Eq
from pyramid.traversal import resource_path
from pyramid.view import view_config
from zope.intid import IIntIds
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_catalog.query import CatalogResultSet
from pyams_content.feature.seo import ISEOContentInfo
from pyams_content.feature.sitemap.interfaces import IRobotsExtension, ISitemapExtension
from pyams_content.root import ISiteRootToolsConfiguration
from pyams_content.shared.common import IBaseSharedTool, SHARED_CONTENT_TYPES_VOCABULARY
from pyams_content.shared.site.interfaces import ISiteManager, SITE_MANAGER_INDEXATION_INTERNAL_MODE, \
    SITE_MANAGER_INDEXATION_NULL_MODE
from pyams_i18n.interfaces import II18nManager
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_site.interfaces import ISiteRoot
from pyams_utils.list import unique_iter
from pyams_utils.registry import get_all_utilities_registered_for, get_utilities_for, get_utility
from pyams_utils.timezone import tztime
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo

__docformat__ = 'restructuredtext'


@view_config(name='robots.txt',
             context=ISiteRoot, request_type=IPyAMSUserLayer,
             renderer='templates/robots.pt')
def site_root_robots_view(request):
    """Site root robots.txt view"""
    request.response.content_type = 'text/plain'
    disallowed_sites = []
    allowed_inner_sites = []
    for site in get_all_utilities_registered_for(ISiteManager):
        publication_info = IWorkflowPublicationInfo(site, None)
        if (publication_info is not None) and not publication_info.is_visible(request):
            disallowed_sites.append(site)
            continue
        if site.indexation_mode == SITE_MANAGER_INDEXATION_INTERNAL_MODE:
            disallowed_sites.append(site)
            allowed_inner_sites.append(site)
        elif site.indexation_mode == SITE_MANAGER_INDEXATION_NULL_MODE:
            disallowed_sites.append(site)
    disallowed_tools = []
    for name, tool in get_utilities_for(IBaseSharedTool):
        if not name:
            continue
        seo_info = ISEOContentInfo(tool, None)
        if seo_info is None:
            if not tool.shared_content_menu:
                disallowed_tools.append(resource_path(tool))
                continue
        else:
            if not seo_info.include_sitemap:
                disallowed_tools.append(resource_path(tool))
                continue
        publication_info = IWorkflowPublicationInfo(tool, None)
        if (publication_info is not None) and not publication_info.is_visible(request):
            disallowed_tools.append(resource_path(tool))
    extensions = []
    for name, adapter in request.registry.getAdapters((request.context, request),
                                                      IRobotsExtension):
        extensions.append(adapter)
    return {
        'tools_configuration': ISiteRootToolsConfiguration(request.root),
        'disallowed_sites': disallowed_sites,
        'allowed_inner_sites': allowed_inner_sites,
        'disallowed_tools': disallowed_tools,
        'extensions': extensions
    }


@view_config(name='humans.txt',
             context=ISiteRoot, request_type=IPyAMSUserLayer,
             renderer='templates/humans.pt')
def site_root_humans_view(request):
    """Site root humans.txt view"""
    request.response.content_type = 'text/plain'
    return {}


@view_config(name='sitemap.xml',
             context=ISiteRoot, request_type=IPyAMSUserLayer,
             renderer='templates/root-sitemap.pt')
class SiteRootSitemapView:
    """Site root sitemap view"""

    def __init__(self, request):
        self.request = request

    def __call__(self):
        self.request.response.content_type = 'text/xml'
        return {}

    @property
    def sources(self):
        """Sitemap sources"""
        request = self.request
        timestamp = tztime(datetime.now(timezone.utc)).isoformat()
        for name, tool in get_utilities_for(IBaseSharedTool):
            if not name:
                continue
            seo_info = ISEOContentInfo(tool, None)
            if seo_info is None:
                if not tool.shared_content_menu:
                    continue
            else:
                if not seo_info.include_sitemap:
                    continue
            publication_info = IWorkflowPublicationInfo(tool, None)
            if (publication_info is None) or publication_info.is_visible(request):
                yield timestamp, tool
        for name, adapter in request.registry.getAdapters((request.context, request),
                                                          ISitemapExtension):
            source = adapter.source
            if source is not None:
                yield timestamp, source


@view_config(name='sitemap.xml',
             context=IBaseSharedTool, request_type=IPyAMSUserLayer,
             renderer='templates/tool-sitemap.pt')
class SharedToolSitemapView:
    """Shared tool sitemap view"""

    def __init__(self, request):
        self.request = request

    def __call__(self):
        self.request.response.content_type = 'text/xml'
        return {}

    @property
    def contents(self):
        """Sitemap contents getter"""
        context = self.request.context
        catalog = get_utility(ICatalog)
        intids = get_utility(IIntIds)
        workflow = IWorkflow(context)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = Eq(catalog['parents'], intids.register(context)) & \
            Any(catalog['content_type'], vocabulary.by_value.keys()) & \
            Any(catalog['workflow_state'], workflow.visible_states)
        for version in unique_iter(CatalogResultSet(CatalogQuery(catalog).query(params))):
            seo_info = ISEOContentInfo(version, None)
            if (seo_info is None) or seo_info.include_sitemap:
                yield from product(II18nManager(version).get_languages(), (version,))
