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

"""PyAMS_content.shared.common.zmi.workflow module

"""

from datetime import datetime, timezone

from pyramid.events import subscriber
from zope.container.interfaces import IContainer
from zope.interface import Interface, Invalid
from zope.lifecycleevent import ObjectModifiedEvent

from pyams_content.interfaces import CREATE_VERSION_PERMISSION, MANAGE_CONTENT_PERMISSION, \
    PUBLISH_CONTENT_PERMISSION
from pyams_content.shared.common.interfaces import IBaseSharedTool, ISharedContent, ISharedToolInnerFolder, \
    IWfSharedContent, IWfSharedContentRoles
from pyams_content.shared.common.zmi.interfaces import IWorkflowDeleteFormTarget
from pyams_content.workflow import DELETED, DRAFT, PROPOSED, PUBLISHED
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.utility import get_principal
from pyams_skin.interfaces.viewlet import IFormFooterViewletManager, IFormHeaderViewletManager
from pyams_skin.schema.button import CloseButton, SubmitButton
from pyams_skin.viewlet.help import AlertMessage
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.date import format_datetime
from pyams_utils.text import text_to_html
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import Viewlet, viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowCommentInfo, \
    IWorkflowInfo, IWorkflowPublicationInfo, IWorkflowRequestUrgencyInfo, IWorkflowState, \
    IWorkflowStateLabel, IWorkflowTransitionInfo, IWorkflowVersion, IWorkflowVersions, \
    MANUAL_TRANSITION, NoTransitionAvailableError, SYSTEM_TRANSITION
from pyams_workflow.zmi.transition import WorkflowContentTransitionForm
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'

from pyams_content import _


class ISharedContentWorkflowFormButtons(Interface):
    """Shared content workflow transition form buttons"""

    action = SubmitButton(name='action', title=_("Workflow action"))
    close = CloseButton(name='close', title=_("Cancel"))


class SharedContentWorkflowTransitionForm(WorkflowContentTransitionForm):
    """Shared content workflow transition form"""

    legend = _("Action comment")
    buttons = Buttons(ISharedContentWorkflowFormButtons)

    def update_actions(self):
        super().update_actions()
        if 'action' in self.actions:
            self.actions['action'].title = self.transition.title

    @handler(buttons['action'])
    def handle_delete(self, action):
        """Delete action handler"""
        super().handle_add(self, action)


@adapter_config(required=(IWorkflowVersion, IAdminLayer, SharedContentWorkflowTransitionForm),
                provides=IAJAXFormRenderer)
