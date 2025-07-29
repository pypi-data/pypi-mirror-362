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

"""PyAMS_content.feature.script.zmi module

This module provides management components for scripts and scripts containers.
"""

from pyramid.view import view_config
from zope.interface import Interface, alsoProvides

from pyams_content.feature.script import IScriptContainer, IScriptContainerTarget, IScriptInfo
from pyams_content.feature.script.zmi.interfaces import IScriptContainerNavigationMenu, IScriptContainerTable
from pyams_content.interfaces import MANAGE_SITE_ROOT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.view import IModalEditForm
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.traversing import get_parent
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm, SimpleAddFormRenderer, SimpleEditFormRenderer
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectLabel, TITLE_SPAN, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import ISiteManagementMenu, IToolbarViewletManager
from pyams_zmi.table import AttributeSwitcherColumn, NameColumn, ReorderColumn, SortableTable, TableAdminView, \
    TableElementEditor, TrashColumn
from pyams_zmi.utils import get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewletmanager_config(name='scripts.menu',
                       context=IScriptContainerTarget, layer=IAdminLayer,
                       manager=ISiteManagementMenu, weight=30,
                       provides=IScriptContainerNavigationMenu,
                       permission=MANAGE_SITE_ROOT_PERMISSION)
class ScriptsContainerMenu(NavigationMenuItem):
    """Scripts container navigation menu"""

    label = _("External scripts")
    icon_class = 'fas fa-code'
    href = '#scripts.html'


@factory_config(IScriptContainerTable)
class ScriptContainerTable(SortableTable):
    """Script container table"""

    container_class = IScriptContainer

    display_if_empty = True


@adapter_config(required=(IScriptContainerTarget, IAdminLayer, IScriptContainerTable),
                provides=IValues)
class ScriptContainerTableValues(ContextRequestViewAdapter):
    """Script container table values adapter"""

    @property
    def values(self):
        """Script container table values getter"""
        yield from IScriptContainer(self.context).values()


@adapter_config(name='reorder',
                required=(IScriptContainerTarget, IAdminLayer, IScriptContainerTable),
                provides=IColumn)
class ScriptContainerTableReorderColumn(ReorderColumn):
    """Scripts container table reorder column"""


@view_config(name='reorder.json',
             context=IScriptContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_SITE_ROOT_PERMISSION)
