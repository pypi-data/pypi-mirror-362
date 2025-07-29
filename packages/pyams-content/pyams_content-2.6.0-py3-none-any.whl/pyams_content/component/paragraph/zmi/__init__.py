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

"""PyAMS_content.component.paragraph.zmi module

This module provides base paragraphs management components.
"""

from zope.interface import Interface, implementer

from pyams_content.component.association.interfaces import IAssociationContainer
from pyams_content.component.association.zmi.interfaces import IAssociationsTable
from pyams_content.component.paragraph.interfaces import IBaseParagraph, IParagraphContainer, \
    IParagraphContainerTarget, IParagraphFactorySettings, IParagraphFactorySettingsTarget, \
    PARAGRAPH_HIDDEN_FIELDS
from pyams_content.component.paragraph.zmi.helper import get_json_paragraph_toolbar_refresh_event
from pyams_content.component.paragraph.zmi.interfaces import IInnerParagraphEditForm, \
    IParagraphAddForm, IParagraphContainerBaseTable, IParagraphContainerFullTable, \
    IParagraphContainerView, IParagraphRendererSettingsEditForm
from pyams_content.feature.renderer.interfaces import IRendererSettings
from pyams_content.interfaces import IBaseContent, MANAGE_TOOL_PERMISSION
from pyams_content.shared.common.interfaces import IWfSharedContent
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.interfaces import PREVIEW_MODE
from pyams_portal.skin.page import PortalContextPreviewPage
from pyams_portal.zmi.portlet import PortletRendererSettingsEditForm
from pyams_portal.zmi.widget import RendererSelectFieldWidget
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.schema.button import ActionButton
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_utils.adapter import ContextRequestViewAdapter, NullAdapter, adapter_config
from pyams_utils.factory import get_all_factories, get_object_factory
from pyams_utils.request import get_annotations
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.manager import get_label, viewletmanager_config
from pyams_viewlet.viewlet import EmptyContentProvider, contentprovider_config, viewlet_config
from pyams_zmi.form import AdminEditForm, AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_refresh_callback, \
    get_json_table_row_add_callback, get_json_widget_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IEditFormButtons, IFormTitle, IPropertiesEditForm
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IPropertiesMenu, \
    IToolbarViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_hint, get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem
from pyams_zmi.zmi.viewlet.toolbar import AddingsViewletManager

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='paragraph-types.menu',
                context=IParagraphFactorySettingsTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=400,
                permission=MANAGE_TOOL_PERMISSION)
class ParagraphFactorySettingsMenu(NavigationMenuItem):
    """Paragraph factory settings menu"""

    label = _("Paragraphs types")
    href = '#paragraph-types.html'


@ajax_form_config(name='paragraph-types.html',
                  context=IParagraphFactorySettingsTarget, layer=IPyAMSLayer,
                  permission=MANAGE_TOOL_PERMISSION)
class ParagraphFactorySettingsEditForm(AdminEditForm):
    """Paragraph factory settings edit form"""

    title = _("Paragraph types")
    legend = _("Shared content paragraph types")

    fields = Fields(IParagraphFactorySettings)


@adapter_config(required=(IParagraphFactorySettingsTarget, IAdminLayer,
                          ParagraphFactorySettingsEditForm),
                provides=IFormContent)
def get_paragraph_factory_settings_edit_form_content(context, request, form):
    """Paragraph factory settings edit form content getter"""
    return IParagraphFactorySettings(context)


#
# Paragraph add menu
#

@viewletmanager_config(name='pyams.context_addings',
                       context=IParagraphContainerTarget, layer=IAdminLayer,
                       view=IParagraphContainerBaseTable, manager=IToolbarViewletManager, weight=10,
                       provides=IContextAddingsViewletManager)
class ParagraphContainerAddingsViewletManager(AddingsViewletManager):
    """Paragraph container addings viewlet manager"""

    def sort(self, viewlets):
        """Viewlets sorter"""

        def get_sort_order(viewlet):
            menu = viewlet[1]
            if isinstance(menu, MenuDivider):
                return getattr(menu, 'weight', 500), None
            factory = get_object_factory(IBaseParagraph, name=menu.factory_name)
            if factory.factory.secondary:
                return 900, get_label(viewlet, self.request)
            return getattr(menu, 'weight', 500), get_label(viewlet, self.request)

        return sorted(viewlets, key=get_sort_order)


@viewlet_config(name='paragraphs.divider',
                context=IParagraphContainerTarget, layer=IAdminLayer,
                view=IParagraphContainerBaseTable, manager=IContextAddingsViewletManager, weight=500)
