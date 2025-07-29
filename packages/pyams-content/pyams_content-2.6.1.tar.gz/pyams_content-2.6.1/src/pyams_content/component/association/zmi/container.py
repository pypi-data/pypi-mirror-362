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

"""PyAMS_content.component.association.zmi.container module

This module provides a few components used for management of associations containers.
"""

from pyramid.decorator import reify
from pyramid.view import view_config
from zope.interface import implementer

from pyams_content.component.association import IAssociationContainer, IAssociationContainerTarget
from pyams_content.component.association.interfaces import IAssociationInfo, IAssociationParagraph
from pyams_content.component.association.zmi import IAssociationsTable
from pyams_content.component.association.zmi.interfaces import IAssociationsContainerEditForm
from pyams_content.component.paragraph.zmi.helper import get_json_paragraph_toolbar_refresh_event
from pyams_content.shared.common.interfaces.types import ITypedSharedTool
from pyams_content.shared.common.zmi.types import ISharedToolTypesTable
from pyams_form.ajax import ajax_form_config
from pyams_form.interfaces.form import IInnerSubForm
from pyams_layer.interfaces import IPyAMSLayer
from pyams_layer.skin import apply_skin
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.permission import get_edit_permission
from pyams_skin.interfaces.view import IModalDisplayForm
from pyams_skin.interfaces.viewlet import IContentPrefixViewletManager
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import MISSING_INFO
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalDisplayForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_zmi.skin import AdminSkin
from pyams_zmi.table import ActionColumn, ContentTypeColumn, I18nColumnMixin, InnerTableAdminView, \
    NameColumn, ReorderColumn, SortableTable, TableGroupSwitcher, TrashColumn, VisibilityColumn
from pyams_zmi.utils import get_object_hint, get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(name='associations',
                required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesAssociationsColumn(ActionColumn):
    """Shared tool data types table associations column"""

    hint = _("Default links and external files")
    icon_class = 'fas fa-link'

    href = 'associations-modal.html'
    modal_target = True

    weight = 450


#
# Associations table modal viewer
#

@ajax_form_config(name='associations-modal.html',
                  context=IAssociationContainerTarget, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
@implementer(IAssociationsContainerEditForm)
class AssociationsModalEditForm(AdminModalDisplayForm):
    """Associations modal edit form"""

    modal_class = 'modal-xl'

    subtitle = _("Links and external files")


@adapter_config(required=(IAssociationContainerTarget, IAdminLayer, IModalDisplayForm),
                provides=IFormTitle)
def association_container_display_form_title(context, request, form):
    """Association container display form title"""
    hint = get_object_hint(context, request, form)
    label = get_object_label(context, request, form)
    return TITLE_SPAN_BREAK.format(hint, label)


@factory_config(IAssociationsTable)
class AssociationsTable(SortableTable):
    """Associations table"""

    container_class = IAssociationContainer

    display_if_empty = True

    @property
    def css_classes(self):
        container = self.container_class(self.context)
        permission = get_edit_permission(self.request, container, self)
        table_class = super().css_classes.get('table')
        if self.request.has_permission(permission, context=container):
            table_class += ' my-0'
        return {
            'table': table_class
        }


@adapter_config(required=(IAssociationContainer, IAdminLayer, IAssociationsTable),
                provides=IValues)
class AssociationsTableValues(ContextRequestViewAdapter):
    """Associations table values"""

    @property
    def values(self):
        """Associations container values getter"""
        yield from IAssociationContainer(self.context).values()


@adapter_config(name='reorder',
                required=(IAssociationContainer, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsReorderColumn(ReorderColumn):
    """Associations reorder column"""


@view_config(name='reorder.json',
             context=IAssociationContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def reorder_associations_table(request):
    """Reorder associations"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='visible',
                required=(IAssociationContainer, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsVisibleColumn(VisibilityColumn):
    """Associations table visible column"""


@view_config(name='switch-visible-item.json',
             context=IAssociationContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_item(request):
    """Switch visible item"""
    return switch_element_attribute(request)


@adapter_config(name='icon',
                required=(IAssociationContainer, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsIconColumn(ContentTypeColumn):
    """Associations table icon column"""


@adapter_config(name='label',
                required=(IAssociationContainer, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsLabelColumn(NameColumn):
    """Associations table label column"""

    i18n_header = _("Public label")


@adapter_config(name='target',
                required=(IAssociationContainer, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsTargetColumn(I18nColumnMixin, GetAttrColumn):
    """Associations table target column"""

    i18n_header = _("Internal target")
    weight = 50

    def get_value(self, obj):
        """Column value getter"""
        info = IAssociationInfo(obj, None)
        if info is None:
            return MISSING_INFO
        return info.inner_title


@adapter_config(name='size',
                required=(IAssociationContainer, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsSizeColumn(I18nColumnMixin, GetAttrColumn):
    """Associations table size column"""

    i18n_header = _("Size")
    weight = 60

    def get_value(self, obj):
        """Column value getter"""
        info = IAssociationInfo(obj, None)
        if info is None:
            return MISSING_INFO
        return info.human_size


@adapter_config(name='trash',
                required=(IAssociationContainer, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class AssociationsTrashColumn(TrashColumn):
    """Associations table trash column"""


@view_config(name='delete-element.json',
             context=IAssociationContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def delete_data_type(request):
    """Delete data type"""
    result = delete_container_element(request)
    apply_skin(request, AdminSkin)
    event = get_json_paragraph_toolbar_refresh_event(request.context, request)
    if event is not None:
        result.setdefault('callbacks', []).append(event)
        result.setdefault('handle_json', True)
    return result


#
# Main associations table
#

@viewlet_config(name='associations-table',
                context=IAssociationContainerTarget, layer=IAdminLayer,
                view=IAssociationsContainerEditForm,
                manager=IContentPrefixViewletManager, weight=10)
class AssociationsTableView(InnerTableAdminView):
    """Associations table view"""

    table_class = IAssociationsTable
    table_label = _("Links and external files list")

    container_intf = IAssociationContainer


#
# Associations table group
#

@adapter_config(name='associations-group',
                required=(IAssociationContainerTarget, IAdminLayer, IPropertiesEditForm),
                provides=IInnerSubForm, force_implements=False)
@template_config(template='templates/associations-table.pt', layer=IAdminLayer)
class AssociationsGroup(TableGroupSwitcher):
    """Associations table group"""

    legend = _("Links and external files")

    table_class = IAssociationsTable
    container_intf = IAssociationContainer

    weight = 20

    @property
    def state(self):
        """Always open switcher in associations paragraphs"""
        if IAssociationParagraph.providedBy(self.context):
            return 'open'
        return super().state

    @reify
    def container(self):
        """Associations container getter"""
        return self.container_intf(self.context)

    @property
    def edit_permission(self):
        """Edit permission getter"""
        return get_edit_permission(self.request, self.container, self)
