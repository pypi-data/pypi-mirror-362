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

"""PyAMS_content.shared.common.zmi.content module

This module provides common management components for shared contents.
"""

from zope.interface import Interface

from pyams_content.shared.common import IBaseSharedTool
from pyams_content.shared.common.interfaces import ISharedContent, IWfSharedContent, IWfSharedContentRoles
from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentNumber, \
    IDashboardContentOwner, IDashboardContentType, ISiteRootDashboardContentType
from pyams_i18n.interfaces import II18n
from pyams_security.utility import get_principal
from pyams_security_views.interfaces.login import ILoginView
from pyams_sequence.interfaces import ISequentialIdTarget
from pyams_skin.interfaces.view import IModalPage
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.date import format_datetime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import EmptyViewlet, Viewlet, viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, IWorkflowState, \
    IWorkflowStateLabel, IWorkflowVersions
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectLabel
from pyams_zmi.zmi.viewlet.header import ContentHeaderViewlet

__docformat__ = 'restructuredtext'

from pyams_content import _


def shared_content_version_getter(context, request, view, interface):
    """Shared content version generic interface getter"""
    versions = IWorkflowVersions(context, None)
    if versions is not None:
        version = versions.get_last_versions()[0]
        return request.registry.queryMultiAdapter((version, request, view), interface)


@adapter_config(required=(IWfSharedContent, IAdminLayer, Interface),
                provides=IObjectHint)
def wf_shared_content_hint(context, request, view):
    """Workflow-managed shared content hint"""
    translate = request.localizer.translate
    return translate(context.content_name)


@adapter_config(required=(ISharedContent, IAdminLayer, Interface),
                provides=IObjectHint)
def shared_content_hint(context, request, view):
    """Shared content hint"""
    return shared_content_version_getter(context, request, view, IObjectHint)


@adapter_config(required=(IWfSharedContent, IAdminLayer, Interface),
                provides=IObjectLabel)
