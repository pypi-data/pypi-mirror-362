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

"""PyAMS_content.shared.common.zmi.summary module

This module provides components which are used to display a summary of main content properties.
"""

from zope.interface import Interface

from pyams_content.shared.common import IWfSharedContent, IWfSharedContentRoles
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces import DISPLAY_MODE, IDataConverter
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.utility import get_principal
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_skin.viewlet.actions import ContextAction
from pyams_utils.adapter import adapter_config
from pyams_utils.date import format_datetime
from pyams_utils.timezone import tztime
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, IWorkflowState, \
    IWorkflowStateHistoryItem
from pyams_zmi.form import AdminModalDisplayForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='summary.action',
                context=IWfSharedContent, layer=IAdminLayer, view=Interface,
                manager=IToolbarViewletManager, weight=5,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedContentSummaryAction(ContextAction):
    """Shared content summary action"""

    status = 'transparent'
    css_class = 'btn-xs rounded-circle border-primary mr-3'
    icon_class = 'fas fa-info text-primary px-0 py-1'

    hint = _("Content information")

    href = 'summary.html'
    modal_target = True


@ajax_form_config(name='summary.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SharedContentSummaryView(AdminModalDisplayForm):
    """Shared content summary view"""

    legend = _("Display content summary")
    modal_class = 'modal-xl'


@adapter_config(name='dublincore',
                required=(IWfSharedContent, IAdminLayer, SharedContentSummaryView),
                provides=IGroup)
class SharedContentDublinCoreGroup(Group):
    """Shared content dublin-core group"""

    legend = _("Identity card")
    weight = 10

    fields = Fields(IWfSharedContent).select('title') + \
        Fields(ISequentialIdInfo).select('public_oid')
    mode = DISPLAY_MODE


@adapter_config(name='workflow-waiting',
                required=(IWfSharedContent, IAdminLayer, SharedContentSummaryView),
                provides=IGroup)
class SharedContentWorkflowWaitingState(Group):
    """Shared content workflow"""

    def __new__(cls, context, request, form):
        state  = IWorkflowState(context, None)
        if state is None:
            return None
        workflow = IWorkflow(context)
        if state.state not in workflow.waiting_states:
            return None
        return Group.__new__(cls)

    legend = _("Workflow requested action")
    weight = 20

    fields = Fields(IWorkflowState).select('state', 'state_urgency') + \
        Fields(IWorkflowStateHistoryItem).select('comment')
    mode = DISPLAY_MODE

    ignore_context = True

    def update_widgets(self, prefix=None, use_form_mode=True):
        self.parent_form.widgets.ignore_context = True
        super().update_widgets(prefix, use_form_mode)
        state = IWorkflowState(self.context)
        state_widget = self.widgets.get('state')
        if state_widget is not None:
            translate = self.request.localizer.translate
            workflow = IWorkflow(self.context)
            state_widget.value = translate(_("{state} {date} by {principal}")).format(
                state=translate(workflow.get_state_label(state.state)),
                date=format_datetime(state.state_date),
                principal=get_principal(self.request, state.state_principal).title)
        state_urgency = self.widgets.get('state_urgency')
        if state_urgency is not None:
            converter = IDataConverter(state_urgency)
            state_urgency.value = converter.to_widget_value(state.state_urgency)
        state_comment = self.widgets.get('comment')
        if state_comment is not None:
            history_item = state.history[-1]
            state_comment.label = _("Associated comment")
            state_comment.value = history_item.comment
        self.parent_form.widgets.ignore_context = False


@adapter_config(name='publication',
                required=(IWfSharedContent, IAdminLayer, SharedContentSummaryView),
                provides=IGroup)
class SharedContentPublicationInfo(Group):
    """Shared content version info"""

    def __new__(cls, context, request, form):
        info = IWorkflowPublicationInfo(context, None)
        if (info is None) or not info.publication_effective_date:
            return None
        return Group.__new__(cls)

    legend = _("Publication dates")
    weight = 30

    fields = Fields(IWorkflowPublicationInfo).select('publication_effective_date',
                                                     'push_end_date',
                                                     'publication_expiration_date',
                                                     'displayed_publication_date')
    mode = DISPLAY_MODE


@adapter_config(name='version',
                required=(IWfSharedContent, IAdminLayer, SharedContentSummaryView),
                provides=IGroup)
class SharedContentVersionInfo(Group):
    """Shared content version info"""

    def __new__(cls, context, request, form):
        state = IWorkflowState(context, None)
        if state is None:
            return None
        return Group.__new__(cls)

    legend = _("Current version")
    weight = 40

    fields = Fields(IWorkflowState).select('version_id', 'state') + \
        Fields(IWfSharedContent).select('creation_label') + \
        Fields(IWfSharedContentRoles).select('owner') + \
        Fields(IWfSharedContent).select('last_update_label', 'modifiers')
    mode = DISPLAY_MODE

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        version_id = self.widgets.get('version_id')
        if version_id is not None:
            version_id.label = _("Version")
        state_widget = self.widgets.get('state')
        if state_widget is not None:
            translate = self.request.localizer.translate
            workflow = IWorkflow(self.context)
            workflow_state = IWorkflowState(self.context)
            history_item = workflow_state.history[-1]
            state_widget.value = translate(_("{state} since {date}, by {principal}")).format(
                state=translate(workflow.get_state_label(workflow_state.state)),
                date=format_datetime(tztime(history_item.date)),
                principal=get_principal(self.request, history_item.principal).title)


@adapter_config(name='history',
                required=(IWfSharedContent, IAdminLayer, SharedContentSummaryView),
                provides=IGroup)
class SharedContentHistoryInfo(Group):
    """Shared content history info"""

    def __new__(cls, context, request, form):
        info = IWorkflowPublicationInfo(context, None)
        if info is None:
            return None
        return Group.__new__(cls)

    legend = _("Content history")
    weight = 50

    @property
    def fields(self):
        fields = Fields(IWorkflowPublicationInfo).select('first_publication_date')
        state = IWorkflowState(self.context, None)
        if state and state.version_id > 1:
            fields += Fields(IWorkflowPublicationInfo).select('content_publication_date')
        fields += Fields(IWfSharedContent).select('first_owner')
        return fields

    mode = DISPLAY_MODE

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        info = IWorkflowPublicationInfo(self.context, None)
        version_date = self.widgets.get('first_publication_date')
        if version_date is not None:
            version_date.value = format_datetime(info.first_publication_date)
        content_date = self.widgets.get('content_publication_date')
        if content_date is not None:
            content_date.value = format_datetime(info.content_publication_date)
