#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content.feature.redirect.zmi.container module

This module provides management interface components for redirection manager.
"""

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import Eq
from pyramid.renderers import render
from pyramid.view import view_config
from zope.interface import Interface
from zope.schema import Bool, TextLine

from pyams_catalog.query import CatalogResultSet
from pyams_content.feature.redirect.interfaces import IRedirectionManager, IRedirectionManagerTarget
from pyams_content.feature.redirect.zmi.interfaces import IRedirectionsTable
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer, IUserSkinnable
from pyams_layer.skin import apply_skin
from pyams_pagelet.pagelet import pagelet_config
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_skin.interfaces.viewlet import IContentSuffixViewletManager, IHelpViewletManager
from pyams_skin.schema.button import CloseButton, SubmitButton
from pyams_skin.viewlet.actions import ContextAction
from pyams_skin.viewlet.help import AlertMessage
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_utility
from pyams_utils.request import copy_request
from pyams_viewlet.viewlet import EmptyViewlet, viewlet_config
from pyams_workflow.interfaces import IWorkflow, IWorkflowPublicationInfo, IWorkflowVersions
from pyams_zmi.form import AdminModalAddForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import ISiteManagementMenu, IToolbarViewletManager
from pyams_zmi.table import AttributeSwitcherColumn, I18nColumnMixin, IconColumn, ReorderColumn, SortableTable, \
    TableAdminView, TrashColumn
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='redirections.menu',
                context=IRedirectionManagerTarget, layer=IAdminLayer,
                manager=ISiteManagementMenu, weight=25,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class RedirectionManagerMenu(NavigationMenuItem):
    """Redirections manager menu"""

    label = _("Redirections")
    icon_class = 'fas fa-map-signs'

    href = '#redirections.html'


@pagelet_config(name='redirections.html',
                context=IRedirectionManagerTarget, layer=IPyAMSLayer,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class RedirectionManagerView(TableAdminView):
    """Redirections manager view"""

    title = _("Site redirections")
    table_class = IRedirectionsTable
    table_label = _("List of site redirections")


@viewlet_config(name='redirections.help',
                context=IRedirectionManagerTarget, layer=IAdminLayer, view=RedirectionManagerView,
                manager=IHelpViewletManager, weight=10)
class RedirectionManagerHelp(AlertMessage):
    """Redirection manager help"""

    status = 'info'
    css_class = 'mx-2'

    _message = _("""Redirection rules are used to provide redirections responses when a request generates
a famous « 404 NotFound » error.<br />
Redirections are particularly useful when you are migrating from a previous site and don't want to lose
your SEO.<br />
You can define a set of rules which will be applied on every \"NotFound\" exception; rules are based on
regular expressions which are applied to input URL: if the rule is \"matching\", the target URL is rewritten
and a \"Redirect\" response is send.<br />
You can chain rules together: when a rule is chained, it's rewritten URL is passed as input URL to the
next rule, until a matching rule is found.
""")
    message_renderer = 'markdown'


@factory_config(IRedirectionsTable)
class RedirectionsTable(SortableTable):
    """Redirections table"""

    container_class = IRedirectionManager

    display_if_empty = True


@adapter_config(required=(IRedirectionManagerTarget, IAdminLayer, IRedirectionsTable),
                provides=IValues)
class RedirectionsTableValues(ContextRequestViewAdapter):
    """Redirections table values adapter"""

    @property
    def values(self):
        yield from IRedirectionManager(self.context).values()


@adapter_config(name='reorder',
                required=(IRedirectionManagerTarget, IAdminLayer, IRedirectionsTable),
                provides=IColumn)
class RedirectionTableReorderColumn(ReorderColumn):
    """Redirections table reorder column"""


@view_config(name='reorder.json',
             context=IRedirectionManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_SITE_ROOT_PERMISSION)
def reorder_redirections_container(request):
    """Reorder redirections container"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': True
    }


@adapter_config(name='active',
                required=(IRedirectionManagerTarget, IAdminLayer, IRedirectionsTable),
                provides=IColumn)
