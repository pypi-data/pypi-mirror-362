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

"""PyAMS_content.reference.zmi.table module

This module defines generic components used to handle references tables properties.
"""
from pyramid.view import view_config
from zope.interface import Interface, implementer

from pyams_content.interfaces import MANAGE_REFERENCE_TABLE_PERMISSION
from pyams_content.reference import IReferenceTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm
from pyams_zmi.helper.container import delete_container_element
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_zmi.interfaces.viewlet import IMenuHeader, IPropertiesMenu, ISiteManagementMenu
from pyams_zmi.table import I18nColumnMixin, Table, TrashColumn
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='properties.menu',
                context=IReferenceTable, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=10,
                permission=VIEW_SYSTEM_PERMISSION)
class ReferenceTablePropertiesMenu(NavigationMenuItem):
    """Reference table properties menu"""

    label = _("Properties")

    href = '#properties.html'


@ajax_form_config(name='properties.html',
                  context=IReferenceTable, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
@implementer(IPropertiesEditForm)
class ReferenceTablePropertiesEditForm(AdminEditForm):
    """Reference table properties edit form"""

    legend = _("Edit table properties")

    fields = Fields(IReferenceTable).omit('__parent__', '__name__')
    edit_permission = MANAGE_REFERENCE_TABLE_PERMISSION


@adapter_config(required=(IReferenceTable, IAdminLayer, Interface, ISiteManagementMenu),
                provides=IMenuHeader)
def reference_table_site_management_menu_header(context, request, view, manager):
    """Reference table site management menu header adapter"""
    return _("Table management")


class ReferenceTableContainerTable(Table):
    """Reference table container table"""

    display_if_empty = True


@adapter_config(required=(IReferenceTable, IAdminLayer, ReferenceTableContainerTable),
                provides=IValues)
class ReferenceTableContainerTableValues(ContextRequestViewAdapter):
    """Reference table container table values adapter"""

    @property
    def values(self):
        """Reference table values getter"""
        yield from self.context.values()


@adapter_config(name='name',
                required=(IReferenceTable, IAdminLayer, ReferenceTableContainerTable),
                provides=IColumn)
class ReferenceTableNameColumn(I18nColumnMixin, GetAttrColumn):
    """Reference table name column"""

    i18n_header = _("Title")
    attr_name = 'title'

    weight = 10

    def get_value(self, obj):
        return II18n(obj).query_attribute(self.attr_name, request=self.request)


@adapter_config(name='trash',
                required=(IReferenceTable, IAdminLayer, ReferenceTableContainerTable),
                provides=IColumn)
class ReferenceTableTrashColumn(TrashColumn):
    """Reference table trash column"""

    permission = MANAGE_REFERENCE_TABLE_PERMISSION


@view_config(name='delete-element.json',
             context=IReferenceTable, request_type=IPyAMSLayer,
             permission=MANAGE_REFERENCE_TABLE_PERMISSION,
             renderer='json', xhr=True)
def delete_table_element(request):
    """Reference table delete view"""
    return delete_container_element(request)
