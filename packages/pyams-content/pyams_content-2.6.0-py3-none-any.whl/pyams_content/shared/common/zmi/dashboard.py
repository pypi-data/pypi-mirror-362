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

"""PyAMS_content.shared.common.zmi.dashboard module

This module provides dashboard management components which are common to all
shared contents.
"""

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Any, Eq, Or
from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.interfaces import IView
from zope.annotation import IAttributeAnnotatable
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface, implementer
from zope.intid import IIntIds
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_catalog.query import CatalogResultSet
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION, PUBLISH_CONTENT_PERMISSION
from pyams_content.shared.common.interfaces import IBaseSharedTool, IManagerRestrictions, ISharedContent, \
    IWfSharedContentRoles, SHARED_CONTENT_TYPES_VOCABULARY
from pyams_content.shared.common.zmi.content import shared_content_version_getter
from pyams_content.zmi.interfaces import IAllDashboardMenu, IDashboardColumn, \
    IDashboardContentModifier, IDashboardContentNumber, IDashboardContentOwner, \
    IDashboardContentStatus, IDashboardContentStatusDatetime, IDashboardContentTimestamp, \
    IDashboardContentVersion, IDashboardTable, IDashboardView, IMyDashboardMenu
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.utility import get_principal
from pyams_sequence.interfaces import ISequentialIdInfo, ISequentialIdTarget, ISequentialIntIds
from pyams_skin.viewlet.help import AlertMessage
from pyams_table.interfaces import ITableRowUpdatedEvent, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.date import SH_DATETIME_FORMAT, format_datetime
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.list import boolean_iter, unique_iter
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import ViewContentProvider, viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, \
    IWorkflowPublicationSupport, IWorkflowState, IWorkflowVersions
from pyams_workflow.versions import get_last_version_in_state
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IInnerTable, ITableWithActions
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IMenuHeader
from pyams_zmi.table import InnerTableAdminView, MultipleTablesAdminView, Table, TableAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@subscriber(ITableRowUpdatedEvent,
            context_selector=IDashboardTable,
            row_context_selector=ISharedContent)
def handle_shared_content_table_row_update(event):
    """Shared content table row update event handler"""
    item_key = ICacheKeyValue(event.item)
    versions = IWorkflowVersions(event.context, None)
    if versions is not None:
        event.object.rows_state[item_key] = versions.get_last_versions()[-1]


@adapter_config(required=(ISequentialIdTarget, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentNumber)
def sequence_target_number(context, request, column):
    """Sequence target number getter"""
    sequence_info = ISequentialIdInfo(context, None)
    if sequence_info is not None:
        sequence = get_utility(ISequentialIntIds, name=context.sequence_name)
        return sequence.get_base_oid(sequence_info.oid, context.sequence_prefix)
    return None


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentStatus)
def content_workflow_status(context, request, column):
    """Content workflow status getter"""
    state = IWorkflowState(context, None)
    if state is not None:
        workflow = IWorkflow(context)
        result = request.localizer.translate(workflow.get_state_label(state.state))
        if state.state in workflow.waiting_states:
            if state.state_urgency:
                result += ' <i class="fas fa-fw fa-exclamation-triangle text-danger"></i>'
        elif state.state in workflow.published_states:
            pub_info = IWorkflowPublicationInfo(context, None)
            if (pub_info is not None) and not pub_info.is_published():
                translate = request.localizer.translate
                result += ' <i class="fas fa-fw fa-hourglass-half opacity-75 hint align-base" ' \
                          '    data-offset="5" title="{}"></i>'.format(
                    translate(_("Content publication start date is not passed yet")))
        return result
    return None


@adapter_config(required=(ISharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentStatus)
def shared_content_workflow_status(context, request, view):
    """Shared content workflow status getter"""
    return shared_content_version_getter(context, request, view, IDashboardContentStatus)


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentStatusDatetime)
def content_workflow_status_datetime(context, request, column):
    """Content workflow status datetime getter"""
    state = IWorkflowState(context, None)
    if state is not None:
        return format_datetime(state.state_date, SH_DATETIME_FORMAT,
                               request=request)
    return None


