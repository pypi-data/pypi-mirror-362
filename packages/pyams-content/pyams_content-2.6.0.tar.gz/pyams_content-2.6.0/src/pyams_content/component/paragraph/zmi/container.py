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

"""PyAMS_content.component module

"""

import json

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPInternalServerError, HTTPNotFound, HTTPServiceUnavailable
from pyramid.interfaces import IView
from pyramid.view import view_config
from zope.contentprovider.interfaces import IContentProvider
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import implementer

from pyams_content.component.association.interfaces import IAssociationContainerTarget
from pyams_content.component.association.zmi.container import AssociationsTableView
from pyams_content.component.paragraph.interfaces import IBaseParagraph, IParagraphContainer, \
    IParagraphContainerTarget
from pyams_content.component.paragraph.zmi.interfaces import IInnerParagraphEditForm, \
    IParagraphContainerBaseTable, IParagraphContainerFullTable, IParagraphContainerView, \
    IParagraphTitleToolbar
from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION, PUBLISH_CONTENT_PERMISSION
from pyams_content.shared.common.interfaces import IWfSharedContent
from pyams_content.shared.common.interfaces.types import ITypedSharedTool
from pyams_content.shared.common.zmi.types.interfaces import ISharedToolTypesTable
from pyams_content.zmi import content_js
from pyams_layer.interfaces import IPyAMSLayer
from pyams_layer.skin import apply_skin
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.viewlet import IContentPrefixViewletManager
from pyams_table.interfaces import IColumn, IValues
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.traversing import get_parent
from pyams_viewlet.manager import TemplateBasedViewletManager, WeightOrderedViewletManager, \
    viewletmanager_config
from pyams_viewlet.viewlet import ViewContentProvider, viewlet_config
from pyams_workflow.interfaces import IWorkflowState
from pyams_zmi.form import AdminModalDisplayForm
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.skin import AdminSkin
from pyams_zmi.table import ActionColumn, AttributeSwitcherColumn, ContentTypeColumn, \
    IconColumn, InnerTableAdminView, MultipleTablesAdminView, NameColumn, ReorderColumn, Table, \
    TableAdminView, TrashColumn, VisibilityColumn, get_ordered_data_attributes, get_table_id
from pyams_zmi.utils import get_object_hint, get_object_icon, get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@factory_config(IParagraphContainerBaseTable)
class ParagraphsBaseTable(Table):
    """Paragraphs container table"""

    @reify
    def data_attributes(self):
        """Attributes getter"""
        attributes = super().data_attributes
        attributes.setdefault('table', {}).update({
            'data-ams-modules': json.dumps({
                'content': {
                    'src': get_resource_path(content_js)
                }
            })
        })
        container = IParagraphContainer(self.context)
        get_ordered_data_attributes(self, attributes, container, self.request)
        return attributes

    display_if_empty = True


@factory_config(IParagraphContainerFullTable)
@implementer(IView)
class ParagraphsTable(ParagraphsBaseTable):
    """Full paragraphs table"""


@adapter_config(required=(IParagraphContainer, IAdminLayer, IParagraphContainerBaseTable),
                provides=IValues)
class ParagraphContainerValues(ContextRequestViewAdapter):
    """Paragraph container values adapter"""

    @property
    def values(self):
        """Paragraph container values getter"""
        yield from IParagraphContainer(self.context).values()


@adapter_config(name='reorder',
                required=(IParagraphContainer, IAdminLayer, IParagraphContainerBaseTable),
                provides=IColumn)
class ParagraphsReorderColumn(ReorderColumn):
    """Paragraphs reorder column"""


@view_config(name='reorder.json',
             context=IParagraphContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def reorder_paragraphs_table(request):
    """Reorder paragraphs"""
    order = request.params.get('order').split(';')
    request.context.updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='visible',
                required=(IParagraphContainer, IAdminLayer, IParagraphContainerBaseTable),
                provides=IColumn)
class ParagraphsVisibleColumn(VisibilityColumn):
    """Paragraphs table visible column"""


