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

"""PyAMS_content.root.zmi.search module

This module defines components which are used to handle search on site root.
"""

__docformat__ = 'restructuredtext'

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import Any, Contains, Eq, Ge, Le
from pyramid.interfaces import IView
from pyramid.view import view_config
from zope.interface import Interface, implementer
from zope.intid import IIntIds
from zope.schema import Choice, TextLine
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_catalog.query import CatalogResultSet
from pyams_content.component.thesaurus import ICollectionsManager, ITagsManager, IThemesManager
from pyams_content.root.zmi.dashboard import BaseSiteRootDashboardTable, SiteRootDashboardView
from pyams_content.shared.common import SHARED_CONTENT_TYPES_VOCABULARY
from pyams_content.shared.common.zmi.search import SharedToolAdvancedSearchForm, \
    SharedToolAdvancedSearchResultsView, SharedToolAdvancedSearchView, \
    SharedToolQuickSearchPageView, SharedToolQuickSearchView, get_json_search_results, \
    get_quick_search_params
from pyams_content.zmi.interfaces import IAllDashboardMenu
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_i18n.interfaces import INegotiator
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.schema import PrincipalField
from pyams_sequence.interfaces import ISequentialIntIds
from pyams_sequence.workflow import get_last_version
from pyams_site.interfaces import ISiteRoot
from pyams_table.interfaces import IValues
from pyams_thesaurus.schema import ThesaurusTermsListField
from pyams_thesaurus.zmi.widget import ThesaurusTermsTreeFieldWidget
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.list import unique, unique_iter
from pyams_utils.registry import get_utility
from pyams_utils.schema import DatetimesRangeField
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IInnerTable
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

from pyams_content import _


#
# Quick search components
#

@implementer(IView)
class SiteRootQuickSearchResultsTable(BaseSiteRootDashboardTable):
    """Site root quick search results table"""


@adapter_config(required=(ISiteRoot, IPyAMSLayer, SiteRootQuickSearchResultsTable),
                provides=IValues)
class SiteRootQuickSearchResultsValues(ContextRequestViewAdapter):
    """Site root quick search results table values adapter"""

    @property
    def values(self):
        """Table values getter"""
        catalog = get_utility(ICatalog)
        query = self.request.params.get('query', '').strip()
        if not query:
            return ()
        sequence = get_utility(ISequentialIntIds)
        query = query.lower().replace('*', '')
        if query.startswith('+'):
            params = Eq(catalog['oid'], sequence.get_full_oid(query))
        else:
            vocabulary = getVocabularyRegistry().get(self.context,
                                                     SHARED_CONTENT_TYPES_VOCABULARY)
            params = Any(catalog['content_type'], vocabulary.by_value.keys())
            params &= get_quick_search_params(query, self.request, catalog, sequence)
        yield from unique_iter(map(get_last_version,
                                   CatalogResultSet(CatalogQuery(catalog).query(
                                       params, sort_index='modified_date', reverse=True))))


@view_config(name='quick-search.json',
             context=ISiteRoot, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION, renderer='json', xhr=True)
def shared_tool_quick_search_view(request):
    """Shared tool quick search view"""
    results = SiteRootQuickSearchResultsTable(request.context, request)
    return get_json_search_results(request, results)


@adapter_config(name='quick-search',
                required=(ISiteRoot, IAdminLayer, SiteRootDashboardView),
                provides=IInnerTable)
class SiteRootQuickSearchView(SharedToolQuickSearchView):
    """Shared tool quick search view"""

    @property
    def legend(self):
        """Legend getter"""
        translate = self.request.localizer.translate
        return translate(_("Between all contents"))