@adapter_config(required=(ISharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentStatusDatetime)
def shared_content_workflow_status_datetime(context, request, view):
    """Shared content workflow status datetime getter"""
    return shared_content_version_getter(context, request, view, IDashboardContentStatusDatetime)


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentVersion)
def content_workflow_version(context, request, column):
    """Content workflow version getter"""
    state = IWorkflowState(context, None)
    if state is not None:
        return str(state.version_id)
    return None


@adapter_config(required=(ISharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentVersion)
def shared_content_workflow_version(context, request, view):
    """Shared content workflow version getter"""
    return shared_content_version_getter(context, request, view, IDashboardContentVersion)


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentModifier)
def content_workflow_status_principal(context, request, column):
    """Content workflow status principal getter"""
    state = IWorkflowState(context, None)
    if state is not None:
        manager = get_utility(ISecurityManager)
        return manager.get_principal(state.state_principal).title
    return None


@adapter_config(required=(ISharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentModifier)
def shared_content_workflow_status_principal(context, request, view):
    """Shared content workflow status principal getter"""
    return shared_content_version_getter(context, request, view, IDashboardContentModifier)


@adapter_config(required=(IWorkflowPublicationSupport, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentOwner)
def content_workflow_owner(context, request, column):
    """Content workflow owner getter"""
    try:
        owner = IWfSharedContentRoles(context).owner
    except (TypeError, AttributeError):
        return None
    if owner:
        return get_principal(request, next(iter(owner))).title
    return None


@adapter_config(required=(ISharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentOwner)
def shared_content_workflow_owner(context, request, view):
    """Shared content workflow owner getter"""
    return shared_content_version_getter(context, request, view, IDashboardContentOwner)


@adapter_config(required=(IAttributeAnnotatable, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentTimestamp)
def content_timestamp(context, request, column):
    """Content timestamp getter"""
    dc = IZopeDublinCore(context, None)
    if dc is not None:
        return format_datetime(tztime(dc.modified), SH_DATETIME_FORMAT,
                               request=request)
    return None


@adapter_config(required=(ISharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentTimestamp)
def shared_content_timestamp(context, request, view):
    """Shared content timestamp getter"""
    return shared_content_version_getter(context, request, view, IDashboardContentTimestamp)


#
# Base shared tool dashboard components
#

class BaseDashboardTable(Table):
    """Base dashboard table"""

    @property
    def sort_index(self):
        return len(self.columns) - 1

    sort_order = 'desc'

    @reify
    def values(self):
        return list(super().values)

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        attributes.setdefault('table', {}).update({
            'data-ams-order': f'{self.sort_index},{self.sort_order}'
        })
        return attributes


@implementer(IDashboardTable)
class DashboardTable(BaseDashboardTable):
    """Dashboard table"""


@implementer(ITableWithActions)
class DashboardTableWithActions(DashboardTable):
    """Dashboard table with actions"""


@implementer(IDashboardView)
class SharedToolDashboardViewMixin:
    """Shared tool dashboard mixin view"""

    empty_label = None
    single_label = None
    plural_label = None

    @property
    def table_label(self):
        translate = self.request.localizer.translate
        length = len(self.table.values)
        if length == 0:
            return translate(self.empty_label)
        if length == 1:
            return translate(self.single_label)
        return translate(self.plural_label).format(length)


class BaseSharedToolDashboardView(SharedToolDashboardViewMixin, InnerTableAdminView,
                                  ViewContentProvider):
    """Base shared tool dashboard view with multiple tables"""

    hide_section = True

    def render(self):
        if not self.table.values:
            return ''
        return super().render()


class BaseSharedToolDashboardSingleView(SharedToolDashboardViewMixin, TableAdminView):
    """Base shared tool dashboard view with single table"""


#
# Main shared tool dashboard
#

@adapter_config(required=(IBaseSharedTool, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def shared_tool_menu_header(context, request, view, menu):
    """Shared tool menu header"""
    return request.localizer.translate(_("Users activity"))


@viewlet_config(name='dashboard.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IContentManagementMenu, weight=5,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolDashboardMenu(NavigationMenuItem):
    """Shared tool dashboard menu"""

    label = _("Dashboard")
    icon_class = 'fas fa-chart-line'
    href = '#dashboard.html'


@pagelet_config(name='dashboard.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolDashboardView(MultipleTablesAdminView):
    """Shared tool dashboard view"""

    header_label = _("My dashboard")
    table_label = _("My dashboard")


@adapter_config(name='no-content-warning',
                required=(IBaseSharedTool, IAdminLayer, SharedToolDashboardView),
                provides=IInnerTable, force_implements=False)
class SharedToolMissingContentWarning(AlertMessage):
    """Shared tool missing content warning"""

    def __init__(self, context, request, view):
        super().__init__(context, request, view, None)

    _message = _("You are not actually concerned by any content.")

    def render(self):
        for view in self.view.tables:
            if not IInnerTable.providedBy(view):
                continue
            has_values, _values = boolean_iter(view.table.values)
            if has_values:
                return ''
        return super().render()

    weight = 999


#
# Manager waiting contents
#

class SharedToolDashboardManagerWaitingTable(DashboardTable):
    """Shared tool dashboard manager waiting table"""

    @reify
    def id(self):
        return f'{super().id}_waiting'


@adapter_config(name='manager-waiting',
                required=(IBaseSharedTool, IAdminLayer, SharedToolDashboardView),
                provides=IInnerTable)
class SharedToolDashboardManagerWaitingView(BaseSharedToolDashboardView):
    """Shared tool dashboard manager waiting view"""

    table_class = SharedToolDashboardManagerWaitingTable

    empty_label = _("MANAGER - No content waiting for your action")
    single_label = _("MANAGER - 1 content waiting for your action")
    plural_label = _("MANAGER - {} contents waiting for your action")

    weight = 20


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolDashboardManagerWaitingTable),
                provides=IValues)
class SharedToolDashboardManagerWaitingValues(ContextRequestViewAdapter):
    """Shared tool dashboard waiting values getter"""

    @property
    def values(self):
        """Table values getter"""
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        workflow = IWorkflow(self.context)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(self.context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()),
                     Any(catalog['workflow_state'], workflow.waiting_states))
        yield from filter(
            self.check_access,
            unique_iter(
                map(get_last_version_in_state,
                    CatalogResultSet(CatalogQuery(catalog).query(params,
                                                                 sort_index='modified_date')))))

    def check_access(self, content):
        """Content access checker"""
        if self.request.has_permission(MANAGE_SITE_ROOT_PERMISSION, context=content):
            return True
        roles = IWfSharedContentRoles(content)
        if self.request.principal.id in roles.managers:
            return True
        restrictions = IManagerRestrictions(content, None)
        if restrictions is not None:
            return restrictions.can_access(content, PUBLISH_CONTENT_PERMISSION, self.request)
        return False


#
# Last owned contents waiting for action
#

class SharedToolDashboardOwnerWaitingTable(DashboardTable):
    """Table of owned contents waiting for action"""

    @reify
    def id(self):
        return f'{super().id}_owner_waiting'


@adapter_config(name='owner-waiting',
                required=(IBaseSharedTool, IAdminLayer, SharedToolDashboardView),
                provides=IInnerTable)
class SharedToolDashboardOwnerWaitingView(BaseSharedToolDashboardView):
    """View of owned contents waiting for action"""

    table_class = SharedToolDashboardOwnerWaitingTable

    empty_label = _("CONTRIBUTOR - 0 content waiting for action")
    single_label = _("CONTRIBUTOR - 1 content waiting for action")
    plural_label = _("CONTRIBUTOR - {0} contents waiting for action")

    weight = 30


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolDashboardOwnerWaitingTable),
                provides=IValues)
class SharedToolDashboardOwnerWaitingValues(ContextRequestViewAdapter):
    """Shared tool dashboard waiting owned contents values adapter"""

    @property
    def values(self):
        """Table values getter"""
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        workflow = IWorkflow(self.context)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(self.context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()),
                     Any(catalog['workflow_state'], workflow.waiting_states),
                     Eq(catalog['workflow_principal'], self.request.principal.id))
        yield from unique_iter(
            map(get_last_version_in_state,
                CatalogResultSet(CatalogQuery(catalog).query(params,
                                                             sort_index='modified_date'))))


#
# Last owner modified contents
#

class SharedToolDashboardOwnerModifiedTable(DashboardTable):
    """Shared tool dashboard owner modified table"""

    @reify
    def id(self):
        return f'{super().id}_modified'


@adapter_config(name='owner-modified',
                required=(IBaseSharedTool, IAdminLayer, SharedToolDashboardView),
                provides=IInnerTable)
class SharedToolDashboardOwnerModifiedView(BaseSharedToolDashboardView):
    """Shared tool dashboard owner modified view"""

    table_class = SharedToolDashboardOwnerModifiedTable

    empty_label = _("CONTRIBUTOR - 0 modified content")
    single_label = _("CONTRIBUTOR - 1 modified content")

    @property
    def plural_label(self):
        length = len(self.table.values)
        if length > 50:
            return _("CONTRIBUTOR - Last {} modified contents")
        return _("CONTRIBUTOR - {} modified contents")

    weight = 40


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolDashboardOwnerModifiedTable),
                provides=IValues)
class SharedToolDashboardOwnerModifiedValues(ContextRequestViewAdapter):
    """Shared tool dashboard owner modified adapter"""

    @property
    def values(self):
        """Table values getter"""
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(self.context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()),
                     Or(Eq(catalog['role:owner'], principal_id),
                        Eq(catalog['role:contributor'], principal_id)))
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
                       context=IBaseSharedTool, layer=IAdminLayer,
                       manager=IContentManagementMenu, weight=10,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IMyDashboardMenu)
