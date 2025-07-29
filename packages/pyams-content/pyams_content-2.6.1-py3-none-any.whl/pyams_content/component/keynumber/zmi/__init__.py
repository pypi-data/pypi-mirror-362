# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyramid.view import view_config
from zope.interface import Interface, implementer

from pyams_content.component.keynumber import IKeyNumberInfo, IKeyNumbersContainer, IKeyNumbersParagraph, \
    KEYNUMBERS_PARAGRAPH_ICON_CLASS, KEYNUMBERS_PARAGRAPH_NAME, KEYNUMBERS_PARAGRAPH_TYPE
from pyams_content.component.paragraph import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu, \
    IParagraphContainerBaseTable
from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.interfaces.view import IModalPage
from pyams_skin.interfaces.viewlet import IContentSuffixViewletManager
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config, query_adapter
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.helper.event import get_json_table_row_add_callback, get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IToolbarViewletManager
from pyams_zmi.table import I18nColumnMixin, InnerTableAdminView, NameColumn, ReorderColumn, SortableTable, \
    TableElementEditor, TrashColumn, VisibilityColumn
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


class KeyNumbersTable(SortableTable):
    """Key numbers table"""
    
    container_class = IKeyNumbersContainer
    
    display_if_empty = True
    
    
@adapter_config(required=(IKeyNumbersContainer, IAdminLayer, KeyNumbersTable),
                provides=IValues)
class KeyNumbersTableValues(ContextRequestViewAdapter):
    """Key numbers table values adapter"""
    
    @property
    def values(self):
        """Key numbers table values getter"""
        yield from self.context.values()
        
        
@adapter_config(name='reorder',
                required=(IKeyNumbersContainer, IAdminLayer, KeyNumbersTable),
                provides=IColumn)
class KeyNumbersTableReorderColumn(ReorderColumn):
    """Key numbers table reorder column"""
    
    
@view_config(name='reorder.json',
             context=IKeyNumbersContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TEMPLATE_PERMISSION)
@view_config(name='reorder.json',
             context=IKeyNumbersParagraph, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_CONTENT_PERMISSION)