@pagelet_config(name='quick-search.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootQuickSearchPageView(SharedToolQuickSearchPageView):
    """Shared tool quick search page view"""

    table_class = SiteRootQuickSearchResultsTable


#
# Advanced search components
#

@viewlet_config(name='advanced-search.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IAllDashboardMenu, weight=40,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootAdvancedSearchMenu(NavigationMenuItem):
    """Site root advanced search menu"""

    label = _("Advanced search")
    href = "#advanced-search.html"


class ISiteRootAdvancedSearchQuery(Interface):
    """Site root advanced search query interface"""

    query = TextLine(title=_("Search text"),
                     description=_("Entered text will be search in title only"),
                     required=False)

    owner = PrincipalField(title=_("Owner"),
                           required=False)

    content_type = Choice(title=_("Content type"),
                          vocabulary=SHARED_CONTENT_TYPES_VOCABULARY,
                          required=False)

    created = DatetimesRangeField(title=_("Creation date"),
                                  required=False)

    modified = DatetimesRangeField(title=_("Modification date"),
                                   required=False)

    tags = ThesaurusTermsListField(title=_("Tags"),
                                   required=False)

    themes = ThesaurusTermsListField(title=_("Themes"),
                                     required=False)

    collections = ThesaurusTermsListField(title=_("Collections"),
                                          required=False)


class SiteRootAdvancedSearchForm(SharedToolAdvancedSearchForm):
    """Site root advanced search form"""


@adapter_config(required=(Interface, IAdminLayer, SiteRootAdvancedSearchForm),
                provides=IFormFields)
def site_root_advanced_search_form_fields(context, request, form):
    """Site root advanced search form fields getter"""
    return Fields(ISiteRootAdvancedSearchQuery).omit('tags', 'themes', 'collections')


class BaseThesaurusTermsSearchGroup(FormGroupSwitcher):
    """Base thesaurus terms search group"""

    fieldname = None
    manager = None

    def __new__(cls, context, request, view):
        manager = cls.manager(request.root)
        if not manager.thesaurus_name:
            return None
        return FormGroupSwitcher.__new__(cls)

    @property
    def fields(self):
        """Fields getter"""
        fields = Fields(ISiteRootAdvancedSearchQuery).select(self.fieldname)
        fields[self.fieldname].widget_factory = ThesaurusTermsTreeFieldWidget
        return fields

    label_css_class = 'hidden'
    input_css_class = 'col-12'

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        terms = self.widgets.get(self.fieldname)
        if terms is not None:
            manager = self.manager(self.request.root)
            terms.thesaurus_name = manager.thesaurus_name
            terms.extract_name = manager.extract_name


@adapter_config(name='tags',
                required=(ISiteRoot, IAdminLayer, SiteRootAdvancedSearchForm),
                provides=IGroup)
class SiteRootAdvancedSearchFormTagsGroup(BaseThesaurusTermsSearchGroup):
    """Site root advanced search form tags group"""

    legend = _("Tags")

    fieldname = 'tags'
    manager = ITagsManager

    weight = 10


@adapter_config(name='themes',
                required=(ISiteRoot, IAdminLayer, SiteRootAdvancedSearchForm),
                provides=IGroup)
class SiteRootAdvancedSearchFormThemesGroup(BaseThesaurusTermsSearchGroup):
    """Site root advanced search form themes group"""

    legend = _("Themes")

    fieldname = 'themes'
    manager = IThemesManager

    weight = 20


@adapter_config(name='collections',
                required=(ISiteRoot, IAdminLayer, SiteRootAdvancedSearchForm),
                provides=IGroup)
class SharedToolAdvancedSearchFormCollectionsGroup(BaseThesaurusTermsSearchGroup):
    """Shared tool advanced search form collections group"""

    legend = _("Collections")

    fieldname = 'collections'
    manager = ICollectionsManager

    weight = 30


@pagelet_config(name='advanced-search.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootAdvancedSearchView(SharedToolAdvancedSearchView):
    """Site root advanced search view"""

    search_form = SiteRootAdvancedSearchForm


class SiteRootAdvancedSearchResultsTable(BaseSiteRootDashboardTable):
    """Site root advanced search results table"""


@adapter_config(required=(ISiteRoot, IPyAMSLayer, SiteRootAdvancedSearchResultsTable),
                provides=IValues)
class SiteRootAdvancedSearchResultsValues(ContextRequestViewAdapter):
    """Site root advanced search results values"""

    def get_params(self, data):
        """Extract catalog query params from incoming request"""
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = Any(catalog['content_type'], vocabulary.by_value.keys())
        query = data.get('query')
        if query:
            sequence = get_utility(ISequentialIntIds)
            if query.startswith('+'):
                params &= Eq(catalog['oid'], sequence.get_full_oid(query))
            else:
                query_params = Eq(catalog['oid'], sequence.get_full_oid(query))
                negotiator = get_utility(INegotiator)
                for lang in {self.request.registry.settings.get('pyramid.default_locale_name',
                                                                'en'),
                             self.request.locale_name,
                             negotiator.server_language} | negotiator.offered_languages:
                    index_name = 'title:{0}'.format(lang)
                    if index_name in catalog:
                        index = catalog[index_name]
                        if index.check_query(query):
                            query_params |= Contains(index,
                                                     ' and '.join((w+'*' for w in query.split())))
                params &= query_params
        if data.get('owner'):
            params &= Eq(catalog['role:owner'], data['owner'])
        if data.get('content_type'):
            params &= Eq(catalog['content_type'], data['content_type'])
        created_after, created_before = data.get('created', (None, None))
        if created_after:
            params &= Ge(catalog['created_date'], created_after)
        if created_before:
            params &= Le(catalog['created_date'], created_before)
        modified_after, modified_before = data.get('modified', (None, None))
        if modified_after:
            params &= Ge(catalog['modified_date'], modified_after)
        if modified_before:
            params &= Le(catalog['modified_date'], modified_before)
        if data.get('tags'):
            tags = [intids.register(term) for term in data['tags']]
            params &= Any(catalog['tags'], tags)
        if data.get('themes'):
            tags = [intids.register(term) for term in data['themes']]
            params &= Any(catalog['themes'], tags)
        if data.get('collections'):
            tags = [intids.register(term) for term in data['collections']]
            params &= Any(catalog['collections'], tags)
        return params

    @property
    def values(self):
        """Shared tool advanced search results values getter"""
        form = SiteRootAdvancedSearchForm(self.context, self.request)
        form.update()
        data, _errors = form.extract_data()
        params = self.get_params(data)
        catalog = get_utility(ICatalog)
        yield from unique_iter(map(get_last_version,
                                   CatalogResultSet(CatalogQuery(catalog).query(
                                       params, sort_index='modified_date', reverse=True))))


@pagelet_config(name='advanced-search-results.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION, xhr=True)
class SiteRootAdvancedSearchResultsView(SharedToolAdvancedSearchResultsView):
    """Site root advanced search results view"""

    table_class = SiteRootAdvancedSearchResultsTable