class SharedToolMyDashboardMenu(NavigationMenuItem):
    """Shared tool 'my contents' dashboard menu"""

    label = _("My contents")
    icon_class = 'fas fa-user'
    href = '#'


#
# My preparations
# Dashboard of owned and modified contents which can be updated
#

@viewlet_config(name='my-preparations.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=5,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolPreparationsMenu(NavigationMenuItem):
    """Shared tool preparations dashboard menu"""

    label = _("My drafts")
    href = '#my-preparations.html'


@implementer(IView)
class SharedToolPreparationsTable(DashboardTable):
    """Shared tool preparations table"""


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolPreparationsTable),
                provides=IValues)
class SharedToolPreparationsValues(ContextRequestViewAdapter):
    """Shared tool preparations values adapter"""

    @property
    def values(self):
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        workflow = IWorkflow(self.context)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(self.context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()),
                     Or(Eq(catalog['role:owner'], principal_id),
                        Eq(catalog['role:contributor'], principal_id)),
                     Eq(catalog['workflow_state'], workflow.initial_state))
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-preparations.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolPreparationsView(BaseSharedToolDashboardSingleView):
    """Shared tool preparations view"""

    header_label = _("My drafts")
    table_class = SharedToolPreparationsTable

    empty_label = _("CONTRIBUTOR - 0 content in preparation")
    single_label = _("CONTRIBUTOR - 1 content in preparation")
    plural_label = _("CONTRIBUTOR - {} contents in preparation")


