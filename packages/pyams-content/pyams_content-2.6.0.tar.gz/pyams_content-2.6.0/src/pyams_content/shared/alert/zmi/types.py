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

"""PyAMS_content.shared.alert.zmi.types module

"""

from pyramid.view import view_config
from zope.interface import Interface

from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.shared.alert import IAlertManager, IAlertTypesManager
from pyams_content.shared.alert.interfaces import IAlertType
from pyams_content.shared.alert.zmi.interfaces import IAlertTypesTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_skin.interfaces.view import IModalEditForm
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces.intids import IUniqueID
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.helper.event import get_json_table_row_add_callback, get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectLabel, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IPropertiesMenu, IToolbarViewletManager
from pyams_zmi.table import NameColumn, ReorderColumn, SortableTable, TableAdminView, TableElementEditor, TrashColumn, \
    VisibilityColumn
from pyams_zmi.utils import get_object_hint, get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='alert-types.menu',
                context=IAlertManager, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=400,
                permission=MANAGE_TOOL_PERMISSION)
class AlertTypesMenu(NavigationMenuItem):
    """Alert types menu"""

    label = _("Alert types")
    href = '#alert-types.html'


@factory_config(IAlertTypesTable)
class AlertTypesTable(SortableTable):
    """Alert types table"""

    container_class = IAlertTypesManager

    display_if_empty = True


@adapter_config(required=(IAlertManager, IAdminLayer, IAlertTypesTable),
                provides=IValues)
class AlertTypesTableValues(ContextRequestViewAdapter):
    """Alert types table values"""

    @property
    def values(self):
        """Alert types values getter"""
        yield from IAlertTypesManager(self.context).values()


@adapter_config(name='reorder',
                required=(IAlertManager, IAdminLayer, IAlertTypesTable),
                provides=IColumn)
class AlertTypesReorderColumn(ReorderColumn):
    """Alert types table reorder column"""


@view_config(name='reorder.json',
             context=IAlertTypesManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TOOL_PERMISSION)
def reorder_types_table(request):
    """Reorder alert types"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success'
    }


@adapter_config(name='visible',
                required=(IAlertManager, IAdminLayer, IAlertTypesTable),
                provides=IColumn)
class AlertTypesVisibleColumn(VisibilityColumn):
    """Alert types table visible column"""

    hint = _("Click icon to enable or disable alert type")


@view_config(name='switch-visible-item.json',
             context=IAlertTypesManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_item(request):
    """Switch visible item"""
    return switch_element_attribute(request)


@adapter_config(name='label',
                required=(IAlertManager, IAdminLayer, IAlertTypesTable),
                provides=IColumn)
class AlertTypesLabelColumn(NameColumn):
    """Alert types table label column"""

    i18n_header = _("Label")


@adapter_config(name='trash',
                required=(IAlertManager, IAdminLayer, IAlertTypesTable),
                provides=IColumn)
class AlertTypesTrashColumn(TrashColumn):
    """Alert types table trash column"""


@view_config(name='delete-element.json',
             context=IAlertTypesManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TOOL_PERMISSION)
def delete_data_type(request):
    """Delete data type"""
    return delete_container_element(request)


@pagelet_config(name='alert-types.html',
                context=IAlertManager, layer=IPyAMSLayer,
                permission=MANAGE_TOOL_PERMISSION)
class AlertTypesView(TableAdminView):
    """Alert types view"""

    title = _("Alert types")

    table_class = IAlertTypesTable
    table_label = _("Alert types list")
    
    
#
# Alert types views
#

@viewlet_config(name='add-alert-type.action',
                context=IAlertManager, layer=IAdminLayer, view=IAlertTypesTable,
                manager=IToolbarViewletManager, weight=20,
                permission=MANAGE_TOOL_PERMISSION)
class AlertTypesAddAction(ContextAddAction):
    """Alert type add action"""

    label = _("Add alert type")
    href = 'add-alert-type.html'


@ajax_form_config(name='add-alert-type.html',
                  context=IAlertManager, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class AlertTypeAddForm(AdminModalAddForm):
    """Alert type add form"""

    subtitle = _("New alert type")
    legend = _("New alert type properties")

    fields = Fields(IAlertType).omit('__name__', '__parent__', 'visible')
    content_factory = IAlertType

    def add(self, obj):
        oid = IUniqueID(obj).oid
        IAlertTypesManager(self.context)[oid] = obj


@adapter_config(required=(IAlertManager, IAdminLayer, AlertTypeAddForm),
                provides=IAJAXFormRenderer)
class AlertTypeAddFormRenderer(ContextRequestViewAdapter):
    """Alert type add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                IAlertTypesTable, changes)
            ]
        }


@adapter_config(required=(IAlertType, IAdminLayer, Interface),
                provides=IObjectLabel)
def alert_type_label(context, request, view):
    """Alert type label"""
    i18n = II18n(context)
    return i18n.query_attribute('label', request=request)


@adapter_config(required=(IAlertType, IAdminLayer, Interface),
                provides=IObjectHint)
def alert_type_hint(context, request, view):  # pylint: disable=unused-argument
    """Alert type hint"""
    return request.localizer.translate(_("Alert type"))


@adapter_config(required=(IAlertType, IAdminLayer, IAlertTypesTable),
                provides=ITableElementEditor)
class AlertTypeEditor(TableElementEditor):
    """Alert type editor"""


@ajax_form_config(name='properties.html',
                  context=IAlertType, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class AlertTypeEditForm(AdminModalEditForm):
    """Alert type properties edit form"""

    legend = _("Alert type properties")

    fields = Fields(IAlertType).omit('__name__', '__parent__', 'visible')


@adapter_config(required=(IAlertType, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def alert_type_edit_form_title(context, request, form):
    """Alert type edit form title getter"""
    return TITLE_SPAN_BREAK.format(
        get_object_hint(context, request, form),
        get_object_label(context, request, form))


@adapter_config(required=(IAlertType, IAdminLayer, AlertTypeEditForm),
                provides=IAJAXFormRenderer)
class AlertTypeEditFormRenderer(ContextRequestViewAdapter):
    """Alert type edit form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        tool = get_parent(self.context, IAlertManager)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(tool, self.request,
                                                    IAlertTypesTable, self.context)
            ]
        }