class RedirectionsTableActiveColumn(AttributeSwitcherColumn):
    """Redirections table active column"""

    hint = _("Click icon to enable or disable redirection rule")

    attribute_name = 'active'
    attribute_switcher = 'switch-active-rule.json'

    icon_on_class = 'far fa-check-square'
    icon_off_class = 'far fa-square opacity-50'

    weight = 5


@view_config(name='switch-active-rule.json',
             context=IRedirectionManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_SITE_ROOT_PERMISSION)
def switch_active_rule(request):
    """Switch active redirection rule"""
    return switch_element_attribute(request)


@adapter_config(name='chain',
                required=(IRedirectionManagerTarget, IAdminLayer, IRedirectionsTable),
                provides=IColumn)
class RedirectionsTableChainColumn(AttributeSwitcherColumn):
    """Redirections table chain column"""

    hint = _("Click icon to enable or disable rule chain")

    attribute_name = 'chained'
    attribute_switcher = 'switch-chained-rule.json'

    icon_on_class = 'fas fa-link'
    icon_off_class = 'fas fa-unlink opacity-50'

    weight = 6


@view_config(name='switch-chained-rule.json',
             context=IRedirectionManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_SITE_ROOT_PERMISSION)
def switch_chained_rule(request):
    """Switch chained redirection rule"""
    return switch_element_attribute(request)


@adapter_config(name='label',
                required=(IRedirectionManagerTarget, IPyAMSLayer, IRedirectionsTable),
                provides=IColumn)
class RedirectionsTableLabelColumn(I18nColumnMixin, GetAttrColumn):
    """Redirections container label column"""

    i18n_header = _("Rule label")
    attr_name = 'label'

    weight = 10


@adapter_config(name='pattern',
                required=(IRedirectionManagerTarget, IPyAMSLayer, IRedirectionsTable),
                provides=IColumn)
class RedirectionsTablePatternColumn(I18nColumnMixin, GetAttrColumn):
    """Redirections container pattern column"""

    i18n_header = _("URL pattern")
    attr_name = 'url_pattern'

    weight = 15


MISSING_TARGET = object()


@adapter_config(name='visible',
                required=(IRedirectionManagerTarget, IPyAMSLayer, IRedirectionsTable),
                provides=IColumn)
class RedirectionsTableVisibleColumn(IconColumn):
    """Redirections container visible column"""

    weight = 19

    def __init__(self, context, request, table):
        super().__init__(context, request, table)
        self.targets = {}

    def get_status(self, reference):
        status = self.targets.get(reference, MISSING_TARGET)
        if status is not MISSING_TARGET:
            return status
        status = ''
        hint = ''
        catalog = get_utility(ICatalog)
        params = Eq(catalog['oid'], reference)
        results = list(CatalogResultSet(CatalogQuery(catalog).query(params)))
        if results:
            target = results[0]
            versions = IWorkflowVersions(target, None)
            if versions is not None:
                workflow = IWorkflow(target, None)
                versions = versions.get_versions(workflow.published_states)
                if versions:
                    target = versions.pop()
                else:
                    target = None
                    status = 'fas fa-eye-slash text-danger'
                    hint = _("Target has no published version")
            if target is not None:
                info = IWorkflowPublicationInfo(target, None)
                if info is not None:
                    if info.is_published():
                        status = 'fas fa-eye'
                        hint = _("Target is published")
                    else:
                        status = 'fas fa-eye-slash text-danger'
                        hint = _("Target is not published")
        self.targets[reference] = result = {
            'status': status,
            'hint': hint
        }
        return result

    def get_icon_class(self, item):
        if item.reference:
            return self.get_status(item.reference).get('status', 'fas fa-question')
        return 'fas fa-external-link-alt'

    def get_icon_hint(self, item):
        if item.reference:
            hint = self.get_status(item.reference).get('hint')
            return self.request.localizer.translate(hint)
        return self.request.localizer.translate(_("External link"))


@adapter_config(name='target',
                context=(IRedirectionManagerTarget, IPyAMSLayer, IRedirectionsTable),
                provides=IColumn)