@view_config(name='switch-visible-item.json',
             context=IParagraphContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_item(request):
    """Switch visible item"""
    return switch_element_attribute(request)


@adapter_config(name='anchor',
                required=(IParagraphContainer, IAdminLayer, IParagraphContainerBaseTable),
                provides=IColumn)
class ParagraphsAnchorColumn(AttributeSwitcherColumn):
    """Paragraphs table anchor column"""

    attribute_name = 'anchor'
    attribute_switcher = 'switch-anchor-item.json'

    icon_on_class = 'fas fa-anchor'
    icon_off_class = 'fas fa-anchor opacity-25'

    weight = 2

    def get_icon_hint(self, item):
        """Icon hint getter"""
        if self.has_permission(item):
            hint = _("Click to set/unset paragraph as navigation anchor")
        elif item.anchor:
            hint = _("This paragraph is defined as a navigation anchor")
        else:
            hint = _("This paragraph is not defined as a navigation anchor")
        return self.request.localizer.translate(hint)


@view_config(name='switch-anchor-item.json',
             context=IParagraphContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_anchor_item(request):
    """Switch anchor item"""
    return switch_element_attribute(request)


@adapter_config(name='icon',
                required=(IParagraphContainer, IAdminLayer, IParagraphContainerBaseTable),
                provides=IColumn)
class ParagraphsIconColumn(ContentTypeColumn):
    """Paragraphs table icon column"""
    
    
@viewletmanager_config(name='pyams_content.paragraph.title-toolbar',
                       context=IBaseParagraph, layer=IAdminLayer,
                       view=IParagraphContainerBaseTable,
                       provides=IParagraphTitleToolbar)
@template_config(template='templates/title-toolbar.pt', layer=IAdminLayer)
class ParagraphTitleToolbar(TemplateBasedViewletManager, WeightOrderedViewletManager):
    """Paragraph title toolbar viewlet manager"""

    render_empty = True

    @property
    def id(self):
        """Unique ID getter"""
        return f'{get_table_id(self.view)}_title_{self.context.__name__}'


class ParagraphTitleToolbarItemMixin:
    """Paragraph title toolbar item"""

    icon_hint = None
    icon_class = None

    target_intf = None
    item_intf = None

    counter = 0

    def update(self):
        target = self.target_intf(self.context, None)
        if target is None:
            return
        self.counter = sum(1 for _ in filter(self.item_intf.providedBy, target.values()))

    def checker(self):
        """Context checker"""
        return self.counter > 0

    def render(self):
        """Viewlet render"""
        if not self.checker():
            return ''
        translate = self.request.localizer.translate
        return f'<span class="px-2">' \
               f'  {self.counter or ""} ' \
               f'  <i class="{self.icon_class} hint pl-1" ' \
               f'     data-original-title="{translate(self.icon_hint)}"></i>' \
               f'</span>'


@adapter_config(name='label',
                required=(IParagraphContainer, IAdminLayer, IParagraphContainerBaseTable),
                provides=IColumn)
class ParagraphsLabelColumn(NameColumn):
    """Paragraphs label column"""

    i18n_header = _("Title")

    css_classes = {
        'td': 'title'
    }


@adapter_config(name='label',
                required=(IParagraphContainer, IAdminLayer, IParagraphContainerFullTable),
                provides=IColumn)
class ParagraphsFullLabelColumn(ParagraphsLabelColumn):
    """Paragraphs label column"""

    i18n_header = _("Show/hide all paragraphs")
    head_hint = _("Click to show/hide all paragraphs editors")
    cell_hint = _("Click to show/hide paragraph editor")
    modified_hint = _("Created or modified in this version")

    css_classes = {}

    def render_head_cell(self):
        """Head cell renderer"""
        hint = self.request.localizer.translate(self.head_hint)
        return f'<span data-ams-click-handler="MyAMS.content.paragraphs.switchAllEditors" ' \
               f'      data-ams-stop-propagation="true">' \
               f'  <span class="switcher mr-2 hint" data-original-title="{hint}">' \
               f'    <i class="far fa-plus-square"></i>' \
               f'  </span>' \
               f'  <span class="title">{super().render_head_cell()}</span>' \
               f'</span>'

    def render_cell(self, item):
        """Cell renderer"""
        modified_icon = ''
        item_dc = IZopeDublinCore(item, None)
        if item_dc is not None:
            content = get_parent(item, IWfSharedContent)
            if content is not None:
                state = IWorkflowState(content, None)
                if (state is not None) and (state.version_id > 1):
                    content_dc = IZopeDublinCore(content, None)
                    if (content_dc is not None) and (item_dc.modified > content_dc.created):
                        translate = self.request.localizer.translate
                        hint = translate(self.modified_hint)
                        modified_icon = f' <i class="fas fa-fw fa-sm fa-circle text-warning hint mx-2"' \
                                        f'    data-original-title="{hint}"></i>'
        toolbar = ''
        provider = self.request.registry.queryMultiAdapter(
            (item, self.request, self.table), IContentProvider,
            name='pyams_content.paragraph.title-toolbar')
        if provider is not None:
            provider.update()
            toolbar = provider.render()
        hint = self.request.localizer.translate(self.cell_hint)
        return f'<div class="switcher-parent" ' \
               f'     data-ams-click-handler="MyAMS.content.paragraphs.switchEditor" ' \
               f'     data-ams-stop-propagation="true">' \
               f'  <span class="switcher mr-2 hint" data-original-title="{hint}">' \
               f'    <i class="far fa-plus-square"></i>' \
               f'  </span>' \
               f'  <span class="title">{super().render_cell(item)}</span>' \
               f'  <span>{modified_icon}</span>' \
               f'  {toolbar}' \
               f'</div>' \
               f'<div class="editor"></div>'


@adapter_config(name='lock',
                required=(IParagraphContainer, IAdminLayer, IParagraphContainerBaseTable),
                provides=IColumn)
class ParagraphsLockColumn(AttributeSwitcherColumn):
    """Paragraphs lock column"""

    permission = PUBLISH_CONTENT_PERMISSION

    attribute_name = 'locked'
    attribute_switcher = 'switch-paragraph-lock.json'

    icon_on_class = 'fas fa-lock'
    icon_off_class = 'fas fa-unlock opacity-50'

    weight = 900

    def get_icon_hint(self, item):
        """Icon hint getter"""
        if self.has_permission(item):
            hint = _("Click to lock/unlock paragraph")
        elif item.locked:
            hint = _("This paragraph is locked and can't be removed!")
        else:
            hint = _("This paragraph is not locked")
        return self.request.localizer.translate(hint)


@view_config(name='switch-paragraph-lock.json',
             context=IParagraphContainer, request_type=IPyAMSLayer,
             permission=MANAGE_CONTENT_PERMISSION,
             renderer='json', xhr=True)
def switch_paragraph_lock(request):
    """Switch paragraph lock"""
    return switch_element_attribute(request)


@adapter_config(name='trash',
                required=(IParagraphContainer, IAdminLayer, IParagraphContainerBaseTable),
                provides=IColumn)
class ParagraphsTrashColumn(TrashColumn):
    """Paragraphs table trash column"""


@view_config(name='delete-element.json',
             context=IParagraphContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def delete_data_type(request):
    """Delete data type"""
    return delete_container_element(request)


#
# Paragraphs table and views
#

@viewlet_config(name='paragraphs.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=100,
                permission=VIEW_SYSTEM_PERMISSION)
class ParagraphsMenu(NavigationMenuItem):
    """Paragraphs menu"""

    label = _("Paragraphs")
    href = '#paragraphs.html'


class ParagraphsContainerViewMixin:
    """Paragraphs container view mixin class"""

    table_class = IParagraphContainerBaseTable
    table_label = _("Paragraphs list")

    container_intf = IParagraphContainer


@pagelet_config(name='paragraphs.html',
                context=IParagraphContainerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
@implementer(IParagraphContainerView)
class ParagraphsContainerView(ParagraphsContainerViewMixin, TableAdminView):
    """Paragraphs container view"""

    table_class = IParagraphContainerFullTable


@adapter_config(name='paragraphs',
                required=(ITypedSharedTool, IAdminLayer, ISharedToolTypesTable),
                provides=IColumn)
class SharedToolTypesParagraphsColumn(ActionColumn):
    """Shared tool data types table paragraphs column"""

    hint = _("Default paragraphs")
    icon_class = 'fas fa-paragraph'

    href = 'paragraphs-modal.html'
    modal_target = True

    weight = 400


@pagelet_config(name='paragraphs-modal.html',
                context=IParagraphContainerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class ParagraphsContainerModalView(AdminModalDisplayForm):
    """Paragraphs container modal view"""

    subtitle = _("Paragraphs")
    modal_class = 'modal-xl'
    modal_content_class = 'min-height-50vh'


@adapter_config(required=(IParagraphContainerTarget, IAdminLayer, ParagraphsContainerModalView),
                provides=IFormTitle)
def paragraph_container_modal_view_title(context, request, view):
    """Paragraph container modal view title"""
    hint = get_object_hint(context, request, view)
    label = get_object_label(context, request, view)
    return TITLE_SPAN_BREAK.format(hint, label)


@viewlet_config(name='paragraphs-modal-table',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=ParagraphsContainerModalView,
                manager=IContentPrefixViewletManager, weight=10)
class ParagraphsContainerTableView(ParagraphsContainerViewMixin, InnerTableAdminView):
    """Paragraphs container table view"""


@view_config(name='get-paragraphs-editors.json',
             context=IParagraphContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=VIEW_SYSTEM_PERMISSION)
def get_paragraphs_editors(request):
    """Get internal editors of all paragraphs"""
    apply_skin(request, AdminSkin)
    result = {}
    for name, element in IParagraphContainer(request.context).items():
        editor = request.registry.queryMultiAdapter((element, request), IInnerParagraphEditForm)
        if editor is None:
            raise HTTPInternalServerError("Can't get inner paragraphs editors!")
        editor.update()
        result[name] = editor.render()
    return result


@view_config(name='get-paragraph-editor.json',
             context=IParagraphContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True,
             permission=VIEW_SYSTEM_PERMISSION)
def get_paragraph_editor(request):
    """Get internal editor of a paragraph"""
    name = request.params.get('object_name')
    if not name:
        raise HTTPServiceUnavailable()
    element = IParagraphContainer(request.context).get(name)
    if element is None:
        raise HTTPNotFound()
    apply_skin(request, AdminSkin)
    editor = request.registry.queryMultiAdapter((element, request), IInnerParagraphEditForm)
    if editor is None:
        raise HTTPInternalServerError("Can't get inner paragraph editor!")
    editor.update()
    return {
        element.__name__: editor.render()
    }


#
# Paragraphs associations view components
#

@viewlet_config(name='paragraphs-associations.menu',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=110,
                permission=VIEW_SYSTEM_PERMISSION)
class ParagraphsAssociationsMenu(NavigationMenuItem):
    """Paragraphs associations menu"""

    label = _("Links and attachments")
    href = '#paragraphs-associations.html'


class ParagraphAssociationsTableView(AssociationsTableView, ViewContentProvider):
    """Paragraph associations table view"""

    @property
    def table_label(self):
        """Table label getter"""
        return f'<i class="fa-fw {get_object_icon(self.context, self.request)} hint mr-1"' \
               f'   data-original-title="{get_object_hint(self.context, self.request)}"></i> ' \
               f'{get_object_label(self.context, self.request)}'


@pagelet_config(name='paragraphs-associations.html',
                context=IParagraphContainerTarget, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class ParagraphsAssociationsView(MultipleTablesAdminView):
    """Paragraphs associations view"""

    table_label = _("Content blocks links and attachments")

    @reify
    def tables(self):
        """Tables getter"""
        result = []
        container = IParagraphContainer(self.context)
        for paragraph in filter(IAssociationContainerTarget.providedBy, container.values()):
            result.append(ParagraphAssociationsTableView(paragraph, self.request, self))
        return result