def wf_shared_content_label(context, request, view):
    """Workflow-managed shared content label"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=(ISharedContent, IAdminLayer, Interface),
                provides=IObjectLabel)
def shared_content_label(context, request, view):
    """Shared content label"""
    return shared_content_version_getter(context, request, view, IObjectLabel)


@adapter_config(required=(IWfSharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentType)
def wf_shared_content_type(context, request, column):
    """Workflow-managed shared content type"""
    if IWfTypedSharedContent.providedBy(context):
        data_type = context.get_data_type()
        if data_type is not None:
            i18n = II18n(data_type)
            return i18n.query_attributes_in_order(('dashboard_label', 'label'),
                                                  request=request)
    return None


@adapter_config(required=(ISharedContent, IAdminLayer, Interface),
                provides=IDashboardContentType)
def shared_content_type(context, request, view):
    """Shared content label"""
    return shared_content_version_getter(context, request, view, IDashboardContentType)


@adapter_config(required=(IWfSharedContent, IAdminLayer, IDashboardColumn),
                provides=ISiteRootDashboardContentType)
def wf_site_root_shared_content_type(context, request, column):
    """Site root workflow-managed shared content type"""
    translate = request.localizer.translate
    data_type = wf_shared_content_type(context, request, column)
    content_name = translate(context.content_name)
    if data_type is None:
        return content_name
    return f'{content_name} ({data_type})'


@adapter_config(required=(ISharedContent, IAdminLayer, IDashboardColumn),
                provides=ISiteRootDashboardContentType)
def site_root_shared_content_type(context, request, view):
    """Site root shared content type"""
    return shared_content_version_getter(context, request, view, ISiteRootDashboardContentType)


@adapter_config(required=(IWfSharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentNumber)
def wf_shared_content_number(context, request, column):
    """Shared content dashboard number getter"""
    target = get_parent(context, ISequentialIdTarget)
    return request.registry.queryMultiAdapter((target, request, column),
                                              IDashboardContentNumber)


@adapter_config(required=(IWfSharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentOwner)
def wf_shared_content_owner(context, request, column):
    """Workflow-managed shared content dashboard owner getter"""
    owner = IWfSharedContentRoles(context).owner
    if owner:
        return get_principal(request, next(iter(owner))).title
    return None


@adapter_config(required=(ISharedContent, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentOwner)
def shared_content_owner(context, request, view):
    """Shared content owner getter"""
    return shared_content_version_getter(context, request, view, IDashboardContentOwner)


@viewlet_config(name='pyams.content_header',
                context=IWfSharedContent, layer=IAdminLayer,
                manager=IHeaderViewletManager, weight=10)
@template_config(template='templates/content-header.pt')
class SharedContentHeaderViewlet(ContentHeaderViewlet):
    """Shared content header viewlet"""

    @property
    def parent_target_url(self):
        """Parent target URL"""
        tool = get_parent(self.context, IBaseSharedTool)
        if tool is None:
            return None
        return absolute_url(tool, self.request, 'admin#dashboard.html')

    @property
    def owner(self):
        """Owner getter"""
        owner = IWfSharedContentRoles(self.context).owner
        if owner:
            translate = self.request.localizer.translate
            return translate(_("from {}")).format(
                get_principal(self.request, next(iter(owner))).title)


@viewlet_config(name='pyams.content_header',
                context=IWfSharedContent, layer=IAdminLayer, view=ILoginView,
                manager=IHeaderViewletManager, weight=10)
class SharedContentHeaderLoginViewViewlet(EmptyViewlet):
    """Shared content header viewlet on login view"""


@viewlet_config(name='workflow-status',
                context=IWfSharedContent, layer=IAdminLayer,
                manager=IHeaderViewletManager, weight=20)
@template_config(template='templates/content-workflow.pt')
class SharedContentWorkflowStatus(Viewlet):
    """Shared content workflow status"""

    @property
    def version(self):
        """Version getter"""
        return IWorkflowState(self.context).version_id

    @staticmethod
    def create_link(href, title, css_class):
        """Link creation"""
        return f'<a href="{href}" class="{css_class}">{title}</a>'

    @property
    def state(self):
        context = self.context
        request = self.request
        registry = request.registry
        translate = request.localizer.translate
        result = []
        workflow = IWorkflow(context)
        state = IWorkflowState(context)
        versions = IWorkflowVersions(context)
        # init state format
        state_format = translate(_('{state} <span class="px-1">by</span> {principal}'))
        if state.state in workflow.waiting_states:
            if state.state_urgency:
                state_format = state_format.replace(
                    '{state}',
                    '{state} <i class="fas fa-fw fa-exclamation-triangle text-danger"></i>')
        elif state.state in workflow.published_states:
            pub_info = IWorkflowPublicationInfo(context, None)
            if (pub_info is not None) and not pub_info.is_published():
                state_format = state_format.replace(
                    '{state}',
                    '{{state}} <i class="fas fa-fw fa-hourglass-half font-xs '
                    'text-danger opacity-75 hint align-base" '
                    'data-ams-hint-offset="5" title="{0}"></i>'.format(
                        translate(_("Content publication start date is not passed yet"))))
        state_class = 'text-danger'
        state_format = state_format.replace(
            '{state}',
            f'<span class="{state_class}">{{state}}</span>')
        # init principal format
        principal_class = 'text-danger' \
            if state.state in (workflow.update_states | workflow.waiting_states) \
            else 'txt-color-text'
        state_format = state_format.replace(
            '{principal}',
            f'<span class="{principal_class}">{{principal}}</span>')
        # get state label
        state_label = registry.queryAdapter(workflow, IWorkflowStateLabel, name=state.state)
        if state_label is None:
            state_label = registry.queryAdapter(workflow, IWorkflowStateLabel)
        if state_label is None:
            wf_state = state_format.format(
                state=translate(workflow.get_state_label(state.state)),
                principal=get_principal(request, state.state_principal).title)
        else:
            wf_state = state_format.format(
                state=state_label.get_label(context, request, format=False),
                principal=get_principal(request, state.state_principal).title)
        result.append(wf_state)
        result.append(translate(_("since {date}")).format(
            date=format_datetime(state.state_date, request=request)))
        # check for links to other versions
        visible_versions = sorted(versions.get_versions(workflow.visible_states),
                                  key=lambda x: IWorkflowState(x).version_id)
        draft_versions = sorted(versions.get_versions(workflow.update_states),
                                key=lambda x: IWorkflowState(x).version_id)
        if (state.version_id > 1) or (state.state != workflow.initial_state):
            targets = set()
            if visible_versions:
                target = visible_versions[0]
                if (target is not context) and (target not in targets):
                    result.append(self.create_link(**{
                        'title': translate(_("access published version")),
                        'href': absolute_url(target, request, 'admin'),
                        'css_class': 'text-primary'
                    }))
                    targets.add(target)
            if draft_versions:
                target = draft_versions[0]
                if (target is not context) and (target not in targets):
                    result.append(self.create_link(**{
                        'title': translate(_("access new version")),
                        'href': absolute_url(target, request, 'admin'),
                        'css_class': 'text-primary'
                    }))
                    targets.add(target)
            else:
                waiting_versions = sorted(versions.get_versions(workflow.waiting_states),
                                          key=lambda x: IWorkflowState(x).version_id)
                if waiting_versions:
                    target = waiting_versions[-1]
                    if (target is not context) and (target not in targets):
                        result.append(self.create_link(**{
                            'title': translate(_("access waiting version")),
                            'href': absolute_url(target, request, 'admin'),
                            'css_class': 'text-primary'
                        }))
                        targets.add(target)
            if (state.version_id > 1) and \
                    (state.state not in (workflow.retired_states | workflow.archived_states)):
                retired_versions = sorted(filter(
                        lambda x: IWorkflowState(x).version_id < state.version_id,
                        versions.get_versions(workflow.retired_states)),
                    key=lambda x: IWorkflowState(x).version_id)
                if retired_versions:
                    target = retired_versions[-1]
                    if (target is not context) and (target not in targets):
                        result.append(self.create_link(**{
                            'title': translate(_("access retired version")),
                            'href': absolute_url(target, request, 'admin'),
                            'css_class': 'text-primary'
                        }))
                else:
                    archived_versions = sorted(filter(
                            lambda x: IWorkflowState(x).version_id < state.version_id,
                            versions.get_versions(workflow.archived_states)),
                        key=lambda x: IWorkflowState(x).version_id)
                    if archived_versions:
                        target = archived_versions[-1]
                        if (target is not context) and (target not in targets):
                            result.append(self.create_link(**{
                                'title': translate(_("access archived version")),
                                'href': absolute_url(target, request, 'admin'),
                                'css_class': 'text-primary'
                            }))
        return '<span class="px-2">|</span>'.join(result)


@viewlet_config(name='workflow-status',
                context=IWfSharedContent, layer=IAdminLayer, view=IModalPage,
                manager=IHeaderViewletManager, weight=20)
@viewlet_config(name='workflow-status',
                context=IWfSharedContent, layer=IAdminLayer, view=ILoginView,
                manager=IHeaderViewletManager, weight=20)
class SharedContentWorkflowModalStatus(EmptyViewlet):
    """Shared content workflow modal status"""
