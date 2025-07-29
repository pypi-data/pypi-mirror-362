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

"""PyAMS_content.root.zmi.dashboard module

This module defines management components for site root dashboard.
"""

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Any, Eq, Or
from pyramid.decorator import reify
from pyramid.interfaces import IView
from zope.interface import Interface, implementer
from zope.intid import IIntIds
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_catalog.query import CatalogResultSet
from pyams_content.shared.common import IBaseSharedTool, SHARED_CONTENT_TYPES_VOCABULARY
from pyams_content.shared.common.zmi.dashboard import BaseSharedToolDashboardSingleView, \
    DashboardTable, BaseSharedToolDashboardView, SharedToolAllInterventionsMenu, \
    SharedToolArchivedContentsMenu, SharedToolArchivedContentsView, \
    SharedToolDashboardManagerWaitingValues, SharedToolDashboardManagerWaitingView, \
    SharedToolDashboardMenu, SharedToolDashboardOwnerModifiedView, \
    SharedToolDashboardOwnerWaitingView, SharedToolLastModificationsView, \
    SharedToolLastModifiedMenu, SharedToolLastPublicationsMenu, SharedToolLastPublicationsView, \
    SharedToolMissingContentWarning, SharedToolMyDashboardMenu, SharedToolPreparationsMenu, \
    SharedToolPreparationsView, SharedToolPublicationsMenu, SharedToolPublicationsView, \
    SharedToolRetiredContentsMenu, SharedToolRetiredContentsView, SharedToolSubmissionsMenu, \
    SharedToolSubmissionsView
from pyams_content.zmi.dashboard import DashboardContentTypeColumn
from pyams_content.zmi.interfaces import IAllDashboardMenu, IDashboardTable, IMyDashboardMenu, \
    ISiteRootDashboardContentType
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.list import unique_iter
from pyams_utils.registry import get_all_utilities_registered_for, get_utility
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflow
from pyams_workflow.versions import get_last_version_in_state
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IInnerTable
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader
from pyams_zmi.table import MultipleTablesAdminView


__docformat__ = 'restructuredtext'

from pyams_content import _


class BaseSiteRootDashboardTable(DashboardTable):
    """Base site root dashboard table"""


class BaseSiteRootDashboardView(BaseSharedToolDashboardView):
    """Base site root dashboard view"""


class BaseSiteRootDashboardSingleView(BaseSharedToolDashboardSingleView):
    """Base site root dashboard view with single table"""


@adapter_config(name='content-type',
                required=(ISiteRoot, IAdminLayer, IDashboardTable),
                provides=IColumn)
class SiteRootContentTypeColumn(DashboardContentTypeColumn):
    """Site root dashboard content type column"""

    i18n_header = _("Content type")
    interface = ISiteRootDashboardContentType


#
# Main shared tool dashboard
#

@adapter_config(required=(ISiteRoot, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def site_root_menu_header(context, request, view, menu):
    """Site root menu header"""
    return request.localizer.translate(_("Users activity"))


@viewlet_config(name='dashboard.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IContentManagementMenu, weight=5,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootDashboardMenu(SharedToolDashboardMenu):
    """Site root dashboard menu"""


@pagelet_config(name='dashboard.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootDashboardView(MultipleTablesAdminView):
    """Site root dashboard view"""

    header_label = _("My dashboard")
    table_label = _("My dashboard")


@adapter_config(name='no-content-warning',
                required=(ISiteRoot, IAdminLayer, SiteRootDashboardView),
                provides=IInnerTable, force_implements=False)
class SiteRootMissingContentWarning(SharedToolMissingContentWarning):
    """Site root missing content warning"""


#
# Manager waiting contents
#

class SiteRootDashboardManagerWaitingTable(BaseSiteRootDashboardTable):
    """Site root dashboard manager waiting table"""

    @reify
    def id(self):
        return f'{super().id}_waiting'


@adapter_config(name='manager-waiting',
                required=(ISiteRoot, IAdminLayer, SiteRootDashboardView),
                provides=IInnerTable)
class SiteRootDashboardManagerWaitingView(SharedToolDashboardManagerWaitingView):
    """Site root dashboard manager waiting view"""

    table_class = SiteRootDashboardManagerWaitingTable


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootDashboardManagerWaitingTable),
                provides=IValues)
class SiteRootDashboardManagerWaitingValues(SharedToolDashboardManagerWaitingValues):
    """Site root dashboard waiting values adapter"""

    @property
    def values(self):
        """Table values getter"""
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            workflow = IWorkflow(tool)
            query = And(Eq(catalog['parents'], intids.register(tool)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Any(catalog['workflow_state'], workflow.waiting_states))
            params = params | query if params else query
        yield from filter(
            self.check_access,
            unique_iter(
                map(get_last_version_in_state,
                    CatalogResultSet(CatalogQuery(catalog).query(params,
                                                                 sort_index='modified_date')))))


#
# Last owned contents waiting for action
#

class SiteRootDashboardOwnerWaitingTable(BaseSiteRootDashboardTable):
    """Table of owned contents waiting for action"""

    @reify
    def id(self):
        return f'{super().id}_owner_waiting'


@adapter_config(name='owner-waiting',
                required=(ISiteRoot, IAdminLayer, SiteRootDashboardView),
                provides=IInnerTable)
class SiteRootDashboardOwnerWaitingView(SharedToolDashboardOwnerWaitingView):
    """View of owned contents waiting for action"""

    table_class = SiteRootDashboardOwnerWaitingTable


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootDashboardOwnerWaitingTable),
                provides=IValues)
class SiteRootDashboardOwnerWaitingValues(ContextRequestViewAdapter):
    """Site root dashboard waiting owned contents values adapter"""

    @property
    def values(self):
        """Table values getter"""
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            workflow = IWorkflow(tool)
            query = And(Eq(catalog['parents'], intids.register(tool)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Any(catalog['workflow_state'], workflow.waiting_states),
                        Eq(catalog['workflow_principal'], principal_id))
            params = params | query if params else query
        yield from unique_iter(
            map(get_last_version_in_state,
                CatalogResultSet(CatalogQuery(catalog).query(params,
                                                             sort_index='modified_date'))))


#
# Last owner modified contents
#

class SiteRootDashboardOwnerModifiedTable(BaseSiteRootDashboardTable):
    """Site root dashboard owner modified table"""

    @reify
    def id(self):
        return f'{super().id}_modified'


@adapter_config(name='owner-modified',
                required=(ISiteRoot, IAdminLayer, SiteRootDashboardView),
                provides=IInnerTable)
class SiteRootDashboardOwnerModifiedView(SharedToolDashboardOwnerModifiedView):
    """Site root dashboard owner modified view"""

    table_class = SiteRootDashboardOwnerModifiedTable


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootDashboardOwnerModifiedTable),
                provides=IValues)
