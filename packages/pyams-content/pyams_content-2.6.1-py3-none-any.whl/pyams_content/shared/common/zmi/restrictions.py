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

"""PyAMS_content.shared.common.zmi.restrictions module

This module defines components which are used to handle security restrictions.
"""

from pyramid.decorator import reify
from zope.interface import implementer

from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.shared.common import IBaseSharedTool
from pyams_content.shared.common.interfaces import IContributorRestrictions, \
    IContributorWorkflowRestrictions, IManagerRestrictions, IManagerWorkflowRestrictions, \
    IPrincipalRestrictions, ISharedToolRoles
from pyams_content.shared.common.zmi.interfaces import IContributorRestrictionsEditForm, \
    IManagerRestrictionsEditForm, IManagerRestrictionsGroup
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces import HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IFormContent, IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces import ISecurityManager
from pyams_security_views.zmi.interfaces import IObjectSecurityMenu
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.registry import get_utility
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalEditForm, FormGroupChecker
from pyams_zmi.helper.event import get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.table import I18nColumnMixin, IconColumn, Table, TableAdminView, TableElementEditor
from pyams_zmi.utils import get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _  # pylint: disable=ungrouped-imports


#
# Managers restrictions table view
#

@viewlet_config(name='managers-restrictions.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IObjectSecurityMenu, weight=200,
                permission=MANAGE_TOOL_PERMISSION)
class ManagersRestrictionsMenu(NavigationMenuItem):
    """Manager restrictions menu"""

    label = _("Managers restrictions")
    href = '#managers-restrictions.html'


class ManagersRestrictionsTable(Table):
    """Managers restrictions table"""

    def get_row_id(self, row):
        return f'{self.id}::{row[0].id}'


@adapter_config(required=(IBaseSharedTool, IAdminLayer, ManagersRestrictionsTable),
                provides=IValues)
class ManagersRestrictionsTableValues(ContextRequestViewAdapter):
    """Managers restrictions table values"""

    @property
    def values(self):
        """Managers restrictions table values getter"""
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        roles = ISharedToolRoles(self.context)
        restrictions = IManagerRestrictions(self.context)
        for principal_id in roles.managers:
            yield sm.get_principal(principal_id), restrictions.get_restrictions(principal_id)


@adapter_config(name='title',
                required=(IBaseSharedTool, IAdminLayer, ManagersRestrictionsTable),
                provides=IColumn)
class ManagerTitleColumn(I18nColumnMixin, GetAttrColumn):
    """Manager title column"""

    i18n_header = _("Manager name")
    attr_name = 'title'

    weight = 10

    def get_value(self, obj):
        return super().get_value(obj[0])


@adapter_config(name='warning',
                required=(IBaseSharedTool, IAdminLayer, ManagersRestrictionsTable),
                provides=IColumn)
class ManagerWarningColumn(I18nColumnMixin, IconColumn):
    """Manager workflow warning column"""

    i18n_header = _("Show warnings")
    css_classes = {}
    weight = 20

    def get_icon_class(self, item):
        restrictions = IManagerWorkflowRestrictions(item[1])
        if restrictions.show_workflow_warning:
            return 'fas fa-check'
        return ''


@adapter_config(name='restricted',
                required=(IBaseSharedTool, IAdminLayer, ManagersRestrictionsTable),
                provides=IColumn)
class ManagerRestrictedColumn(I18nColumnMixin, IconColumn):
    """Manager workflow warning column"""

    i18n_header = _("Restricted")
    css_classes = {}
    weight = 30

    def get_icon_class(self, item):
        restrictions = IManagerWorkflowRestrictions(item[1])
        if restrictions.restricted_contents:
            return 'fas fa-check'
        return ''


@adapter_config(name='owners',
                required=(IBaseSharedTool, IAdminLayer, ManagersRestrictionsTable),
                provides=IColumn)
class ManagerOwnersColumn(I18nColumnMixin, GetAttrColumn):
    """Manager owners column"""

    i18n_header = _("Manager for")
    weight = 40

    def get_value(self, obj):
        restrictions = IManagerWorkflowRestrictions(obj[1])
        if not restrictions.owners:
            return MISSING_INFO
        sm = get_utility(ISecurityManager)
        return ', '.join((
            sm.get_principal(principal_id).title
            for principal_id in restrictions.owners
        ))


