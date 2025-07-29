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

import json
from datetime import datetime, timezone

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Any, Eq
from pyramid.decorator import reify
from zope.interface import Interface, implementer
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import Bool, Choice, TextLine
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_catalog.query import CatalogResultSet
from pyams_content.interfaces import MANAGE_SITE_PERMISSION
from pyams_content.shared.common.interfaces import CONTENT_MANAGER_CONTRIBUTORS, IBaseSharedTool, ISharedToolRoles, \
    IWfSharedContent, IWfSharedContentRoles, SHARED_CONTENT_TYPES_VOCABULARY
from pyams_content.shared.common.zmi.dashboard import DashboardTable
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces import HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.interfaces import IPagelet, PageletCreatedEvent
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.schema import PrincipalField
from pyams_security.utility import get_principal
from pyams_security_views.zmi.interfaces import IObjectSecurityMenu
from pyams_sequence.interfaces import ISequentialIdInfo, ISequentialIntIds
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager, IHeaderViewletManager
from pyams_skin.schema.button import ResetButton, SubmitButton
from pyams_skin.viewlet.help import AlertMessage
from pyams_table.column import CheckBoxColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.list import unique_iter
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_viewlet.viewlet import EmptyViewlet, viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowState, IWorkflowVersions
from pyams_workflow.versions import WorkflowHistoryItem, get_last_version
from pyams_zmi.form import AdminAddForm
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.search import SearchForm, SearchResultsView, SearchView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


def set_owner(context, request, new_owner, keep_owner_as_contributor=False):
    """Set content owner"""
    updated = False
    workflow = IWorkflow(context)
    translate = request.localizer.translate
    for version in IWorkflowVersions(context).get_versions():
        state = IWorkflowState(version)
        if state.state in workflow.readonly_states:
            continue
        roles = IWfSharedContentRoles(version, None)
        if roles is not None:
            [previous_owner] = roles.owner
            if previous_owner != new_owner:
                roles.owner = {new_owner}
                contributors = roles.contributors.copy()  # don't modify contributors in place!!
                if keep_owner_as_contributor:
                    contributors |= {previous_owner}
                else:
                    if previous_owner in contributors:
                        contributors.remove(previous_owner)
                roles.contributors = contributors
                state.history.append(
                    WorkflowHistoryItem(date=tztime(datetime.now(timezone.utc)),
                                        source_state=state.state,
                                        target_state=state.state,
                                        transition_id=MISSING_INFO,
                                        principal=request.principal.id,
                                        comment=translate(_("Owner changed: {} -> {}")).format(
                                            get_principal(request, previous_owner).title,
                                            get_principal(request, new_owner).title
                                        )))
                request.registry.notify(ObjectModifiedEvent(version))
                updated = True
    return updated


#
# Bulk owner change
#

@viewlet_config(name='change-owner.menu',
                context=IBaseSharedTool, layer=IAdminLayer,
                manager=IObjectSecurityMenu, weight=300,
                permission=MANAGE_SITE_PERMISSION)
class SharedToolOwnerChangeMenu(NavigationMenuItem):
    """Shared tool owner change menu"""

    label = _("Change owner")
    href = '#change-owner.html'


class ISharedToolOwnerChangeSearchInfo(Interface):
    """Shared tool owner change search form fields"""

    old_owner = Choice(title=_("Current owner"),
                       description=_("This is the name of the current owner"),
                       vocabulary=CONTENT_MANAGER_CONTRIBUTORS,
                       required=False)


class SharedToolOwnerChangeSearchForm(SearchForm):
    """Shared tool owner change search form"""

    title = _("Contents owner change form")

    ajax_form_handler = 'change-owner-search-results.html'
    _edit_permission = MANAGE_SITE_PERMISSION

    fields = Fields(ISharedToolOwnerChangeSearchInfo)


