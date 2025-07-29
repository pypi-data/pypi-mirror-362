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

"""PyAMS_content.component.verbatim.zmi module

This module defines components for verbatim management.
"""

from pyramid.view import view_config
from zope.interface import Interface, implementer

from pyams_content.component.illustration import IIllustration
from pyams_content.component.paragraph.interfaces import IParagraphContainer, IParagraphContainerTarget
from pyams_content.component.paragraph.zmi import BaseParagraphAddForm, BaseParagraphAddMenu
from pyams_content.component.paragraph.zmi.interfaces import IParagraphContainerBaseTable
from pyams_content.component.verbatim.interfaces import IVerbatimContainer, IVerbatimInfo, IVerbatimParagraph, \
    VERBATIM_PARAGRAPH_ICON_CLASS, VERBATIM_PARAGRAPH_NAME, VERBATIM_PARAGRAPH_TYPE
from pyams_content.component.verbatim.zmi.interfaces import IVerbatimTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_skin.interfaces.view import IModalPage
from pyams_skin.interfaces.viewlet import IContentSuffixViewletManager
from pyams_skin.interfaces.widget import IHTMLEditorConfiguration
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.column import GetAttrColumn, I18nGetAttrColumn
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config, query_adapter
from pyams_utils.factory import factory_config
from pyams_utils.html import html_to_text
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.text import get_text_start
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.helper.event import get_json_table_row_add_callback, get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IToolbarViewletManager
from pyams_zmi.table import I18nColumnMixin, IconColumn, InnerTableAdminView, ReorderColumn, SortableTable, \
    TableElementEditor, \
    TrashColumn, VisibilityColumn
from pyams_zmi.utils import get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IVerbatimTable)
class VerbatimTable(SortableTable):
    """Verbatim table"""

    container_class = IVerbatimContainer

    display_if_empty = True


@adapter_config(required=(IVerbatimContainer, IAdminLayer, IVerbatimTable),
                provides=IValues)
class VerbatimTableValues(ContextRequestViewAdapter):
    """Verbatim table values adapter"""

    @property
    def values(self):
        """Verbatim table values getter"""
        yield from self.context.values()


@adapter_config(name='reorder',
                required=(IVerbatimContainer, IAdminLayer, IVerbatimTable),
                provides=IColumn)
class VerbatimTableReorderColumn(ReorderColumn):
    """Verbatim table reorder column"""


@view_config(name='reorder.json',
             context=IVerbatimContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TEMPLATE_PERMISSION)
def reorder_verbatim_container(request):
    """Reorder verbatim container"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='visible',
                required=(IVerbatimContainer, IAdminLayer, IVerbatimTable),
                provides=IColumn)
class VerbatimTableVisibleColumn(VisibilityColumn):
    """Verbatim table visible column"""

    hint = _("Click icon to show or hide verbatim")


@view_config(name='switch-visible-item.json',
             context=IVerbatimContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_verbatim(request):
    """Switch visible verbatim"""
    return switch_element_attribute(request)


@adapter_config(name='illustration',
                required=(IVerbatimContainer, IAdminLayer, IVerbatimTable),
                provides=IColumn)
class VerbatimTableIllustrationColumn(IconColumn):
    """Verbatim table illustration column"""

    icon_class = 'fas fa-image'
    hint = _("Illustration")

    weight = 9

    def checker(self, item):
        illustration = IIllustration(item, None)
        return illustration and illustration.data


@adapter_config(name='author',
                required=(IVerbatimContainer, IAdminLayer, IVerbatimTable),
                provides=IColumn)
class VerbatimTableAuthorColumn(I18nColumnMixin, GetAttrColumn):
    """Verbatim table author column"""

    i18n_header = _("Author")
    attr_name = 'author'
    default_value = MISSING_INFO
    
    weight = 10

    def get_value(self, obj):
        return super().get_value(obj) or self.default_value


@adapter_config(name='quote',
                required=(IVerbatimContainer, IAdminLayer, IVerbatimTable),
                provides=IColumn)
class VerbatimTableQuoteColumn(I18nColumnMixin, I18nGetAttrColumn):
    """Verbatim table quote column"""

    i18n_header = _("Quote")
    attr_name = 'quote'
    default_value = MISSING_INFO

    weight = 20
    
    def get_value(self, obj):
        return get_text_start(html_to_text(II18n(obj).query_attribute(self.attr_name, request=self.request)),
                              length=100) or self.default_value


@adapter_config(name='trash',
                required=(IVerbatimContainer, IAdminLayer, IVerbatimTable),
                provides=IColumn)
class VerbatimTableTrashColumn(TrashColumn):
    """Verbatim table trash column"""


@view_config(name='delete-element.json',
             context=IVerbatimContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=MANAGE_TEMPLATE_PERMISSION)
def delete_verbatim(request):
    """Delete verbatim"""
    return delete_container_element(request)


@viewlet_config(name='verbatim-content-table',
                context=IVerbatimContainer, layer=IAdminLayer,
                view=IPropertiesEditForm,
                manager=IContentSuffixViewletManager, weight=10)
class VerbatimTableView(InnerTableAdminView):
    """Verbatim table view"""

    table_class = IVerbatimTable
    table_label = _("List of verbatim")


#
# Verbatim forms
#

@viewlet_config(name='add-verbatim.action',
                context=IVerbatimContainer, layer=IAdminLayer, view=IVerbatimTable,
                manager=IToolbarViewletManager, weight=10,
                permission=MANAGE_TEMPLATE_PERMISSION)
class VerbatimAddAction(ContextAddAction):
    """Verbatim add action"""

    label = _("Add verbatim")
    href = 'add-verbatim.html'


class IVerbatimForm(Interface):
    """Verbatim form marker interface"""


@ajax_form_config(name='add-verbatim.html',
                  context=IVerbatimContainer, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
@implementer(IVerbatimForm)
class VerbatimAddForm(AdminModalAddForm):
    """Verbatim add form"""

    subtitle = _("New verbatim")
    legend = _("New verbatim properties")
    modal_class = 'modal-xl'

    fields = Fields(IVerbatimInfo).select('title', 'quote', 'author', 'charge')
    content_factory = IVerbatimInfo

    def add(self, obj):
        self.context.append(obj)


@adapter_config(required=(IVerbatimContainer, IAdminLayer, VerbatimAddForm),
                provides=IAJAXFormRenderer)
class VerbatimAddFormRenderer(ContextRequestViewAdapter):
    """Verbatim add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                IVerbatimTable, changes)
            ]
        }