#
# My submissions
# Dashboard of contents waiting for manager action
#

@viewlet_config(name='my-submissions.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=10,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolSubmissionsMenu(NavigationMenuItem):
    """Shared tool submissions dashboard menu"""

    label = _("My submissions")
    href = '#my-submissions.html'


@implementer(IView)
class SharedToolSubmissionsTable(DashboardTable):
    """Shared tool submissions table"""


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolSubmissionsTable),
                provides=IValues)
class SharedToolSubmissionsValues(ContextRequestViewAdapter):
    """Shared tool submissions values adapter"""

    @property
    def values(self):
        context = self.context
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        workflow = IWorkflow(context)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()),
                     Or(Eq(catalog['role:owner'], principal_id),
                        Eq(catalog['role:contributor'], principal_id)),
                     Any(catalog['workflow_state'], workflow.waiting_states))
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-submissions.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolSubmissionsView(BaseSharedToolDashboardSingleView):
    """Shared tool submissions view"""

    header_label = _("My submissions")
    table_class = SharedToolSubmissionsTable

    empty_label = _("CONTRIBUTOR - 0 submitted content")
    single_label = _("CONTRIBUTOR - 1 submitted content")
    plural_label = _("CONTRIBUTOR - {} submitted contents")


#
# My publications
# Dashboard of published contents
#

