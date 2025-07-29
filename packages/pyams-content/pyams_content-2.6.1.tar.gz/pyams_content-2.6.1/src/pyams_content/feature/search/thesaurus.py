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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from hypatia.interfaces import ICatalog
from hypatia.query import Any
from zope.intid.interfaces import IIntIds

from pyams_content.component.thesaurus import ICollectionsManager, ITagsManager, IThemesManager
from pyams_content.feature.search.interfaces import ISearchFolder, ISearchFolderQuery, ISearchFormRequestParams
from pyams_content.shared.view.interfaces.query import IViewUserQuery
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_thesaurus.interfaces.thesaurus import IThesaurus
from pyams_utils.adapter import ContextAdapter, ContextRequestAdapter, adapter_config
from pyams_utils.registry import get_utility, query_utility


#
# Tags search adapters
#

@adapter_config(name='tags',
                required=ISearchFolderQuery,
                provides=IViewUserQuery)
class SearchFolderTagQuery(ContextAdapter):
    """Search folder tags query"""

    @staticmethod
    def get_user_params(request):
        tags = request.params.getall('tag')
        if not tags:
            return
        manager = ITagsManager(request.root, None)
        if manager is None:
            return
        thesaurus = query_utility(IThesaurus, name=manager.thesaurus_name)
        if thesaurus is None:
            return
        if isinstance(tags, str):
            tags = tags.split(',')
        catalog = get_utility(ICatalog)
        intids = query_utility(IIntIds)
        yield Any(catalog['tags'], [
            intids.queryId(term)
            for term in [
                thesaurus.terms.get(value)
                for tag in tags
                for value in tag.split(',')
            ]
            if term is not None
        ])


@adapter_config(name='tags',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormTagsRequestParams(ContextRequestAdapter):
    """Search form tags request params"""

    def get_params(self):
        """Request params getter"""
        for tag in self.request.params.getall('tag'):
            yield {
                'name': 'tag',
                'value': tag
            }


#
# Themes search adapters
#

@adapter_config(name='themes',
                required=ISearchFolderQuery,
                provides=IViewUserQuery)
class SearchFolderThemeQuery(ContextAdapter):
    """Search folder themes query"""

    @staticmethod
    def get_user_params(request):
        themes = request.params.get('theme')
        if not themes:
            return
        manager = IThemesManager(request.root, None)
        if manager is None:
            return
        thesaurus = query_utility(IThesaurus, name=manager.thesaurus_name)
        if thesaurus is None:
            return
        if isinstance(themes, str):
            themes = themes.split(',')
        catalog = get_utility(ICatalog)
        intids = query_utility(IIntIds)
        yield Any(catalog['themes'], [
            intids.queryId(term)
            for term in [
                thesaurus.terms.get(value)
                for theme in themes
                for value in theme.split(',')
            ]
            if term is not None
        ])


@adapter_config(name='themes',
                required=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormThemesRequestParams(ContextRequestAdapter):
    """Search form themes request params"""

    def get_params(self):
        """Request params getter"""
        for theme in self.request.params.getall('theme'):
            yield {
                'name': 'theme',
                'value': theme
            }


#
# Collections search adapters
#

@adapter_config(name='collections',
                context=ISearchFolderQuery,
                provides=IViewUserQuery)
class SearchFolderCollectionQuery(ContextAdapter):
    """Search folder collections query"""

    @staticmethod
    def get_user_params(request):
        collections = request.params.getall('collection')
        if not collections:
            return
        manager = ICollectionsManager(request.root, None)
        if manager is None:
            return
        thesaurus = query_utility(IThesaurus, name=manager.thesaurus_name)
        if thesaurus is None:
            return
        if isinstance(collections, str):
            collections = collections.split(',')
        catalog = get_utility(ICatalog)
        intids = query_utility(IIntIds)
        yield Any(catalog['collections'], [
            intids.queryId(term)
            for term in [
                thesaurus.terms.get(value)
                for collection in collections
                for value in collection.split(',')
            ]
            if term is not None
        ])


@adapter_config(name='collections',
                context=(ISearchFolder, IPyAMSUserLayer),
                provides=ISearchFormRequestParams)
class SearchFormCollectionsRequestParams(ContextRequestAdapter):
    """Search form tags request params"""

    def get_params(self):
        for collection in self.request.params.getall('collection'):
            yield {
                'name': 'collection',
                'value': collection
            }