class RedirectionsContainerTargetColumn(I18nColumnMixin, GetAttrColumn):
    """Redirections container target column"""

    i18n_header = _("Target")
    attr_name = 'target_url'

    weight = 20

    def get_value(self, obj):
        if obj.reference:
            target = obj.target
            if target is not None:
                return '{0} ({1})'.format(II18n(target).query_attribute('title', request=self.request),
                                          ISequentialIdInfo(target).get_short_oid())
            return self.request.localizer.translate(_("Internal reference: {0} (not found)")).format(obj.reference)
        return super().get_value(obj)


@adapter_config(name='trash',
                required=(IRedirectionManagerTarget, IAdminLayer, IRedirectionsTable),
                provides=IColumn)
class RedirectionsContainerTrashColumn(TrashColumn):
    """Redirections table trash column"""

    object_data = {
        'ams-modules': 'container',
        'ams-delete-target': 'delete-redirection-rule.json'
    }


@view_config(name='delete-redirection-rule.json',
             context=IRedirectionManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_SITE_ROOT_PERMISSION)
def delete_rule(request):
    """Delete redirection rule"""
    return delete_container_element(request, container_factory=IRedirectionManager)


#
# Redirection rules testing
#

@viewlet_config(name='test-redirections.action',
                context=IRedirectionManagerTarget, layer=IAdminLayer, view=IRedirectionsTable,
                manager=IToolbarViewletManager, weight=800,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class RedirectionManagerTestAction(ContextAction):
    """Redirection rule test action"""

    css_class = 'btn-sm mx-2'
    icon_class = 'fas fa-magic'
    label = _("Test rules")

    href = 'test-redirections.html'
    modal_target = True


class IRedirectionsManagerTestFields(Interface):
    """Redirections manager test fields"""

    source_url = TextLine(title=_("Test URL"),
                          description=_("Test URL must only contain absolute path, without protocol and "
                                        "hostname, but can include optional query parameters"),
                          required=True)

    check_inactive_rules = Bool(title=_("Test inactive rules?"),
                                description=_("If 'yes', inactive rules will also be tested"),
                                required=True,
                                default=False)


class IRedirectionsManagerTestButtons(Interface):
    """Redirections manager test form buttons"""

    test = SubmitButton(name='test', title=_("Test rules"))
    close = CloseButton(name='close', title=_("Close"))


@ajax_form_config(name='test-redirections.html',
                  context=IRedirectionManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class RedirectionManagerTestForm(AdminModalAddForm):
    """Redirection manager test form"""

    fields = Fields(IRedirectionsManagerTestFields)
    buttons = Buttons(IRedirectionsManagerTestButtons)

    modal_class = 'modal-max'

    @property
    def ajax_form_target(self):
        return f'#{self.id}_test_result'

    @handler(buttons['test'])
    def handle_test(self, action):
        self.handle_add(self, action)

    def create_and_add(self, data):
        data = data.get(self, data)
        request = copy_request(self.request)
        apply_skin(request, IUserSkinnable(request.root).get_skin())
        return IRedirectionManager(self.context).test_rules(source_url=data['source_url'],
                                                            request=request,
                                                            check_inactive_rules=data['check_inactive_rules'])


@viewlet_config(name='test-results',
                context=IRedirectionManagerTarget, layer=IAdminLayer, view=RedirectionManagerTestForm,
                manager=IContentSuffixViewletManager, weight=10)
class RedirectionManagerTestFormResults(EmptyViewlet):
    """Redirection manager test form results container"""

    def render(self):
        return f'<div id="{self.view.ajax_form_target[1:]}"></div>'


@adapter_config(name='test',
                required=(IRedirectionManagerTarget, IAdminLayer, RedirectionManagerTestForm),
                provides=IAJAXFormRenderer)
class RedirectionManagerTestFormRenderer(ContextRequestViewAdapter):
    """Redirection manager test form renderer"""

    def render(self, changes):
        return {
            'status': 'success',
            'content': {
                'html': render('templates/test-results.pt',
                               {'changes': changes},
                               request=self.request)
            },
            'closeForm': False
        }