@adapter_config(required=(IVerbatimInfo, IAdminLayer, Interface),
                provides=ITableElementEditor)
class VerbatimElementEditor(TableElementEditor):
    """Verbatim element editor"""


@ajax_form_config(name='properties.html',
                  context=IVerbatimInfo, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
@implementer(IVerbatimForm, IPropertiesEditForm)
class VerbatimEditForm(AdminModalEditForm):
    """Verbatim properties edit form"""

    @property
    def subtitle(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        return translate(_("Verbatim: {}")).format(get_object_label(self.context, self.request, self))

    legend = _("Verbatim properties")
    modal_class = 'modal-xl'

    fields = Fields(IVerbatimInfo).select('title', 'quote', 'author', 'charge')


@adapter_config(required=(IVerbatimInfo, IAdminLayer, IModalPage),
                provides=IFormTitle)
def verbatim_edit_form_title(context, request, view):
    """Verbatim edit form title"""
    settings = get_parent(context, IVerbatimContainer)
    return query_adapter(IFormTitle, request, settings, view)


@adapter_config(required=(IVerbatimInfo, IAdminLayer, VerbatimEditForm),
                provides=IAJAXFormRenderer)
class VerbatimEditFormRenderer(ContextRequestViewAdapter):
    """Verbatim edit form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(self.context.__parent__, self.request,
                                                    IVerbatimTable, self.context)
            ]
        }


#
# Verbatim paragraph add form
#

@viewlet_config(name='add-verbatim-paragraph.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable,
                manager=IContextAddingsViewletManager, weight=600)
class VerbatimParagraphAddMenu(BaseParagraphAddMenu):
    """Verbatim paragraph add menu"""

    label = VERBATIM_PARAGRAPH_NAME
    icon_class = VERBATIM_PARAGRAPH_ICON_CLASS

    factory_name = VERBATIM_PARAGRAPH_TYPE
    href = 'add-verbatim-paragraph.html'


@ajax_form_config(name='add-verbatim-paragraph.html',
                  context=IParagraphContainer, layer=IPyAMSLayer)
class VerbatimParagraphAddForm(BaseParagraphAddForm):
    """Verbatim paragraph add form"""

    content_factory = IVerbatimParagraph


@adapter_config(name='quote',
                required=(IParagraphContainer, IAdminLayer, VerbatimParagraphAddForm),
                provides=IHTMLEditorConfiguration)
@adapter_config(name='quote',
                required=(IVerbatimParagraph, IAdminLayer, IPropertiesEditForm),
                provides=IHTMLEditorConfiguration)
@adapter_config(name='quote',
                required=(IVerbatimContainer, IAdminLayer, IVerbatimForm),
                provides=IHTMLEditorConfiguration)
@adapter_config(name='quote',
                required=(IVerbatimInfo, IAdminLayer, IVerbatimForm),
                provides=IHTMLEditorConfiguration)
def verbatim_quote_editor_configuration(context, request, view):
    """Verbatim quote editor configuration"""
    return {
        'menubar': False,
        'plugins': 'paste textcolor lists charmap link pyams_link',
        'toolbar': 'undo redo | pastetext | h3 h4 | bold italic superscript | '
                   'forecolor backcolor | bullist numlist | '
                   'charmap pyams_link link',
        'toolbar1': False,
        'toolbar2': False,
        'height': 200
    }
