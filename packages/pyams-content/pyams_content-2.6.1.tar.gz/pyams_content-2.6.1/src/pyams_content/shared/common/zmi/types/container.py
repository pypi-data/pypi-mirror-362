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

"""PyAMS_content.shared.common.zmi.types.container module

This module defines components which are used for shared contents types management interface.
"""

from pyramid.view import view_config

from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.shared.common.interfaces.types import ITypedDataManager, ITypedSharedTool
from pyams_content.shared.common.zmi.types.interfaces import ISharedToolTypesTable
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.table import NameColumn, ReorderColumn, SortableTable, TableAdminView, TrashColumn, \
    VisibilityColumn
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='data-types.menu',
                context=ITypedSharedTool, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=405,
                permission=MANAGE_TOOL_PERMISSION)
class SharedToolTypesMenu(NavigationMenuItem):
    """Shared tool data types menu"""

    label = _("Content types")
    href = '#data-types.html'


@factory_config(ISharedToolTypesTable)
class SharedToolTypesTable(SortableTable):
    """Shared tool data types table"""

    container_class = ITypedDataManager

    display_if_empty = True


@adapter_config(required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IValues)
class SharedToolTypesTableValues(ContextRequestViewAdapter):
    """Shared tool data types table values"""

    @property
    def values(self):
        """Data types values getter"""
        yield from ITypedDataManager(self.context).values()


@adapter_config(name='reorder',
                required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesReorderColumn(ReorderColumn):
    """Shared tool data types table reorder column"""


@view_config(name='reorder.json',
             context=ITypedDataManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TOOL_PERMISSION)
def reorder_types_table(request):
    """Reorder shared tool data types"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success'
    }


@adapter_config(name='visible',
                required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesVisibleColumn(VisibilityColumn):
    """Shared tool data types table visible column"""

    hint = _("Click icon to enable or disable content type")


@view_config(name='switch-visible-item.json',
             context=ITypedDataManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_item(request):
    """Switch visible item"""
    return switch_element_attribute(request)


@adapter_config(name='label',
                required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesLabelColumn(NameColumn):
    """Shared tool data types table label column"""

    i18n_header = _("Label")


@adapter_config(name='trash',
                required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesTrashColumn(TrashColumn):
    """Shared tool data types table trash column"""


@view_config(name='delete-element.json',
             context=ITypedDataManager, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TOOL_PERMISSION)
def delete_data_type(request):
    """Delete data type"""
    return delete_container_element(request)


@pagelet_config(name='data-types.html',
                context=ITypedSharedTool, layer=IPyAMSLayer,
                permission=MANAGE_TOOL_PERMISSION)
class SharedToolTypesView(TableAdminView):
    """Shared tool data types view"""

    title = _("Content types")

    table_class = ISharedToolTypesTable
    table_label = _("Shared tool content types list")