@viewlet_config(name='my-publications.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=15,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolPublicationsMenu(NavigationMenuItem):
    """Shared tool publications dashboard menu"""

    label = _("My publications")
    href = '#my-publications.html'


@implementer(IView)
class SharedToolPublicationsTable(DashboardTable):
    """Shared tool publications table"""


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolPublicationsTable),
                provides=IValues)
class SharedToolPublicationsValues(ContextRequestViewAdapter):
    """Shared tool publications values adapter"""

    @property
    def values(self):
        context = self.context
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        workflow = get_utility(IWorkflow, name=context.shared_content_workflow)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()) &
                     Or(Eq(catalog['role:owner'], principal_id),
                        Eq(catalog['role:contributor'], principal_id)),
                     Any(catalog['workflow_state'], workflow.published_states))
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-publications.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolPublicationsView(BaseSharedToolDashboardSingleView):
    """Shared tool publications view"""

    header_label = _("My publications")
    table_class = SharedToolPublicationsTable

    empty_label = _("CONTRIBUTOR - 0 published content")
    single_label = _("CONTRIBUTOR - 1 published content")
    plural_label = _("CONTRIBUTOR - {} published contents")


#
# My retired contents
# Dashboard of retired contents
#

@viewlet_config(name='my-retired-contents.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=20,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolRetiredContentsMenu(NavigationMenuItem):
    """Shared tool retired contents dashboard menu"""

    label = _("My retired contents")
    href = '#my-retired-contents.html'


@implementer(IView)
class SharedToolRetiredContentsTable(DashboardTable):
    """Shared tool retired contents table"""


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolRetiredContentsTable),
                provides=IValues)
class SharedToolRetiredContentsValues(ContextRequestViewAdapter):
    """Shared tool retired contents values adapter"""

    @property
    def values(self):
        context = self.context
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        workflow = get_utility(IWorkflow, name=context.shared_content_workflow)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()) &
                     Or(Eq(catalog['role:owner'], principal_id),
                        Eq(catalog['role:contributor'], principal_id)),
                     Any(catalog['workflow_state'], workflow.retired_states))
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-retired-contents.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolRetiredContentsView(BaseSharedToolDashboardSingleView):
    """Shared tool retired contents view"""

    header_label = _("My retired contents")
    table_class = SharedToolRetiredContentsTable

    empty_label = _("CONTRIBUTOR - 0 retired content")
    single_label = _("CONTRIBUTOR - 1 retired content")
    plural_label = _("CONTRIBUTOR - {} retired contents")


#
# My archived contents
# Dashboard of archived contents
#

@viewlet_config(name='my-archived-contents.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IMyDashboardMenu, weight=25,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolArchivedContentsMenu(NavigationMenuItem):
    """Shared tool archived contents dashboard menu"""

    label = _("My archived contents")
    href = '#my-archived-contents.html'


@implementer(IView)
class SharedToolArchivedContentsTable(DashboardTable):
    """Shared tool archived contents table"""


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolArchivedContentsTable),
                provides=IValues)
