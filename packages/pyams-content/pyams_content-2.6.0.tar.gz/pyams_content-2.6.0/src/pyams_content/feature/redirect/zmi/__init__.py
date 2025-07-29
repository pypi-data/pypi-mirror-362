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

"""PyAMS_content.feature.redirect.zmi module

This module defines management interface components to handle redirection rules.
"""

from zope.interface import Interface, implementer

from pyams_content.feature.redirect import IRedirectionRule
from pyams_content.feature.redirect.interfaces import IRedirectionManager, IRedirectionManagerTarget
from pyams_content.feature.redirect.zmi.interfaces import IRedirectionsTable
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.view import IModalEditForm
from pyams_skin.interfaces.viewlet import IHelpViewletManager
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import adapter_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm, SimpleAddFormRenderer, SimpleEditFormRenderer
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectLabel, TITLE_SPAN, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='add-redirection-rule.action',
                context=IRedirectionManagerTarget, layer=IAdminLayer, view=IRedirectionsTable,
                manager=IToolbarViewletManager, weight=10,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class RedirectionRuleAddAction(ContextAddAction):
    """Redirection rule add action"""

    label = _("Add redirection rule")
    href = 'add-redirection-rule.html'


class IRedirectionRuleForm(Interface):
    """Redirection rule form marker interface"""


@ajax_form_config(name='add-redirection-rule.html',
                  context=IRedirectionManagerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
@implementer(IRedirectionRuleForm)
class RedirectionRuleAddForm(AdminModalAddForm):
    """Redirection rule add form"""

    subtitle = _("New redirection rule")
    legend = _("New redirection rule properties")
    modal_class = 'modal-xl'

    fields = Fields(IRedirectionRule).omit('active', 'chained')
    content_factory = IRedirectionRule

    def add(self, obj):
        IRedirectionManager(self.context).append(obj)


@adapter_config(required=(IRedirectionManagerTarget, IAdminLayer, RedirectionRuleAddForm),
                provides=IFormTitle)
def redirection_rule_add_form_title(context, request, form):
    """Redirection rule add form title"""
    return TITLE_SPAN.format(
        get_object_label(context, request, form))


@adapter_config(required=(IRedirectionManagerTarget, IAdminLayer, RedirectionRuleAddForm),
                provides=IAJAXFormRenderer)
class RedirectionRuleAddFormRenderer(SimpleAddFormRenderer):
    """Redirection rule add form renderer"""

    table_factory = IRedirectionsTable


@adapter_config(required=(IRedirectionRule, IAdminLayer, Interface),
                provides=IObjectLabel)
def redirection_rule_label(context, request, view):
    """Redirection rule label"""
    return context.label


@adapter_config(required=(IRedirectionRule, IAdminLayer, Interface),
                provides=IObjectHint)
def redirection_rule_hint(context, request, view):
    """Redirection rule hint"""
    return request.localizer.translate(_("Redirection rule"))


@adapter_config(required=(IRedirectionRule, IAdminLayer, Interface),
                provides=ITableElementEditor)
class RedirectionRuleElementEditor(TableElementEditor):
    """Redirection rule element editor"""


@ajax_form_config(name='properties.html',
                  context=IRedirectionRule, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class RedirectionRulePropertiesEditForm(AdminModalEditForm):
    """Redirection rule properties edit form"""

    legend = _("Redirection rule properties")

    fields = Fields(IRedirectionRule).omit('__parent__', '__name__', 'active', 'chained')


@adapter_config(required=(IRedirectionRule, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def redirection_rule_edit_form_title(context, request, form):
    """Redirection rule edit form title"""
    translate = request.localizer.translate
    target = get_parent(context, IRedirectionManagerTarget)
    return TITLE_SPAN_BREAK.format(
        get_object_label(target, request, form),
        translate(_("Redirection rule: {}")).format(get_object_label(context, request, form)))


@adapter_config(required=(IRedirectionRule, IAdminLayer, RedirectionRulePropertiesEditForm),
                provides=IAJAXFormRenderer)
class RedirectionRulePropertiesEditFormRenderer(SimpleEditFormRenderer):
    """Redirection rule properties edit form renderer"""

    parent_interface = IRedirectionManagerTarget
    table_factory = IRedirectionsTable


@viewlet_config(name='redirection.help',
                context=IRedirectionManagerTarget, layer=IAdminLayer, view=RedirectionRuleAddForm,
                manager=IHelpViewletManager, weight=10)
@viewlet_config(name='redirection.help',
                context=IRedirectionRule, layer=IAdminLayer, view=RedirectionRulePropertiesEditForm,
                manager=IHelpViewletManager, weight=10)
class RedirectionRuleFormHelp(AlertMessage):
    """Redirection rule form help"""

    status = 'info'

    _message = _("""URL pattern and target URL are defined by *regular expressions* (see 
[Python Regular Expressions](https://docs.python.org/3/library/re.html)).<br />
In an URL pattern, you can use any valid regular expression element, notably:\n
 - « .* » to match any list of characters
 - « ( ) » to "memorize" parts of the URL which can be replaced into target URL
 - « \\ » to protect special characters (like "+").
 
In target URL, memorized parts can be reused using « \\1 », « \\2 » and so on, where given number is
the order of the matching pattern element.
""")
    message_renderer = 'markdown'
