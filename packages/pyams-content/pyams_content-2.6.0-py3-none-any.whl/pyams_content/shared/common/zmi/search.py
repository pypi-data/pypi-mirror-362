#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.shared.common.zmi.search module

This module provides components used for contents searching from dashboards.
"""

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Any, Contains, Eq, Ge, Le
from pyramid.interfaces import IView
from pyramid.view import view_config
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface, implementer
from zope.intid import IIntIds
from zope.schema import Choice, TextLine
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_catalog.query import CatalogResultSet
from pyams_content.component.thesaurus import ICollectionsManager, ITagsManager, IThemesManager
from pyams_content.shared.common import IBaseSharedTool, SHARED_CONTENT_TYPES_VOCABULARY
from pyams_content.shared.common.interfaces import SHARED_TOOL_WORKFLOW_STATES_VOCABULARY
from pyams_content.shared.common.interfaces.types import DATA_TYPES_VOCABULARY
from pyams_content.shared.common.zmi.dashboard import BaseSharedToolDashboardSingleView, \
    DashboardTable, BaseSharedToolDashboardView, SharedToolDashboardView
from pyams_content.zmi.interfaces import IAllDashboardMenu
from pyams_form.field import Fields
from pyams_form.interfaces.form import IFormFields, IGroup
from pyams_i18n.interfaces import INegotiator
from pyams_layer.interfaces import IPyAMSLayer
from pyams_layer.skin import apply_skin
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.schema import PrincipalField
from pyams_sequence.interfaces import ISequentialIntIds
from pyams_sequence.workflow import get_last_version
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_table.interfaces import IValues
from pyams_template.template import template_config
from pyams_thesaurus.schema import ThesaurusTermsListField
from pyams_thesaurus.zmi.widget import ThesaurusTermsTreeFieldWidget
from pyams_utils.adapter import ContextRequestViewAdapter, NullAdapter, adapter_config
from pyams_utils.list import unique_iter
from pyams_utils.registry import get_utility
from pyams_utils.schema import DatetimesRangeField
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_utils.vocabulary import vocabulary_config
from pyams_viewlet.viewlet import EmptyViewlet, ViewContentProvider, viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowVersions
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IInnerTable
from pyams_zmi.search import SearchForm, SearchResultsView, SearchView
from pyams_zmi.skin import AdminSkin
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(IView)
class SharedToolQuickSearchResultsTable(DashboardTable):
    """Shared tool quick search results table"""


def get_quick_search_params(query, request, catalog, sequence):
    """Get quick search params"""
    query_params = Eq(catalog['oid'], sequence.get_full_oid(query))
    negotiator = get_utility(INegotiator)
    for lang in {
                    request.registry.settings.get('pyramid.default_locale_name', 'en'),
                    request.locale_name,
                    negotiator.server_language
                } | negotiator.offered_languages:
        index_name = f'title:{lang}'
        if index_name in catalog:
            index = catalog[index_name]
            if index.check_query(query):
                query_params |= Contains(index,
                                         ' and '.join((f'{w}*' for w in query.split())))
    return query_params


@adapter_config(required=(IBaseSharedTool, IPyAMSLayer, SharedToolQuickSearchResultsTable),
                provides=IValues)
class SharedToolQuickSearchResultsValues(ContextRequestViewAdapter):
    """Shared tool quick search results values adapter"""

    @property
    def values(self):
        """Table values getter"""
        intids = get_utility(IIntIds)
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
            params = And(Eq(catalog['parents'], intids.register(self.context)),
                         Any(catalog['content_type'], vocabulary.by_value.keys()))
            params &= get_quick_search_params(query, self.request, catalog, sequence)
        yield from unique_iter(map(get_last_version,
                                   CatalogResultSet(CatalogQuery(catalog).query(
                                       params, sort_index='modified_date', reverse=True))))


def get_json_search_results(request, results):
    """Get search results as JSON response"""
    if len(results.values) == 1:
        result = results.values[0]
        return {
            'status': 'redirect',
            'location': absolute_url(result, request, 'admin')
        }
    apply_skin(request, AdminSkin)
    results.update()
    return {
        'status': 'info',
        'content': {
            'html': results.render()
        }
    }


@view_config(name='quick-search.json',
             context=IBaseSharedTool, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION, renderer='json', xhr=True)
def shared_tool_quick_search_view(request):
    """Shared tool quick search view"""
    results = SharedToolQuickSearchResultsTable(request.context, request)
    return get_json_search_results(request, results)


@adapter_config(name='quick-search',
                required=(IBaseSharedTool, IAdminLayer, SharedToolDashboardView),
                provides=IInnerTable)
@template_config(template='templates/quick-search.pt', layer=IAdminLayer)
class SharedToolQuickSearchView(BaseSharedToolDashboardView):
    """Shared tool quick search view"""

    @property
    def legend(self):
        """Legend getter"""
        translate = self.request.localizer.translate
        return translate(_("Between all contents of « {} » content type")) \
            .format(translate(self.context.shared_content_factory.factory.content_name))

    def render(self):
        """Viewlet renderer"""
        return ViewContentProvider.render(self)


@pagelet_config(name='quick-search.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolQuickSearchPageView(BaseSharedToolDashboardSingleView):
    """Shared tool quick search page view"""

    table_class = SharedToolQuickSearchResultsTable

    empty_label = _("SEARCH - No result found")
    single_label = _("SEARCH - 1 result found")
    plural_label = _("SEARCH - {} results found")


#
# Advanced search components
#

@vocabulary_config(name=SHARED_TOOL_WORKFLOW_STATES_VOCABULARY)
def WorkflowStatesVocabulary(context):
    """Workflow states vocabulary"""
    target = get_parent(context, IBaseSharedTool)
    if target is not None:
        workflow = IWorkflow(target)
        return workflow.states


@viewlet_config(name='advanced-search.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IAllDashboardMenu, weight=40,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolAdvancedSearchMenu(NavigationMenuItem):
    """Shared tool advanced search menu"""

    label = _("Advanced search")
    href = "#advanced-search.html"


class ISharedToolAdvancedSearchQuery(Interface):
    """Shared tool advanced search query interface"""

    query = TextLine(title=_("Search text"),
                     description=_("Entered text will be search in title only"),
                     required=False)

    owner = PrincipalField(title=_("Owner"),
                           required=False)

    status = Choice(title=_("Status"),
                    vocabulary=SHARED_TOOL_WORKFLOW_STATES_VOCABULARY,
                    required=False)

    data_type = Choice(title=_("Data type"),
                       vocabulary=DATA_TYPES_VOCABULARY,
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


class SharedToolAdvancedSearchForm(SearchForm):
    """Shared tool advanced search form"""

    title = _("Contents search form")

    ajax_form_handler = 'advanced-search-results.html'
    _edit_permission = VIEW_SYSTEM_PERMISSION


@adapter_config(required=(Interface, IAdminLayer, SharedToolAdvancedSearchForm),
                provides=IFormFields)
def shared_tool_advanced_search_form_fields(context, request, form):
    """Shared tool advanced search form fields getter"""
    return Fields(ISharedToolAdvancedSearchQuery).omit('tags', 'themes', 'collections')


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
        fields = Fields(ISharedToolAdvancedSearchQuery).select(self.fieldname)
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
                required=(IBaseSharedTool, IAdminLayer, SharedToolAdvancedSearchForm),
                provides=IGroup)
class SharedToolAdvancedSearchFormTagsGroup(BaseThesaurusTermsSearchGroup):
    """Shared tool advanced search form tags group"""

    legend = _("Tags")

    fieldname = 'tags'
    manager = ITagsManager

    weight = 10


@adapter_config(name='themes',
                required=(IBaseSharedTool, IAdminLayer, SharedToolAdvancedSearchForm),
                provides=IGroup)
class SharedToolAdvancedSearchFormThemesGroup(BaseThesaurusTermsSearchGroup):
    """Shared tool advanced search form themes group"""

    legend = _("Themes")

    fieldname = 'themes'
    manager = IThemesManager

    weight = 20


@adapter_config(name='collections',
                required=(IBaseSharedTool, IAdminLayer, SharedToolAdvancedSearchForm),
                provides=IGroup)
class SharedToolAdvancedSearchFormCollectionsGroup(BaseThesaurusTermsSearchGroup):
    """Shared tool advanced search form collections group"""

    legend = _("Collections")

    fieldname = 'collections'
    manager = ICollectionsManager

    weight = 30


@pagelet_config(name='advanced-search.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolAdvancedSearchView(SearchView):
    """Shared tool advanced search view"""

    title = _("Contents search form")
    header_label = _("Advanced search")
    search_form = SharedToolAdvancedSearchForm


class SharedToolAdvancedSearchResultsTable(DashboardTable):
    """Shared tool advanced search results table"""


@adapter_config(required=(IBaseSharedTool, IPyAMSLayer, SharedToolAdvancedSearchResultsTable),
                provides=IValues)
class SharedToolAdvancedSearchResultsValues(ContextRequestViewAdapter):
    """Shared tool advanced search results values"""

    def get_params(self, data):
        """Extract catalog query params from incoming request"""
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(self.context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()))
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
        if data.get('status'):
            params &= Eq(catalog['workflow_state'], data['status'])
        if data.get('data_type'):
            params &= Eq(catalog['data_type'], data['data_type'])
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
        form = SharedToolAdvancedSearchForm(self.context, self.request)
        form.update()
        data, _errors = form.extract_data()
        params = self.get_params(data)
        catalog = get_utility(ICatalog)
        if data.get('status'):
            yield from unique_iter(
                map(lambda x: sorted(IWorkflowVersions(x).get_versions(data['status']),
                                     key=lambda y: IZopeDublinCore(y).modified)[0],
                    CatalogResultSet(CatalogQuery(catalog).query(
                        params, sort_index='modified_date', reverse=True))))
        else:
            yield from unique_iter(
                map(get_last_version,
                    CatalogResultSet(CatalogQuery(catalog).query(
                        params, sort_index='modified_date', reverse=True))))


@pagelet_config(name='advanced-search-results.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION, xhr=True)
class SharedToolAdvancedSearchResultsView(SearchResultsView):
    """Shared tool advanced search results view"""

    table_label = _("Search results")
    table_class = SharedToolAdvancedSearchResultsTable


@viewlet_config(name='pyams.content_header',
                layer=IAdminLayer, view=SharedToolAdvancedSearchResultsView,
                manager=IHeaderViewletManager, weight=10)
class AdvancedSearchResultsViewHeaderViewlet(EmptyViewlet):
    """Advanced search results view header viewlet"""

    def render(self):
        return '<h1 class="mt-3"></h1>'