class SiteRootDashboardOwnerModifiedValues(ContextRequestViewAdapter):
    """Site root dashboard owner modified adapter"""

    @property
    def values(self):
        """Table values getter"""
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            query = And(Eq(catalog['parents'], intids.register(tool)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Or(Eq(catalog['role:owner'], principal_id),
                           Eq(catalog['role:contributor'], principal_id)))
            params = params | query if params else query
        yield from unique_iter(
            map(get_last_version_in_state,
                CatalogResultSet(CatalogQuery(catalog).query(params,
                                                             limit=50,
                                                             sort_index='modified_date',
                                                             reverse=True))))


#
# All my contents menu
#

@viewletmanager_config(name='my-contents.menu',
                       context=ISiteRoot, layer=IAdminLayer,
                       manager=IContentManagementMenu, weight=10,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IMyDashboardMenu)
class SiteRootMyDashboardMenu(SharedToolMyDashboardMenu):
    """Site root 'my contents' dashboard menu"""


#
# My preparations
# Dashboard of owned and modified contents which can be updated
#

@viewlet_config(name='my-preparations.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=5,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootPreparationsMenu(SharedToolPreparationsMenu):
    """Site root preparations dashboard menu"""


@implementer(IView)
class SiteRootPreparationsTable(BaseSiteRootDashboardTable):
    """Site root preparations table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootPreparationsTable),
                provides=IValues)
class SiteRootPreparationsValues(ContextRequestViewAdapter):
    """Site root preparations values adapter"""

    @property
    def values(self):
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            workflow = IWorkflow(tool)
            query = And(Eq(catalog['parents'], intids.register(self.context)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Or(Eq(catalog['role:owner'], principal_id),
                           Eq(catalog['role:contributor'], principal_id)),
                        Eq(catalog['workflow_state'], workflow.initial_state))
            params = params | query if params else query
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-preparations.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootPreparationsView(SharedToolPreparationsView):
    """Site root preparations view"""

    table_class = SiteRootPreparationsTable


#
# My submissions
# Dashboard of contents waiting for manager action
#

@viewlet_config(name='my-submissions.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=10,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootSubmissionsMenu(SharedToolSubmissionsMenu):
    """Site root submissions dashboard menu"""


@implementer(IView)
class SiteRootSubmissionsTable(BaseSiteRootDashboardTable):
    """Site root submissions table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootSubmissionsTable),
                provides=IValues)