class SharedContentWorkflowTransitionFormRenderer(ContextRequestViewAdapter):
    """Shared content workflow transition form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        return {
            'status': 'redirect'
        }


@viewlet_config(name='wf-operator-warning',
                context=IWfSharedContent, layer=IAdminLayer,
                view=SharedContentWorkflowTransitionForm,
                manager=IFormHeaderViewletManager, weight=20)
class SharedContentWorkflowOperatorWarning(AlertMessage):
    """Shared content workflow operator warning"""

    def __new__(cls, context, request, view, manager):
        transition = view.transition
        if not transition.user_data.get('show_operator_warning'):
            return None
        state = IWorkflowState(context)
        roles = IWfSharedContentRoles(context)
        if state.state_principal in roles.owner:
            return None
        return AlertMessage.__new__(cls)

    status = 'danger'

    _message = _("WARNING: this request was made by a contributor which is not the owner "
                 "of this content")


@viewlet_config(name='wf-owner-warning',
                context=IWfSharedContent, layer=IAdminLayer,
                view=SharedContentWorkflowTransitionForm,
                manager=IFormHeaderViewletManager, weight=25)
class SharedContentWorkflowOwnerWarning(AlertMessage):
    """Shared content workflow owner warning"""

    def __new__(cls, context, request, view, manager):
        roles = IWfSharedContentRoles(context)
        if request.principal.id in roles.owner:
            return None
        return AlertMessage.__new__(cls)

    status = 'danger'

    _message = _("RECALL: you are not the owner of the content on which you operate!")


#
# Generic transition info
#

@viewlet_config(name='wf-transition-info',
                context=IWfSharedContent, layer=IAdminLayer,
                view=SharedContentWorkflowTransitionForm,
                manager=IFormFooterViewletManager, weight=10)
@template_config(template='templates/wf-transition-info.pt')
class SharedContentWorkflowTransitionFormInfo(Viewlet):
    """Generic workflow transition form info"""

    @property
    def previous_step(self):
        """Previous step getter"""
        translate = self.request.localizer.translate
        workflow = IWorkflow(self.context)
        state = IWorkflowState(self.context)
        registry = self.request.registry
        adapter = registry.queryMultiAdapter((workflow, self.request), IWorkflowStateLabel,
                                             name=state.state)
        if adapter is None:
            adapter = registry.queryAdapter(workflow, IWorkflowStateLabel,
                                            name=state.state)
        if adapter is None:
            adapter = registry.queryAdapter(workflow, IWorkflowStateLabel)
        if adapter is not None:
            state_label = adapter.get_label(self.context, request=self.request)
        else:
            state_label = translate(_("{state} {date}")).format(
                state=translate(workflow.get_state_label(state.state)),
                date=format_datetime(state.state_date, request=self.request))
        return translate(_("{state} | by {principal}")).format(
            state=state_label,
            principal=get_principal(self.request, state.state_principal).title)

    @property
    def previous_message(self):
        """Previous step message"""
        workflow = IWorkflow(self.context)
        state = IWorkflowState(self.context)
        position = 0
        history_item = None
        trigger = SYSTEM_TRANSITION
        while trigger != MANUAL_TRANSITION:
            position -= 1
            history_item = state.history[position]
            if history_item.transition_id:
                try:
                    trigger = workflow.get_transition_by_id(history_item.transition_id).trigger
                except KeyError:
                    trigger = None
            else:
                break
        if history_item:
            return text_to_html((history_item.comment or '').strip())

    @property
    def next_step(self):
        """Next step getter"""
        transition = self.view.transition
        return self.request.localizer.translate(transition.user_data.get('next_step')) \
            if 'next_step' in transition.user_data else None


#
# Publication request
#

@ajax_form_config(name='wf-propose.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class SharedContentPublicationRequestForm(SharedContentWorkflowTransitionForm):
    """Shared content publication request form"""

    legend = _("Publication settings")

    @property
    def fields(self):
        pub_fields = ('publication_effective_date', 'push_end_date',
                      'publication_expiration_date')
        state = IWorkflowState(self.context)
        if state.version_id > 1:
            pub_fields += ('displayed_publication_date',)
        return Fields(IWorkflowTransitionInfo) + \
            Fields(IWorkflowPublicationInfo).select(*pub_fields) + \
            Fields(IWorkflowRequestUrgencyInfo) + \
            Fields(IWorkflowCommentInfo)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        pub_info = IWorkflowPublicationInfo(self.context)
        widget = self.widgets.get('publication_effective_date')
        if widget is not None:
            widget.required = True
            widget.value = tztime(datetime.now(timezone.utc)).isoformat()
        if pub_info.push_end_date:
            widget = self.widgets.get('push_end_date')
            if widget is not None:
                widget.value = tztime(pub_info.push_end_date).isoformat()
        if pub_info.publication_expiration_date:
            widget = self.widgets.get('publication_expiration_date')
            if widget is not None:
                widget.value = tztime(pub_info.publication_expiration_date).isoformat()
        widget = self.widgets.get('displayed_publication_date')
        if widget is not None:
            widget.value = pub_info.displayed_publication_date

    def create_and_add(self, data):
        data = data.get(self, data)
        pub_info = IWorkflowPublicationInfo(self.context)
        pub_info.publication_effective_date = data.get('publication_effective_date')
        pub_info.push_end_date = data.get('push_end_date')
        pub_info.publication_expiration_date = data.get('publication_expiration_date')
        if 'displayed_publication_date' in data:
            pub_info.displayed_publication_date = data.get('displayed_publication_date')
        return super().create_and_add(data)


@subscriber(IDataExtractedEvent, form_selector=SharedContentPublicationRequestForm)
def handle_publication_request_form_data_extraction(event):
    """Handle publication request form data extraction"""
    data = event.data
    if not data.get('publication_effective_date'):
        event.form.widgets.errors += (Invalid(_("Publication start date is required")),)


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationRequestForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationRequestFormHelp(AlertMessage):
    """Shared content publication request form help"""

    status = 'info'

    _message = _("This publication request is going to be transmitted to a content manager.")


#
# Request publication cancel form
#

@ajax_form_config(name='wf-cancel-propose.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class SharedContentPublicationRequestCancelForm(SharedContentWorkflowTransitionForm):
    """Shared content publication request cancel form"""


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationRequestCancelForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationRequestCancelFormHelp(AlertMessage):
    """Shared content publication request cancel form help"""

    status = 'info'

    _message = _("If you cancel this publication request, this content will be updatable again.")


#
# Refuse publication form
#

@ajax_form_config(name='wf-refuse.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=PUBLISH_CONTENT_PERMISSION)
class SharedContentPublicationRequestRefuseForm(SharedContentWorkflowTransitionForm):
    """Shared content publication request refuse form"""

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'comment' in self.widgets:
            self.widgets['comment'].required = True


@subscriber(IDataExtractedEvent, form_selector=SharedContentPublicationRequestRefuseForm)
def handle_publication_request_refuse_form_data_extraction(event):
    """Handle publication request refuse form data extraction"""
    comment = (event.data.get('comment') or '').strip()
    if not comment:
        event.form.widgets.errors += (Invalid(_("A comment is required")),)


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationRequestRefuseForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationRequestRefuseFormHelp(AlertMessage):
    """Shared content publication request refuse form help"""

    status = 'info'

    _message = _("As a content manager, you considerate that this content can't be published "
                 "'as is'.<br />"
                 "The contributor will be notified of this and will be able to update the "
                 "content before doing a new publication request.")
    message_renderer = 'markdown'


#
# Publication form
#

@ajax_form_config(name='wf-publish.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=PUBLISH_CONTENT_PERMISSION)
class SharedContentPublicationForm(SharedContentWorkflowTransitionForm):
    """Shared content publication form"""

    legend = _("Publication settings")

    @property
    def fields(self):
        pub_fields = ('publication_effective_date', 'push_end_date',
                      'publication_expiration_date')
        state = IWorkflowState(self.context)
        if state.version_id > 1:
            pub_fields += ('displayed_publication_date',)
        return Fields(IWorkflowTransitionInfo) + \
            Fields(IWorkflowPublicationInfo).select(*pub_fields) + \
            Fields(IWorkflowCommentInfo)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        pub_info = IWorkflowPublicationInfo(self.context)
        widget = self.widgets.get('publication_effective_date')
        if widget is not None:
            widget.required = True
            now = datetime.now(timezone.utc)
            if pub_info.publication_effective_date:
                widget.value = tztime(max(now, pub_info.publication_effective_date)).isoformat()
            else:
                widget.value = tztime(now).isoformat()
        if pub_info.push_end_date:
            widget = self.widgets.get('push_end_date')
            if widget is not None:
                widget.value = tztime(pub_info.push_end_date).isoformat()
        if pub_info.publication_expiration_date:
            widget = self.widgets.get('publication_expiration_date')
            if widget is not None:
                widget.value = tztime(pub_info.publication_expiration_date).isoformat()
        widget = self.widgets.get('displayed_publication_date')
        if widget is not None:
            widget.value = pub_info.displayed_publication_date

    def create_and_add(self, data):
        data = data.get(self, data)
        pub_info = IWorkflowPublicationInfo(self.context)
        pub_info.publication_effective_date = data.get('publication_effective_date')
        pub_info.push_end_date = data.get('push_end_date')
        pub_info.publication_expiration_date = data.get('publication_expiration_date')
        if 'displayed_publication_date' in data:
            pub_info.displayed_publication_date = data.get('displayed_publication_date')
        now = datetime.now(timezone.utc)
        if pub_info.publication_effective_date <= now:
            # immediate publication
            return super().create_and_add(data)
        # delayed publication: we schedule a publication task
        transition = self.transition.user_data.get('prepared_transition')
        if transition is None:
            raise NoTransitionAvailableError(PROPOSED, PUBLISHED)
        info = IWorkflowInfo(self.context)
        info.fire_transition(transition.transition_id, comment=data.get('comment'))
        info.fire_automatic()
        IWorkflowState(self.context).state_urgency = data.get('urgent_request') or False
        self.request.registry.notify(ObjectModifiedEvent(self.context))
        return info


@subscriber(IDataExtractedEvent, form_selector=SharedContentPublicationForm)
def handle_publication_form_data_extraction(event):
    """Handle publication form data extraction"""
    data = event.data
    if not data.get('publication_effective_date'):
        event.form.widgets.errors += (Invalid(_("Publication start date is required")),)


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationFormHelp(AlertMessage):
    """Shared content publication form help"""

    status = 'info'

    _message = _("As a manager, you considerate that this content is complete and can be "
                 "published 'as is'.<br />"
                 "This operation will make the content publicly available (except if "
                 "restricted access has been set).")
    message_renderer = 'markdown'


#
# Pre-publication cancel form
#

@ajax_form_config(name='wf-cancel-publish.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class SharedContentPublicationCancelForm(SharedContentWorkflowTransitionForm):
    """Shared content publication cancel form"""


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationCancelForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationCancelFormHelp(AlertMessage):
    """Shared content publication cancel form help"""

    status = 'info'

    _message = _("After cancelling the publication, the content will return to proposed "
                 "publication state.")


#
# Publication retire request form
#

@ajax_form_config(name='wf-retiring.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class SharedContentPublicationRetireRequestForm(SharedContentWorkflowTransitionForm):
    """Shared content publication retire request form"""

    fields = Fields(IWorkflowTransitionInfo) + \
        Fields(IWorkflowRequestUrgencyInfo) + \
        Fields(IWorkflowCommentInfo)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'comment' in self.widgets:
            self.widgets['comment'].required = True


@subscriber(IDataExtractedEvent, form_selector=SharedContentPublicationRetireRequestForm)
def handle_publication_retire_request_form_data_extraction(event):
    """Handle publication retire request form data extraction"""
    comment = (event.data.get('comment') or '').strip()
    if not comment:
        event.form.widgets.errors += (Invalid(_("A comment is required")),)


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationRetireRequestForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationRetireRequestFormHelp(AlertMessage):
    """Shared content publication retire request form help"""

    status = 'info'

    _message = _("You considerate that the currently published version should no more be "
                 "publicly visible.<br />"
                 "WARNING: the content will remain visible until a manager validate your "
                 "request.")
    message_renderer = 'markdown'


#
# Publication retire cancel form
#

@ajax_form_config(name='wf-cancel-retiring.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class SharedContentPublicationRetireRequestCancelForm(SharedContentWorkflowTransitionForm):
    """Shared content publication retire request cancel form"""


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationRetireRequestCancelForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationRetireRequestCancelFormHelp(AlertMessage):
    """Shared content publication retire request form help"""

    status = 'info'

    _message = _("After cancelling this request, the content will return to it's normal "
                 "published state.")


#
# Publication retire form
#

@ajax_form_config(name='wf-retire.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=PUBLISH_CONTENT_PERMISSION)
class SharedContentPublicationRetireForm(SharedContentWorkflowTransitionForm):
    """Shared content publication retire form"""


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationRetireForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationRetireFormHelp(AlertMessage):
    """Shared content publication retire form help"""

    status = 'info'

    _message = _("As a content manager, you considerate that this content should no longer be "
                 "published.<br />"
                 "Retired content won't be visible anymore, but it can be updated and published "
                 "again, or archived.")
    message_renderer = 'markdown'


#
# Publication archive request form
#

@ajax_form_config(name='wf-archiving.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class SharedContentPublicationArchiveRequestForm(SharedContentWorkflowTransitionForm):
    """Shared content publication request archive form"""

    fields = Fields(IWorkflowTransitionInfo) + \
        Fields(IWorkflowRequestUrgencyInfo) + \
        Fields(IWorkflowCommentInfo)


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationArchiveRequestForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationArchiveRequestFormHelp(AlertMessage):
    """Shared content publication archive request form help"""

    status = 'info'

    _message = _("This content is already retired and not visible.<br />"
                 "After archiving, it will be backed up but you will not be able to publish "
                 "it again except by creating a new version.")
    message_renderer = 'markdown'


#
# Publication archive cancel form
#

@ajax_form_config(name='wf-cancel-archiving.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class SharedContentPublicationArchiveCancelForm(SharedContentWorkflowTransitionForm):
    """Shared content publication archive request cancel form"""


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationArchiveCancelForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationArchiveCancelFormHelp(AlertMessage):
    """Shared content publication archive request cancel form help"""

    status = 'info'

    _message = _("After cancelling this request, the content will return to it's previous "
                 "retired state.")


#
# Publication archive form
#

@ajax_form_config(name='wf-archive.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=PUBLISH_CONTENT_PERMISSION)
class SharedContentPublicationArchiveForm(SharedContentWorkflowTransitionForm):
    """Shared content publication archive form"""


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentPublicationArchiveForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentPublicationArchiveFormHelp(AlertMessage):
    """Shared content publication archive form help"""

    status = 'info'

    _message = _("As a manager, you considerate that this content must be archived.<br />"
                 "After archiving, it will be backed up but you will not be able to publish it "
                 "again except by creating a new version.")
    message_renderer = 'markdown'


#
# Clone form
#

@ajax_form_config(name='wf-clone.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=CREATE_VERSION_PERMISSION)
class SharedContentCloneForm(SharedContentWorkflowTransitionForm):
    """Shared content clone form"""

    def create_and_add(self, data):
        data = data.get(self, data)
        info = IWorkflowInfo(self.context)
        return info.fire_transition_toward(DRAFT, comment=data.get('comment'))


@adapter_config(required=(IWorkflowVersion, IAdminLayer, SharedContentCloneForm),
                provides=IAJAXFormRenderer)
class SharedContentCloneFormRenderer(ContextRequestViewAdapter):
    """Shared content clone form renderer"""

    def render(self, changes):
        if changes is None:
            return None
        return {
            'status': 'redirect',
            'location': absolute_url(changes, self.request, 'admin')
        }


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer,
                view=SharedContentCloneFormRenderer,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentCloneFormRendererHelp(AlertMessage):
    """Shared content clone form help"""

    status = 'info'

    _message = _("You considerate that the currently published must evolve.<br />"
                 "By creating a new version, you can update it's content without impacting "
                 "the currently published one.<br />"
                 "When the new version will be complete, you will be able to make a new "
                 "publication request to replace the currently published version (which will "
                 "be archived automatically).")
    message_renderer = 'markdown'


#
# Delete form
#

@ajax_form_config(name='wf-delete.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_CONTENT_PERMISSION)
class SharedContentDeleteForm(SharedContentWorkflowTransitionForm):
    """Shared content delete form"""

    @property
    def fields(self):
        fields = super().fields
        state = IWorkflowState(self.context)
        if state.version_id == 1:  # content deletion
            fields = fields.omit('comment')
        return fields

    def update_actions(self):
        super().update_actions()
        action = self.actions.get('action')
        if action is not None:
            state = IWorkflowState(self.context)
            if state.version_id == 1:  # remove the first and only version => remove all
                action.add_class('btn-danger')
                action.title = _("Delete definitively")

    def create_and_add(self, data):
        data = data.get(self, data)
        state = IWorkflowState(self.context)
        if state.version_id == 1:  # remove the first and only version => remove all
            content = get_parent(self.context, ISharedContent)
            container = get_parent(content, IContainer)
            del container[content.__name__]
            target = self.request.registry.queryMultiAdapter((container, self.request, self),
                                                             IWorkflowDeleteFormTarget)
        else:
            versions = IWorkflowVersions(self.context)
            versions.remove_version(state.version_id,
                                    state=DELETED, comment=data.get('comment'))
            target = versions.get_last_versions(count=1)[0]
        return target


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedContentDeleteForm),
                provides=IWorkflowDeleteFormTarget)
def shared_content_workflow_delete_form_target(context, request, form):
    """Shared content workflow delete form target"""
    return context


@adapter_config(required=(ISharedToolInnerFolder, IAdminLayer, SharedContentDeleteForm),
                provides=IWorkflowDeleteFormTarget)
def shared_tool_folder_folder_workflow_delete_form_target(context, request, form):
    """Shared tool inner folder workflow delete form target"""
    return get_parent(context, IBaseSharedTool)


@adapter_config(required=(IWorkflowVersion, IAdminLayer, SharedContentDeleteForm),
                provides=IAJAXFormRenderer)
class SharedContentDeleteFormRenderer(ContextRequestViewAdapter):
    """Shared content delete form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        return {
            'status': 'redirect',
            'location': absolute_url(changes, self.request, 'admin')
        }


@viewlet_config(name='help',
                context=IWorkflowVersion, layer=IAdminLayer, view=SharedContentDeleteForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentDeleteFormHelp(AlertMessage):
    """Shared content delete form help"""

    status = 'danger'

    @property
    def _message(self):
        state = IWorkflowState(self.context)
        if state.version_id == 1:
            return _("This content was never published and is going to be deleted.<br />"
                     "If you confirm deletion, it won't be possible to restore it.")
        return _("The content version is going to be definitely deleted.<br />"
                 "Will only remain the currently published or archived versions.")

    message_renderer = 'markdown'