@pagelet_config(name='managers-restrictions.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=MANAGE_TOOL_PERMISSION)
class ManagersRestrictionsView(TableAdminView):
    """Managers restrictions view"""

    title = _("Managers restrictions")

    table_class = ManagersRestrictionsTable
    table_label = _("Managers list")


#
# Manager restrictions view
#

@adapter_config(required=(tuple, IAdminLayer, ManagersRestrictionsTable),
                provides=ITableElementEditor)
class ManagerRestrictionsEditor(TableElementEditor):
    """Manager restrictions editor"""

    view_name = 'manager-restrictions.html'

    @property
    def href(self):
        return absolute_url(self.view.context, self.request, self.view_name,
                            query={'principal_id': self.context[0].id})


@ajax_form_config(name='manager-restrictions.html',
                  context=IBaseSharedTool, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
@implementer(IManagerRestrictionsEditForm)
class ManagerRestrictionsEditForm(AdminModalEditForm):
    """Manager restrictions edit form"""

    @property
    def subtitle(self):
        return self.principal.title

    fields = Fields(IPrincipalRestrictions)

    @reify
    def principal_id(self):
        """Principal ID getter"""
        params = self.request.params
        return params.get('principal_id') or params.get('form.widgets.principal_id')

    @reify
    def principal(self):
        """Principal ID getter"""
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        return sm.get_principal(self.principal_id)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        principal_id = self.widgets.get('principal_id')
        if principal_id is not None:
            principal_id.mode = HIDDEN_MODE
            principal_id.value = self.principal_id


@adapter_config(required=(IBaseSharedTool, IAdminLayer, IManagerRestrictionsEditForm),
                provides=IFormTitle)
def base_shared_tool_manager_restrictions_form_title(context, request, form):
    """Base shared tool manager restrictions edit form title getter"""
    translate = request.localizer.translate
    return TITLE_SPAN_BREAK.format(
        get_object_label(context, request, form),
        translate(_("Manager restrictions")))


@adapter_config(required=(IBaseSharedTool, IAdminLayer, IManagerRestrictionsEditForm),
                provides=IFormContent)
def manager_restrictions_edit_form_content(context, request, form):
    """Manager restrictions edit form content getter"""
    return IManagerRestrictions(context).get_restrictions(form.principal.id)


@adapter_config(required=(IBaseSharedTool, IAdminLayer, IManagerRestrictionsEditForm),
                provides=IAJAXFormRenderer)
class ManagerRestrictionsEditFormRenderer(ContextRequestViewAdapter):
    """Manager restrictions edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        sm = get_utility(ISecurityManager)
        restrictions = IManagerRestrictions(self.context)
        principal_id = self.view.principal_id
        context = sm.get_principal(principal_id), restrictions.get_restrictions(principal_id)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(self.context, self.request,
                                                    ManagersRestrictionsTable,
                                                    context)
            ]
        }


@adapter_config(name='workflow',
                required=(IBaseSharedTool, IAdminLayer, IManagerRestrictionsEditForm),
                provides=IGroup)
class ManagerRestrictionsWorkflowGroup(Group):
    """Manager restrictions workflow group"""

    legend = _("Principal restrictions")
    fields = Fields(IManagerWorkflowRestrictions).select('show_workflow_warning')


@adapter_config(required=(IBaseSharedTool, IAdminLayer, ManagerRestrictionsWorkflowGroup),
                provides=IFormContent)
def get_manager_restrictions_workflow_group_content(context, request, group):
    """Manager restrictions workflow group content getter"""
    return IManagerWorkflowRestrictions(group.parent_form.get_content())


@adapter_config(name='restrictions',
                required=(IBaseSharedTool, IAdminLayer, ManagerRestrictionsWorkflowGroup),
                provides=IGroup)
@implementer(IManagerRestrictionsGroup)
class ManagerRestrictionInnerGroup(FormGroupChecker):
    """Manager restrictions inner group"""

    fields = Fields(IManagerWorkflowRestrictions).omit('show_workflow_warning')
    weight = 10

    checker_fieldname = 'restricted_contents'


@viewlet_config(name='restrictions.help',
                context=IBaseSharedTool, layer=IAdminLayer, view=ManagerRestrictionInnerGroup,
                manager=IHelpViewletManager, weight=10)
class ManagerRestrictionsHelp(AlertMessage):
    """Manager restrictions help"""

    status = 'info'
    _message = _("If restrictions are enabled for this manager, he will only be able to "
                 "manage contents matching at least one of these properties!")

    message_renderer = 'markdown'


#
# Contributors restrictions table view
#

@viewlet_config(name='contributors-restrictions.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IObjectSecurityMenu, weight=210,
                permission=MANAGE_TOOL_PERMISSION)
class ContributorsRestrictionsMenu(NavigationMenuItem):
    """Contributor restrictions menu"""

    label = _("Contributors restrictions")
    href = '#contributors-restrictions.html'


class ContributorsRestrictionsTable(Table):
    """Contributors restrictions table"""

    def get_row_id(self, row):
        return f'{self.id}::{row[0].id}'


@adapter_config(required=(IBaseSharedTool, IAdminLayer, ContributorsRestrictionsTable),
                provides=IValues)
class ContributorsRestrictionsTableValues(ContextRequestViewAdapter):
    """Contributors restrictions table values"""

    @property
    def values(self):
        """Contributors restrictions table values getter"""
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        roles = ISharedToolRoles(self.context)
        restrictions = IContributorRestrictions(self.context)
        for principal_id in roles.contributors:
            yield sm.get_principal(principal_id), restrictions.get_restrictions(principal_id)


@adapter_config(name='title',
                required=(IBaseSharedTool, IAdminLayer, ContributorsRestrictionsTable),
                provides=IColumn)
class ContributorTitleColumn(I18nColumnMixin, GetAttrColumn):
    """Contributor title column"""

    i18n_header = _("Contributor name")
    attr_name = 'title'

    weight = 10

    def get_value(self, obj):
        return super().get_value(obj[0])


@adapter_config(name='warning',
                required=(IBaseSharedTool, IAdminLayer, ContributorsRestrictionsTable),
                provides=IColumn)
class ContributorWarningColumn(I18nColumnMixin, IconColumn):
    """Contributor workflow warning column"""

    i18n_header = _("Show warnings")
    css_classes = {}
    weight = 20

    def get_icon_class(self, item):
        restrictions = IContributorWorkflowRestrictions(item[1])
        if restrictions.show_workflow_warning:
            return 'fas fa-check'
        return ''


@adapter_config(name='substitutes',
                required=(IBaseSharedTool, IAdminLayer, ContributorsRestrictionsTable),
                provides=IColumn)
class ContributorSubstitutesColumn(I18nColumnMixin, GetAttrColumn):
    """Contributor substitutes column"""

    i18n_header = _("Substitute of")
    weight = 30

    def get_value(self, obj):
        restrictions = IContributorWorkflowRestrictions(obj[1])
        if not restrictions.owners:
            return MISSING_INFO
        sm = get_utility(ISecurityManager)
        return ', '.join((
            sm.get_principal(principal_id).title
            for principal_id in restrictions.owners
        ))


@pagelet_config(name='contributors-restrictions.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=MANAGE_TOOL_PERMISSION)
class ContributorsRestrictionsView(TableAdminView):
    """Contributors restrictions view"""

    title = _("Contributors restrictions")

    table_class = ContributorsRestrictionsTable
    table_label = _("Contributors list")


#
# Contributor restrictions view
#

@adapter_config(required=(tuple, IAdminLayer, ContributorsRestrictionsTable),
                provides=ITableElementEditor)
class ContributorRestrictionsEditor(TableElementEditor):
    """Contributor restrictions editor"""

    view_name = 'contributor-restrictions.html'

    @property
    def href(self):
        return absolute_url(self.view.context, self.request, self.view_name,
                            query={'principal_id': self.context[0].id})


@ajax_form_config(name='contributor-restrictions.html',
                  context=IBaseSharedTool, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
@implementer(IContributorRestrictionsEditForm)
class ContributorRestrictionsEditForm(AdminModalEditForm):
    """Contributor restrictions edit form"""

    @property
    def subtitle(self):
        return self.principal.title

    fields = Fields(IPrincipalRestrictions)

    @reify
    def principal_id(self):
        """Principal ID getter"""
        params = self.request.params
        return params.get('principal_id') or params.get('form.widgets.principal_id')

    @reify
    def principal(self):
        """Principal ID getter"""
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        return sm.get_principal(self.principal_id)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        principal_id = self.widgets.get('principal_id')
        if principal_id is not None:
            principal_id.mode = HIDDEN_MODE
            principal_id.value = self.principal_id


@adapter_config(required=(IBaseSharedTool, IAdminLayer, IContributorRestrictionsEditForm),
                provides=IFormTitle)
def base_shared_tool_contributor_restrictions_form_title(context, request, form):
    """Base shared tool contributor restrictions edit form title getter"""
    translate = request.localizer.translate
    return TITLE_SPAN_BREAK.format(
        get_object_label(context, request, form),
        translate(_("Contributor restrictions")))


@adapter_config(required=(IBaseSharedTool, IAdminLayer, IContributorRestrictionsEditForm),
                provides=IFormContent)
def contributor_restrictions_edit_form_content(context, request, form):
    """Contributor restrictions edit form content getter"""
    return IContributorRestrictions(context).get_restrictions(form.principal.id)


@adapter_config(required=(IBaseSharedTool, IAdminLayer, IContributorRestrictionsEditForm),
                provides=IAJAXFormRenderer)
class ContributorRestrictionsEditFormRenderer(ContextRequestViewAdapter):
    """Contributor restrictions edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        sm = get_utility(ISecurityManager)
        restrictions = IContributorRestrictions(self.context)
        principal_id = self.view.principal_id
        context = sm.get_principal(principal_id), restrictions.get_restrictions(principal_id)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(self.context, self.request,
                                                    ContributorsRestrictionsTable,
                                                    context)
            ]
        }


@adapter_config(name='workflow',
                required=(IBaseSharedTool, IAdminLayer, IContributorRestrictionsEditForm),
                provides=IGroup)
class ContributorRestrictionsWorkflowGroup(Group):
    """Contributor_restrictions workflow group"""

    legend = _("Principal restrictions")
    fields = Fields(IContributorWorkflowRestrictions)


@adapter_config(required=(IBaseSharedTool, IAdminLayer, ContributorRestrictionsWorkflowGroup),
                provides=IFormContent)
def base_shared_tool_contributor_restrictions_form_content(context, request, form):
    """Base shared tool contributor restrictions edit form content getter"""
    return IContributorWorkflowRestrictions(form.parent_form.get_content())