class SiteRootSubmissionsValues(ContextRequestViewAdapter):
    """Site root submissions values adapter"""

    @property
    def values(self):
        context = self.context
        principal_id = self.request.principal.id
        intids  =get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            workflow = IWorkflow(tool)
            query = And(Eq(catalog['parents'], intids.register(context)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Or(Eq(catalog['role:owner'], principal_id),
                           Eq(catalog['role:contributor'], principal_id)),
                        Any(catalog['workflow_state'], workflow.waiting_states))
            params = params | query if params else query
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-submissions.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootSubmissionsView(SharedToolSubmissionsView):
    """Site root submissions view"""

    table_class = SiteRootSubmissionsTable


#
# My publications
# Dashboard of published contents
#

@viewlet_config(name='my-publications.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=15,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootPublicationsMenu(SharedToolPublicationsMenu):
    """Site root publication dashboard menu"""


@implementer(IView)
class SiteRootPublicationsTable(BaseSiteRootDashboardTable):
    """Site root publications table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootPublicationsTable),
                provides=IValues)
class SiteRootPublicationsValues(ContextRequestViewAdapter):
    """Site root publications values adapter"""

    @property
    def values(self):
        context = self.context
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            workflow = IWorkflow(tool)
            query = And(Eq(catalog['parents'], intids.register(self.context)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Or(Eq(catalog['role:owner'], principal_id),
                           Eq(catalog['role:contributor'], principal_id)),
                        Any(catalog['workflow_state'], workflow.published_states))
            params = params | query if params else query
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-publications.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootPublicationsView(SharedToolPublicationsView):
    """Site root publications view"""

    table_class = SiteRootPublicationsTable


#
# My retired contents
# Dashboard of retired contents
#

@viewlet_config(name='my-retired-contents.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=20,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootRetiredContentsMenu(SharedToolRetiredContentsMenu):
    """Site root retired contents dashboard menu"""


@implementer(IView)
class SiteRootRetiredContentsTable(BaseSiteRootDashboardTable):
    """Site root retired contents table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootRetiredContentsTable),
                provides=IValues)
class SiteRootRetiredContentsValues(ContextRequestViewAdapter):
    """Site root retired contents values adapter"""

    @property
    def values(self):
        context = self.context
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            workflow = IWorkflow(tool)
            query = And(Eq(catalog['parents'], intids.register(context)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Or(Eq(catalog['role:owner'], principal_id),
                           Eq(catalog['role:contributor'], principal_id)),
                        Any(catalog['workflow_state'], workflow.retired_states))
            params = params | query if params else query
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-retired-contents.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootRetiredContentsView(SharedToolRetiredContentsView):
    """Site root retired contents view"""

    table_class = SiteRootRetiredContentsTable


#
# My archived contents
# Dashboard of archived contents
#

@viewlet_config(name='my-archived-contents.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=25,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootArchivedContentsMenu(SharedToolArchivedContentsMenu):
    """Site root archived contents dashboard menu"""


@implementer(IView)
class SiteRootArchivedContentsTable(BaseSiteRootDashboardTable):
    """Site root archived contents table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootArchivedContentsTable),
                provides=IValues)
class SiteRootArchivedContentsValues(ContextRequestViewAdapter):
    """Site root archived contents values adapter"""

    @property
    def values(self):
        context = self.context
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            workflow = IWorkflow(tool)
            query = And(Eq(catalog['parents'], intids.register(context)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Or(Eq(catalog['role:owner'], principal_id),
                           Eq(catalog['role:contributor'], principal_id)),
                        Any(catalog['workflow_state'], workflow.archived_states))
            params = params | query if params else query
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-archived-contents.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootArchivedContentsView(SharedToolArchivedContentsView):
    """Site root archived contents view"""

    table_class = SiteRootArchivedContentsTable


#
# All interventions menu
#

@viewletmanager_config(name='my-interventions.menu',
                       context=ISiteRoot, layer=IAdminLayer,
                       manager=IContentManagementMenu, weight=20,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IAllDashboardMenu)
class SiteRootAllInterventionsMenu(SharedToolAllInterventionsMenu):
    """Site root 'all interventions' dashboard menu"""


#
# Last published contents
#

@viewlet_config(name='last-published.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IAllDashboardMenu, weight=25,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootLastPublicationsMenu(SharedToolLastPublicationsMenu):
    """Site root modified contents dashboard menu"""


@implementer(IView)
class SiteRootLastPublicationsTable(BaseSiteRootDashboardTable):
    """Site root dashboard last publications table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootLastPublicationsTable),
                provides=IValues)
class SiteRootLastPublicationsValues(ContextRequestViewAdapter):
    """Site root publications values adapter"""

    @property
    def values(self):
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = None
        for tool in get_all_utilities_registered_for(IBaseSharedTool):
            workflow = IWorkflow(tool)
            query = And(Eq(catalog['parents'], intids.register(self.context)),
                        Any(catalog['content_type'], vocabulary.by_value.keys()),
                        Any(catalog['workflow_state'], workflow.published_states))
            params = params | query if params else query
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         limit=50,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='last-published.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootLastPublicationsView(SharedToolLastPublicationsView):
    """Site root last publications view"""

    table_class = SiteRootLastPublicationsTable


#
# Last modified contents
#

@viewlet_config(name='last-modified.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=IAllDashboardMenu, weight=30,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootLastModifiedMenu(SharedToolLastModifiedMenu):
    """Site root modified contents dashboard menu"""


@implementer(IView)
class SiteRootLastModificationsTable(BaseSiteRootDashboardTable):
    """Site root dashboard last modifications table"""


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootLastModificationsTable),
                provides=IValues)
class SiteRootLastModificationsValues(ContextRequestViewAdapter):
    """Site root modifications values adapter"""

    @property
    def values(self):
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = Any(catalog['content_type'], vocabulary.by_value.keys())
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         limit=50,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='last-modified.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootLastModificationsView(SharedToolLastModificationsView):
    """Site root last modifications view"""

    table_class = SiteRootLastModificationsTable