def reorder_script_container_table(request):
    """Reorder script container table"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='active',
                required=(IScriptContainerTarget, IAdminLayer, IScriptContainerTable),
                provides=IColumn)
class ScriptContainerActiveColumn(AttributeSwitcherColumn):
    """Scripts container table active column"""

    attribute_name = 'active'
    attribute_switcher = 'switch-active-script.json'

    icon_off_class = 'far fa-eye-slash text-danger'

    permission = MANAGE_SITE_ROOT_PERMISSION
    weight = 1

    def get_icon_hint(self, item):
        """Icon hint getter"""
        if self.has_permission(item):
            hint = _("Click icon to switch script activity")
        elif item.active:
            hint = _("This script is active")
        else:
            hint = _("This script is not active")
        return self.request.localizer.translate(hint)


@view_config(name='switch-active-script.json',
             context=IScriptContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_active_script(request):
    """Switch script activity flag"""
    return switch_element_attribute(request, container_factory=IScriptContainer)


@adapter_config(name='label',
                required=(IScriptContainerTarget, IAdminLayer, IScriptContainerTable),
                provides=IColumn)
class ScriptContainerLabelColumn(NameColumn):
    """Scripts container table label column"""

    attr_name = 'name'
    i18n_header = _("Script name")


@adapter_config(name='trash',
                required=(IScriptContainerTarget, IAdminLayer, IScriptContainerTable),
                provides=IColumn)
class ScriptContainerTrashColumn(TrashColumn):
    """Scripts container table trash column"""

    object_data = {
        'ams-modules': 'container',
        'ams-delete-target': 'delete-script.json'
    }


@view_config(name='delete-script.json',
             context=IScriptContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_SITE_ROOT_PERMISSION)
def delete_script(request):
    """Delete script"""
    return delete_container_element(request, container_factory=IScriptContainer)


@pagelet_config(name='scripts.html',
                context=IScriptContainerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class ScriptsView(TableAdminView):
    """Scripts view"""

    title = _("External scripts")

    table_class = IScriptContainerTable
    table_label = _("External scripts list")


#
# Scripts components
#

class ScriptEditorMixin:
    """Script editor mixin class"""

    modal_class = 'modal-max'

    label_css_class = 'col-sm-2 col-md-3'
    input_css_class = 'col-sm-10 col-md-9'

    def update_widgets(self, prefix=None):
        """Widgets update"""
        super().update_widgets(prefix)
        body = self.widgets.get('body')
        if body is not None:
            body.add_class('height-100')
            body.widget_css_class = 'editor height-500px'
            body.object_data = {
                'ams-filename': 'script.html'
            }
            alsoProvides(body, IObjectData)


@viewlet_config(name='add-script.action',
                context=IScriptContainerTarget, layer=IAdminLayer, view=IScriptContainerTable,
                manager=IToolbarViewletManager, weight=20,
                permission=MANAGE_SITE_ROOT_PERMISSION)
class ScriptAddAction(ContextAddAction):
    """Script add action"""

    label = _("Add script")
    href = 'add-script.html'


@ajax_form_config(name='add-script.html',
                  context=IScriptContainerTarget, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_ROOT_PERMISSION)
class ScriptAddForm(ScriptEditorMixin, AdminModalAddForm):
    """Script add form"""

    subtitle = _("New script")
    legend = _("New script properties")

    content_factory = IScriptInfo
    fields = Fields(IScriptInfo).omit('__parent__', '__name__', 'active')

    def add(self, obj):
        IScriptContainer(self.context).append(obj)


@adapter_config(required=(IScriptContainerTarget, IAdminLayer, ScriptAddForm),
                provides=IFormTitle)
def script_add_form_title(context, request, form):
    """Script add form title"""
    return TITLE_SPAN.format(
        get_object_label(context, request, form))


@adapter_config(required=(IScriptContainerTarget, IAdminLayer, ScriptAddForm),
                provides=IAJAXFormRenderer)
class ScriptAddFormRenderer(SimpleAddFormRenderer):
    """Script add form renderer"""

    table_factory = IScriptContainerTable


@adapter_config(required=(IScriptInfo, IAdminLayer, Interface),
                provides=IObjectLabel)
def script_label(context, request, view):
    """Script label"""
    return context.name


@adapter_config(required=(IScriptInfo, IAdminLayer, Interface),
                provides=IObjectHint)
def script_hint(context, request, view):
    """Script hint"""
    return request.localizer.translate(_("Custom script"))


@adapter_config(required=(IScriptInfo, IAdminLayer, IScriptContainerTable),
                provides=ITableElementEditor)
class ScriptEditor(TableElementEditor):
    """Script editor"""


@ajax_form_config(name='properties.html',
                  context=IScriptInfo, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ScriptPropertiesEditForm(ScriptEditorMixin, AdminModalEditForm):
    """Script properties edit form"""

    legend = _("Script properties")

    fields = Fields(IScriptInfo).omit('__parent__', '__name__', 'active')


@adapter_config(required=(IScriptInfo, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def script_edit_form_title(context, request, form):
    """Script edit form title"""
    translate = request.localizer.translate
    target = get_parent(context, IScriptContainerTarget)
    return TITLE_SPAN_BREAK.format(
        get_object_label(target, request, form),
        translate(_("Custom script: {}")).format(get_object_label(context, request, form)))


@adapter_config(required=(IScriptInfo, IAdminLayer, ScriptPropertiesEditForm),
                provides=IAJAXFormRenderer)
class ScriptPropertiesEditFormRenderer(SimpleEditFormRenderer):
    """Script properties edit form renderer"""

    parent_interface = IScriptContainerTarget
    table_factory = IScriptContainerTable