class ParagraphAddMenuDivider(ProtectedViewObjectMixin, MenuDivider):
    """Paragraph add menu divider"""

    def __new__(cls, context, request, view, manager):
        target = get_parent(context, IParagraphFactorySettingsTarget)
        if target is None:
            return MenuDivider.__new__(cls)
        has_primary = False
        has_secondary = False
        settings = IParagraphFactorySettings(target)
        factories = settings.allowed_paragraphs or ()
        if not factories:
            factories = (name for name, factory in get_all_factories(IBaseParagraph))
        for factory_name in factories:
            factory = get_object_factory(IBaseParagraph, name=factory_name)
            if factory is None:
                continue
            if factory.factory.secondary:
                has_secondary = True
            else:
                has_primary = True
            if has_primary and has_secondary:
                return MenuDivider.__new__(cls)
        return None


class BaseParagraphAddMenu(ProtectedViewObjectMixin, MenuItem):
    """Base paragraph add menu"""

    factory_name = None
    modal_target = True

    def __new__(cls, context, request, view, manager):
        target = get_parent(context, IParagraphFactorySettingsTarget)
        if target is not None:
            allowed = IParagraphFactorySettings(target).allowed_paragraphs or ()
            if allowed and (cls.factory_name not in allowed):
                return None
        return MenuItem.__new__(cls)

    def get_href(self):
        container = IParagraphContainer(self.context)
        return absolute_url(container, self.request, self.href)


@implementer(IParagraphAddForm)
class BaseParagraphAddForm(AdminModalAddForm):
    """Base paragraph add form"""

    prefix = 'addform.'

    @property
    def subtitle(self):
        translate = self.request.localizer.translate
        factory = get_object_factory(self.content_factory)
        return translate(_("New paragraph: {}")).format(translate(factory.factory.factory_label))

    legend = _("New paragraph properties")
    modal_class = 'modal-xl'

    @property
    def fields(self):
        """Form fields getter"""
        fields = super().fields
        if fields:
            return fields
        return Fields(self.content_factory).omit(*PARAGRAPH_HIDDEN_FIELDS) + \
            Fields(self.content_factory).select('renderer')

    def add(self, obj):
        """Add paragraph to container"""
        IParagraphContainer(self.context).append(obj)


@adapter_config(required=(IParagraphContainer, IAdminLayer, IParagraphAddForm),
                provides=IFormTitle)
def paragraph_add_form_title(context, request, view):
    """Paragraph add form title"""
    parent = get_parent(context, IParagraphContainerTarget)
    return TITLE_SPAN_BREAK.format(
        get_object_hint(parent, request, view),
        get_object_label(parent, request, view))


def get_json_paragraph_editor_open_event(context, request, table_factory, item):
    """Get paragraph editor opening event"""
    factory = get_object_factory(table_factory)
    table = factory(context, request)
    return {
        'module': 'content',
        'callback': 'MyAMS.content.paragraphs.switchEditor',
        'options': {
            'object_id': table.get_row_id(item)
        }
    }


@adapter_config(required=(IParagraphContainer, IAdminLayer, IParagraphAddForm),
                provides=IAJAXFormRenderer)