@pagelet_config(name='change-owner.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=MANAGE_SITE_PERMISSION)
class SharedToolOwnerChangeView(SearchView):
    """Shared tool owner change view"""

    title = _("Contents owner search form")
    header_label = _("Contents search form")
    search_form = SharedToolOwnerChangeSearchForm


class SharedToolOwnerChangeSearchResultsTable(DashboardTable):
    """Shared tool owner search results table"""

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        modules = attributes.get('table', {}).get('data-ams-modules', '')
        attributes.setdefault('table', {}).update({
            'data-ams-modules': f'{modules} container',
            'data-buttons': json.dumps(['copy', 'csv', 'print'])
        })
        return attributes


@adapter_config(name='checked',
                required=(IBaseSharedTool, IAdminLayer, SharedToolOwnerChangeSearchResultsTable),
                provides=IColumn)
class SharedToolOwnerChangeCheckedColumn(CheckBoxColumn):
    """Shared tool owner change checked column"""

    weight = 1
    sortable = 'false'

    def get_item_key(self, item):
        return 'owner_form.widgets.selection-input'

    def get_item_value(self, item):
        return str(ISequentialIdInfo(item).oid)

    def is_selected(self, item):
        return False

    def render_head_cell(self):
        return ('<input type="checkbox" '
                '       data-ams-change-handler="MyAMS.container.selectAllElements" />')

    def render_cell(self, item):
        return super().render_cell(item).replace(' />',
                                                 ' data-ams-click-handler="MyAMS.container.selectElement" '
                                                 ' data-ams-stop-propagation="true" />')


@adapter_config(required=(IBaseSharedTool, IPyAMSLayer, SharedToolOwnerChangeSearchResultsTable),
                provides=IValues)
class SharedToolOwnerChangeSearchResultsValues(ContextRequestViewAdapter):
    """Shared tool owner search results table values"""

    def get_params(self, data):
        intids = get_utility(IIntIds)
        catalog = get_utility(ICatalog)
        vocabulary = getVocabularyRegistry().get(self.context, SHARED_CONTENT_TYPES_VOCABULARY)
        params = And(Eq(catalog['parents'], intids.register(self.context)),
                     Any(catalog['content_type'], vocabulary.by_value.keys()))
        owner = data.get('old_owner')
        if owner:
            params &= Eq(catalog['role:owner'], owner)
        return params

    @property
    def values(self):
        """Search results values getter"""
        form = SharedToolOwnerChangeSearchForm(self.context, self.request)
        form.update()
        data, _errors = form.extract_data()
        params = self.get_params(data)
        catalog = get_utility(ICatalog)
        yield from unique_iter(
            map(get_last_version,
                CatalogResultSet(CatalogQuery(catalog).query(
                    params, sort_index='modified_date', reverse=True))))


class ISharedToolOwnerChangeFormFields(Interface):
    """Shared tool owner change form fields interface"""

    selection = TextLine(title=_("Selected items"),
                         required=False)

    new_owner = PrincipalField(title=_("New owner"),
                               description=_("Selected contents ownership will be assigned to "
                                             "selected principal"),
                               required=True)

    set_as_tool_contributor = Bool(title=_("Set as tool contributor"),
                                   description=_("If 'yes', selected owner will be granted the "
                                                 "contributor role on shared tool; otherwise, he "
                                                 "will get this role only on selected contents"),
                                   required=False,
                                   default=False)

    keep_owner_as_contributor = Bool(title=_("Keep previous owner as contributor"),
                                     description=_("If 'yes', the previous owner will still be "
                                                   "able to modify selected contents"),
                                     required=False,
                                     default=False)


class ISharedToolOwnerChangeFormActions(Interface):
    """Shared tool owner change form actions interface"""

    assign = SubmitButton(name='assign',
                          title=_("Change owner"))


@ajax_form_config(name='change-contents-owner.html',
                  context=IBaseSharedTool, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_PERMISSION)
@implementer(IObjectData)
class SharedToolOwnerChangeForm(AdminAddForm):
    """Shared tool owner change form"""

    prefix = 'owner_form.'
    title = None
    legend = _("New owner")
    hide_section = True

    fields = Fields(ISharedToolOwnerChangeFormFields)
    buttons = Buttons(ISharedToolOwnerChangeFormActions)

    @property
    def object_data(self):
        return {
            'ams-form-init-data-callback': 'MyAMS.container.getSelectedElements',
            'ams-container-source': 'owner_form.widgets.selection-input',
            'ams-container-target': 'owner_form.widgets.selection'
        }

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        selection = self.widgets.get('selection')
        if selection is not None:
            selection.mode = HIDDEN_MODE

    @handler(buttons['assign'])
    def handle_assign(self, action):
        super().handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        translate = self.request.localizer.translate
        selection = data.get('selection')
        if not selection:
            self.status = translate(_("Can't change owner for empty selection!"))
            return
        selection = list(map(int, selection.split(',')))
        new_owner = data.get('new_owner')
        # check tool contributor
        if data.get('set_as_tool_contributor'):
            roles = ISharedToolRoles(self.context)
            contributors = roles.contributors.copy()
            if new_owner not in contributors:
                contributors |= {new_owner}
                roles.contributors = contributors
        # set content owner
        updated = 0
        sequential_ids = get_utility(ISequentialIntIds)
        for oid in selection:
            content = sequential_ids.query_object_from_oid(oid)
            if content is not None:
                if set_owner(content, self.request, new_owner,
                             data.get('keep_owner_as_contributor')):
                    updated += 1
        return {
            'selected': len(selection),
            'updated': updated
        }


@adapter_config(required=(IBaseSharedTool, IAdminLayer, SharedToolOwnerChangeForm),
                provides=IAJAXFormRenderer)
class SharedToolOwnerChangeFormRenderer(AJAXFormRenderer):
    """Shared tool owner change form renderer"""

    def render(self, changes):
        translate = self.request.localizer.translate
        if not changes:
            return {
                'status': 'info',
                'message': translate(_("Empty selection, no content owner was changed."))
            }
        selected = changes.get('selected', 0)
        changed = changes.get('updated', 0)
        if not changed:
            return {
                'status': 'info',
                'message': translate(_("{} contents selected, no owner changed !")).format(selected)
            }
        return {
            'status': 'success',
            'message': translate(_("{} contents selected, owner changed successfully for {} "
                                   "contents")).format(selected, changed),
            'callbacks': [{
                'callback': "MyAMS.container.removeSelectedElements",
                'options': {
                    'source': 'owner_form.widgets.selection-input'
                }
            }]
        }


@pagelet_config(name='change-owner-search-results.html',
                context=IBaseSharedTool, layer=IPyAMSLayer,
                permission=MANAGE_SITE_PERMISSION, xhr=True)
@template_config(template='templates/owner-change.pt',
                 layer=IPyAMSLayer)
class SharedToolOwnerChangeSearchResultsView(SearchResultsView):
    """Shared tool owner change search results view"""

    table_label = _("Search results")
    table_class = SharedToolOwnerChangeSearchResultsTable

    owner_change_form = None

    def __init__(self, context, request):
        super().__init__(context, request)
        request.registry.notify(PageletCreatedEvent(self))

    def update(self):
        super().update()
        if len(self.table.values) > 0:
            form = self.request.registry.queryMultiAdapter((self.context, self.request), IPagelet,
                                                           name='change-contents-owner.html')
            if form is not None:
                form.update()
                self.owner_change_form = form


@viewlet_config(name='pyams.content_header',
                layer=IAdminLayer, view=SharedToolOwnerChangeSearchResultsView,
                manager=IHeaderViewletManager, weight=10)
class SharedToolOwnerChangeSearchResultsViewHeaderViewlet(EmptyViewlet):
    """Shared tool owner change search results view header viewlet"""

    def render(self):
        return '<h1 class="mt-3"></h1>'


#
# Shared content owner change
#

@viewlet_config(name='change-owner.menu',
                context=IWfSharedContent, layer=IAdminLayer,
                manager=IObjectSecurityMenu, weight=10,
                permission=MANAGE_SITE_PERMISSION)
class WfSharedContentOwnerChangeMenu(NavigationMenuItem):
    """Shared content owner change menu"""

    label = _("Change owner")
    href = '#change-owner.html'


class IWfSharedContentOwnerChangeInfo(Interface):
    """Shared content owner change form fields"""

    new_owner = PrincipalField(title=_("New owner"),
                               description=_("The selected user will become the new content's owner"))

    keep_owner_as_contributor = Bool(title=_("Keep previous owner as contributor"),
                                     description=_("If 'yes', the previous owner will still be "
                                                   "able to modify this content"),
                                     required=False,
                                     default=False)


class IWfSharedContentOwnerChangeButtons(Interface):
    """Shared content owner change form buttons"""

    change = SubmitButton(name='change', title=_("Change owner"))
    reset = ResetButton(name='reset', title=_("Cancel"))


@ajax_form_config(name='change-owner.html',
                  context=IWfSharedContent, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_PERMISSION)
class WfSharedContentOwnerChangeForm(AdminAddForm):
    """Shared content owner change form"""

    title = _("Change content owner")
    legend = _("New owner selection")

    fields = Fields(IWfSharedContentOwnerChangeInfo)
    buttons = Buttons(IWfSharedContentOwnerChangeButtons)

    @handler(buttons['change'])
    def handle_change(self, action):
        super().handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        new_owner = data.get('new_owner')
        set_owner(self.context, self.request, new_owner,
                  data.get('keep_owner_as_contributor'))


@viewlet_config(name='help',
                context=IWfSharedContent, layer=IAdminLayer,
                view=WfSharedContentOwnerChangeForm,
                manager=IFormHeaderViewletManager, weight=10)
class SharedContentOwnerChangeFormHelp(AlertMessage):
    """Shared content owner change form help"""

    status = 'info'

    _message = _("All versions of this content which are not archived will be transferred to "
                 "newly selected owner")
    message_renderer = 'markdown'


@adapter_config(required=(IWfSharedContent, IAdminLayer, WfSharedContentOwnerChangeForm),
                provides=IAJAXFormRenderer)
class SharedContentOwnerChangeFormAJAXRenderer(ContextRequestViewAdapter):
    """Shared content owner change form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        return {
            'status': 'reload'
        }
