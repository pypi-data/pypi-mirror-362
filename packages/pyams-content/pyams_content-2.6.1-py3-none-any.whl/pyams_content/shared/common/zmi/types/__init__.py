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

"""PyAMS_content.shared.common.zmi.types module

This module provides shared content data types management components.
"""

from zope.interface import Interface

from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.reference.pictogram.zmi.widget import PictogramSelectFieldWidget
from pyams_content.shared.common.interfaces.types import IDataType, ITypedDataManager, ITypedSharedTool
from pyams_content.shared.common.zmi.types.interfaces import ISharedToolTypesTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.group import Group
from pyams_form.interfaces.form import IAJAXFormRenderer, IGroup
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.view import IModalEditForm
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.intids import IUniqueID
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm, FormGroupSwitcher
from pyams_zmi.helper.event import get_json_table_row_add_callback, get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectLabel, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_hint, get_object_label


__docformat__ = 'restructuredtext'

from pyams_content import _


#
# Shared data types views
#

@viewlet_config(name='add-data-type.action',
                context=ITypedSharedTool, layer=IAdminLayer, view=ISharedToolTypesTable,
                manager=IToolbarViewletManager, weight=20,
                permission=MANAGE_TOOL_PERMISSION)
class DataTypesAddAction(ContextAddAction):
    """Data type add action"""

    label = _("Add content type")
    href = 'add-data-type.html'


@ajax_form_config(name='add-data-type.html',
                  context=ITypedSharedTool, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class DataTypeAddForm(AdminModalAddForm):
    """Data type add form"""

    subtitle = _("New content type")
    legend = _("New data type properties")

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(IDataType).select('label', 'source_folder',
                                          'color', 'pictogram', 'field_names')
        fields['pictogram'].widget_factory = PictogramSelectFieldWidget
        if not self.context.shared_content_info_factory:
            fields = fields.omit('field_names')
        return fields

    content_factory = IDataType

    def add(self, obj):
        oid = IUniqueID(obj).oid
        ITypedDataManager(self.context)[oid] = obj


@adapter_config(required=(ITypedSharedTool, IAdminLayer, DataTypeAddForm),
                provides=IAJAXFormRenderer)
class DataTypeAddFormRenderer(ContextRequestViewAdapter):
    """Data type add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                ISharedToolTypesTable, changes)
            ]
        }


@adapter_config(required=(IDataType, IAdminLayer, Interface),
                provides=IObjectLabel)
def data_type_label(context, request, view):
    """Data type label"""
    i18n = II18n(context)
    return i18n.query_attribute('label', request=request)


@adapter_config(required=(IDataType, IAdminLayer, Interface),
                provides=IObjectHint)
def data_type_hint(context, request, view):  # pylint: disable=unused-argument
    """Data type hint"""
    return request.localizer.translate(_("Data type"))


@adapter_config(required=(IDataType, IAdminLayer, ISharedToolTypesTable),
                provides=ITableElementEditor)
class DataTypeEditor(TableElementEditor):
    """Data type editor"""


@ajax_form_config(name='properties.html',
                  context=IDataType, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class DataTypeEditForm(AdminModalEditForm):
    """Data type properties edit form"""

    legend = _("Content type properties")

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(IDataType).select('label', 'source_folder',
                                          'color', 'pictogram', 'field_names')
        fields['pictogram'].widget_factory = PictogramSelectFieldWidget
        tool = get_parent(self.context, ITypedSharedTool)
        if (tool is not None) and not tool.shared_content_info_factory:
            fields = fields.omit('field_names')
        return fields


@adapter_config(required=(IDataType, IAdminLayer, IModalEditForm),
                provides=IFormTitle)
def data_type_edit_form_title(context, request, form):
    """Data type edit form title getter"""
    return TITLE_SPAN_BREAK.format(
        get_object_hint(context, request, form),
        get_object_label(context, request, form))


@adapter_config(required=(IDataType, IAdminLayer, DataTypeEditForm),
                provides=IAJAXFormRenderer)
class DataTypeEditFormRenderer(ContextRequestViewAdapter):
    """Data type edit form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        tool = get_parent(self.context, ITypedSharedTool)
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(tool, self.request,
                                                    ISharedToolTypesTable, self.context)
            ]
        }


@adapter_config(name='labels.group',
                required=(ITypedSharedTool, IAdminLayer, DataTypeAddForm),
                provides=IGroup)
@adapter_config(name='labels.group',
                required=(IDataType, IAdminLayer, DataTypeEditForm),
                provides=IGroup)
class DataTypeLabelsGroup(Group):
    """Data type labels group"""

    legend = _("Contents labels")
    weight = 10

    fields = Fields(IDataType).select('navigation_label', 'display_as_tag', 'facets_label',
                                      'facets_type_label', 'dashboard_label')


@adapter_config(name='pictograms.group',
                required=(ITypedSharedTool, IAdminLayer, DataTypeAddForm),
                provides=IGroup)
@adapter_config(name='pictograms.group',
                required=(IDataType, IAdminLayer, DataTypeEditForm),
                provides=IGroup)
class DataTypePictogramsGroup(FormGroupSwitcher):
    """Data type pictograms group"""

    legend = _("Pictograms")
    weight = 20

    fields = Fields(IDataType).select('pictogram_on', 'pictogram_off')
    fields['pictogram_on'].widget_factory = PictogramSelectFieldWidget
    fields['pictogram_off'].widget_factory = PictogramSelectFieldWidget