class ParagraphAddFormRenderer(ContextRequestViewAdapter):
    """Paragraph add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        target = get_parent(self.context, IParagraphContainerTarget)
        table_factory = IParagraphContainerFullTable if IBaseContent.providedBy(target) \
            else IParagraphContainerBaseTable
        callbacks = [
            get_json_table_row_add_callback(self.context, self.request,
                                            table_factory, changes)
        ]
        if IWfSharedContent.providedBy(target):
            callbacks.append(get_json_paragraph_editor_open_event(self.context, self.request,
                                                                  table_factory, changes))
        return {
            'status': 'success',
            'callbacks': callbacks
        }


#
# Paragraphs edit forms
#

@implementer(IPropertiesEditForm)
class ParagraphPropertiesEditFormMixin:
    """Paragraph properties edit form mixin"""

    legend = _("Paragraph properties")

    label_css_class = 'col-sm-2 col-md-3'
    input_css_class = 'col-sm-10 col-md-9'

    @property
    def prefix(self):
        """Form prefix getter"""
        return f'form_{self.context.__name__}.'

    @property
    def fields(self):
        """Form fields getter"""
        fields = super().fields
        if fields:
            return fields
        fields = Fields(self.context.factory_intf).omit(*PARAGRAPH_HIDDEN_FIELDS) + \
            Fields(self.context.factory_intf).select('renderer')
        fields['renderer'].widget_factory = RendererSelectFieldWidget
        return fields


class IInnerParagraphEditFormButtons(IEditFormButtons):
    """Inner paragraph edit form buttons interface"""

    preview = ActionButton(name='preview',
                           title=_("Preview"))


@adapter_config(required=(IBaseParagraph, IAdminLayer),
                provides=IInnerParagraphEditForm)
class InnerParagraphPropertiesEditForm(ParagraphPropertiesEditFormMixin, AdminEditForm):
    """Default inner paragraph edit form"""

    hide_section = True
    title = None

    buttons = Buttons(IInnerParagraphEditFormButtons)
    ajax_form_handler = 'properties.json'

    def update_actions(self):
        """Actions update"""
        super().update_actions()
        preview = self.actions.get('preview')
        if preview is not None:
            preview.icon_class = 'fas fa-binoculars'
            preview.icon_only = True
            preview.href = absolute_url(self.context, self.request, 'modal-preview.html')
            preview.modal_target = True
            preview.hint = self.request.localizer.translate(_("Preview"))

    @handler(IInnerParagraphEditFormButtons['apply'])
    def handle_apply(self, action):
        """Apply button handler"""
        super().handle_apply(self, action)


@adapter_config(required=(IBaseParagraph, IAdminLayer, IParagraphContainerBaseTable),
                provides=ITableElementEditor)
class BaseParagraphTableElementEditor(TableElementEditor):
    """Base paragraph table element editor"""


@adapter_config(required=(IBaseParagraph, IAdminLayer, IParagraphContainerFullTable),
                provides=ITableElementEditor)
class BaseParagraphFullTableElementEditor(NullAdapter):
    """Base paragraph full table element editor"""


@ajax_form_config(name='properties.html',
                  context=IBaseParagraph, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class ParagraphPropertiesEditForm(ParagraphPropertiesEditFormMixin, AdminModalEditForm):
    """Paragraph properties edit form"""

    modal_class = 'modal-xl'


@adapter_config(name='main',
                required=(IBaseParagraph, IAdminLayer, ParagraphPropertiesEditFormMixin),
                provides=IAJAXFormRenderer)
class BaseParagraphPropertiesEditFormRenderer(ContextRequestViewAdapter):
    """Base paragraph properties edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        result = {}
        event = get_json_paragraph_toolbar_refresh_event(self.context, self.request)
        if event is not None:
            result.setdefault('callbacks', []).append(event)
        result.setdefault('callbacks', []).append({
            'callback': 'MyAMS.content.paragraphs.refreshTitle',
            'options': {
                'element_name': self.context.__name__,
                'title': get_object_label(self.context, self.request)
            }
        })
        if 'renderer' in changes.get(self.context.factory_intf, ()):
            result.setdefault('callbacks', []).append(
                get_json_widget_refresh_callback(self.view, 'renderer', self.request))
            renderer = self.context.get_renderer(self.request)
            if (renderer is not None) and (renderer.settings_interface is not None):
                translate = self.request.localizer.translate
                result['closeForm'] = False
                result['messagebox'] = {
                    'status': 'info',
                    'title': translate(_("Updated renderer")),
                    'message': translate(_("You changed renderer selection. Don't omit to "
                                           "check renderer properties...")),
                    'timeout': 5000
                }
        container = IAssociationContainer(self.context, None)
        if container is not None:
            result.setdefault('callbacks', []).append(
                get_json_table_refresh_callback(container, self.request, IAssociationsTable))
        return result


#
# Paragraph renderer properties
#

@ajax_form_config(name='renderer-settings.html',
                  context=IBaseParagraph, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
@implementer(IParagraphRendererSettingsEditForm)
class BaseParagraphRendererSettingsEditForm(PortletRendererSettingsEditForm):
    """Base paragraph renderer settings edit form"""


@adapter_config(required=(IBaseParagraph, IAdminLayer, BaseParagraphRendererSettingsEditForm),
                provides=IFormTitle)
def base_paragraph_renderer_settings_edit_form_title(context, request, form):
    """Base paragraph renderer settings edit form title"""
    container = get_parent(context, IParagraphContainerTarget)
    return TITLE_SPAN_BREAK.format(
        get_object_label(container, request, form),
        get_object_label(context, request, form))


@adapter_config(required=(IBaseParagraph, IAdminLayer, IParagraphRendererSettingsEditForm),
                provides=IFormContent)
def get_paragraph_renderer_settings_edit_form_content(context, request, form):
    """Paragraph renderer settings edit form content getter"""
    renderer = context.get_renderer(request)
    if renderer.settings_interface is None:
        return None
    return IRendererSettings(context)


#
# Paragraph preview
#

@pagelet_config(name='preview.html',
                context=IBaseParagraph, request_type=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class ParagraphPreviewPage(PortalContextPreviewPage):
    """Paragraph preview page"""

    def __init__(self, context, request):
        super().__init__(context, request)
        self.renderer = context.get_renderer(request)

    def update(self):
        """Page update"""
        get_annotations(self.request)[PREVIEW_MODE] = True
        if self.renderer is not None:
            self.renderer.update()

    def render(self):
        """Page renderer"""
        if self.renderer is not None:
            return self.renderer.render()
        return ''


@contentprovider_config(name='pyams_portal.header',
                        context=IBaseParagraph, layer=IPyAMSLayer, view=Interface)
class ParagraphHeaderContentProvider(EmptyContentProvider):
    """Paragraph header content provider"""


@contentprovider_config(name='pyams_portal.footer',
                        context=IBaseParagraph, layer=IPyAMSLayer, view=Interface)
class ParagraphFooterContentProvider(EmptyContentProvider):
    """Paragraph footer content provider"""