def reorder_keynumbers_table(request):
    """Reorder key numbers table"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='visible',
                required=(IKeyNumbersContainer, IAdminLayer, KeyNumbersTable),
                provides=IColumn)
class KeyNumbersTableVisibleColumn(VisibilityColumn):
    """Key numbers table visible column"""

    hint = _("Click icon to show or hide key-number")


@view_config(name='switch-visible-item.json',
             context=IKeyNumbersContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_card(request):
    """Switch visible key number"""
    return switch_element_attribute(request)


@adapter_config(name='label',
                required=(IKeyNumbersContainer, IAdminLayer, KeyNumbersTable),
                provides=IColumn)
class KeyNumbersTableLabelColumn(NameColumn):
    """Key numbers table label column"""

    i18n_header = _("Label")


@adapter_config(name='number',
                required=(IKeyNumbersContainer, IAdminLayer, KeyNumbersTable),
                provides=IColumn)
class KeyNumbersTableNumberColumn(I18nColumnMixin, GetAttrColumn):
    """Key numbers table name column"""

    i18n_header = _("Number")
    attr_name = 'number'

    weight = 20
    

@adapter_config(name='unit',
                required=(IKeyNumbersContainer, IAdminLayer, KeyNumbersTable),
                provides=IColumn)
class KeyNumbersTableUnitColumn(I18nColumnMixin, GetAttrColumn):
    """Key numbers table unit column"""

    i18n_header = _("Unit")
    attr_name = 'unit'
    
    weight = 30
    
    def get_value(self, obj):
        return II18n(obj).query_attribute(self.attr_name, request=self.request)


@adapter_config(name='trash',
                required=(IKeyNumbersContainer, IAdminLayer, KeyNumbersTable),
                provides=IColumn)
class KeyNumbersTableTrashColumn(TrashColumn):
    """Key numbers table trash column"""


@view_config(name='delete-element.json',
             context=IKeyNumbersContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TEMPLATE_PERMISSION)
def delete_key_number(request):
    """Delete key number"""
    return delete_container_element(request)


@viewlet_config(name='keynumbers-content-table',
                context=IKeyNumbersContainer, layer=IAdminLayer,
                view=IPropertiesEditForm,
                manager=IContentSuffixViewletManager, weight=10)
class KeyNumbersTableView(InnerTableAdminView):
    """Key numbers table view"""

    table_class = KeyNumbersTable
    table_label = _("List of portlet key numbers")


#
# Key numbers components
#

@viewlet_config(name='add-key-number.menu',
                context=IKeyNumbersContainer, layer=IAdminLayer, view=KeyNumbersTable,
                manager=IToolbarViewletManager, weight=10)
class KeyNumberAddAction(ProtectedViewObjectMixin, ContextAddAction):
    """Key number add action"""

    label = _("Add key-number")
    href = 'add-key-number.html'


class IKeyNumberForm(Interface):
    """Key number form marker interface"""


@ajax_form_config(name='add-key-number.html',
                  context=IKeyNumbersContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
@implementer(IKeyNumberForm)
class KeyNumberAddForm(AdminModalAddForm):
    """Key number add form"""

    subtitle = _("New key-number")
    legend = _("New key-number properties")
    modal_class = 'modal-xl'

    fields = Fields(IKeyNumberInfo).select('label', 'number', 'unit', 'text')
    content_factory = IKeyNumberInfo

    def add(self, obj):
        self.context.append(obj)


@adapter_config(required=(IKeyNumbersContainer, IAdminLayer, KeyNumberAddForm),
                provides=IAJAXFormRenderer)
class KeyNumberAddFormRenderer(ContextRequestViewAdapter):
    """Key number add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                KeyNumbersTable, changes)
            ]
        }


@adapter_config(required=(IKeyNumberInfo, IAdminLayer, Interface),
                provides=ITableElementEditor)
class KeyNumberElementEditor(TableElementEditor):
    """Key number element editor"""


@ajax_form_config(name='properties.html',
                  context=IKeyNumberInfo, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
@implementer(IKeyNumberForm)
class KeyNumberEditForm(AdminModalEditForm):
    """Key number properties edit form"""

    @property
    def subtitle(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        return translate(_("Key-number: {}")).format(get_object_label(self.context, self.request, self))

    legend = _("Key-number properties")
    modal_class = 'modal-xl'

    fields = Fields(IKeyNumberInfo).select('label', 'number', 'unit', 'text')


@adapter_config(required=(IKeyNumberInfo, IAdminLayer, IModalPage),
                provides=IFormTitle)
def key_number_edit_form_title(context, request, view):
    """Key number edit form title"""
    settings = get_parent(context, IKeyNumbersContainer)
    return query_adapter(IFormTitle, request, settings, view)


@adapter_config(required=(IKeyNumberInfo, IAdminLayer, KeyNumberEditForm),
                provides=IAJAXFormRenderer)
class KeyNumberEditFormRenderer(ContextRequestViewAdapter):
    """Key number edit form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(self.context.__parent__, self.request,
                                                    KeyNumbersTable, self.context)
            ]
        }


#
# Key numbers paragraph forms
#

@viewlet_config(name='add-key-numbers-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class KeyNumbersParagraphAddMenu(BaseParagraphAddMenu):
    """Key-number paragraph add menu"""

    label = KEYNUMBERS_PARAGRAPH_NAME
    icon_class = KEYNUMBERS_PARAGRAPH_ICON_CLASS

    factory_name = KEYNUMBERS_PARAGRAPH_TYPE
    href = 'add-key-numbers-paragraph.html'


@ajax_form_config(name='add-key-numbers-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class KeyNumbersParagraphAddForm(BaseParagraphAddForm):
    """Key-number paragraph add form"""

    content_factory = IKeyNumbersParagraph