class SharedToolArchivedContentsValues(ContextRequestViewAdapter):
    """Shared tool archived contents values adapter"""

    @property
    def values(self):
        context = self.context
        principal_id = self.request.principal.id
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        workflow = get_utility(IWorkflow, name=context.shared_content_workflow)
        vocabulary = getVocabularyRegistry().get(context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()) &
                     Or(Eq(catalog['role:owner'], principal_id),
                        Eq(catalog['role:contributor'], principal_id)),
                     Any(catalog['workflow_state'], workflow.archived_states))
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='my-archived-contents.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolArchivedContentsView(BaseSharedToolDashboardSingleView):
    """Shared tool archived contents view"""

    header_label = _("My archived contents")
    table_class = SharedToolArchivedContentsTable

    empty_label = _("CONTRIBUTOR - 0 archived content")
    single_label = _("CONTRIBUTOR - 1 archived content")
    plural_label = _("CONTRIBUTOR - {} archived contents")


#
# All interventions menu
#

@viewletmanager_config(name='all-interventions.menu',
                       context=IBaseSharedTool, layer=IAdminLayer,
                       manager=IContentManagementMenu, weight=20,
                       permission=VIEW_SYSTEM_PERMISSION,
                       provides=IAllDashboardMenu)
class SharedToolAllInterventionsMenu(NavigationMenuItem):
    """Shared tool 'all interventions' dashboard menu"""

    label = _("All interventions")
    css_class = 'open'
    icon_class = 'fas fa-pen-square'
    href = '#'


#
# Last published contents
#

@viewlet_config(name='last-published.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IAllDashboardMenu, weight=25,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolLastPublicationsMenu(NavigationMenuItem):
    """Shared tool modified contents dashboard menu"""

    label = _("Last publications")
    href = '#last-published.html'


@implementer(IView)
class SharedToolLastPublicationsTable(DashboardTable):
    """Shared tool dashboard last publications table"""


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolLastPublicationsTable),
                provides=IValues)
class SharedToolLastPublicationsValues(ContextRequestViewAdapter):
    """Shared tool publications values adapter"""

    @property
    def values(self):
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        workflow = get_utility(IWorkflow, name=self.context.shared_content_workflow)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(self.context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()) &
                     Any(catalog['workflow_state'], workflow.published_states))
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         limit=50,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='last-published.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolLastPublicationsView(BaseSharedToolDashboardSingleView):
    """Shared tool last publications view"""

    header_label = _("Last publications")
    table_class = SharedToolLastPublicationsTable

    empty_label = _("CONTRIBUTORS - 0 published content")
    single_label = _("CONTRIBUTORS - 1 published content")

    @property
    def plural_label(self):
        length = len(self.table.values)
        if length == 50:
            return _("CONTRIBUTORS - Last {} published contents")
        return _("CONTRIBUTORS - {} published contents")


#
# Last modified contents
#

@viewlet_config(name='last-modified.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IAllDashboardMenu, weight=30,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolLastModifiedMenu(NavigationMenuItem):
    """Shared tool modified contents dashboard menu"""

    label = _("Last modifications")
    href = '#last-modified.html'


@implementer(IView)
class SharedToolLastModificationsTable(DashboardTable):
    """Shared tool dashboard last modifications table"""


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolLastModificationsTable),
                provides=IValues)
class SharedToolLastModificationsValues(ContextRequestViewAdapter):
    """Shared tool modifications values adapter"""

    @property
    def values(self):
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(self.context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()))
        yield from unique_iter(
            CatalogResultSet(CatalogQuery(catalog).query(params,
                                                         limit=50,
                                                         sort_index='modified_date',
                                                         reverse=True)))


@pagelet_config(name='last-modified.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedToolLastModificationsView(BaseSharedToolDashboardSingleView):
    """Shared tool last modifications view"""

    header_label = _("Last modifications")
    table_class = SharedToolLastModificationsTable

    empty_label = _("CONTRIBUTORS - 0 modified content")
    single_label = _("CONTRIBUTORS - 1 modified content")

    @property
    def plural_label(self):
        length = len(self.table.values)
        if length == 50:
            return _("CONTRIBUTORS - Last {} modified contents")
        return _("CONTRIBUTORS - {} modified contents")
