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

"""PyAMS_content.feature.navigation.zmi module

"""

from zope.interface import Interface, implementer

from pyams_content.component.association.zmi import IAssociationsTable
from pyams_content.feature.navigation import IMenu, IMenuLinksContainer, IMenusContainer, \
    IMenusContainerTarget, Menu
from pyams_content.feature.navigation.interfaces import IMenuLinksContainerTarget
from pyams_content.feature.navigation.zmi.interfaces import IMenusTable
from pyams_content.reference.pictogram.zmi.widget import PictogramSelectFieldWidget
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.security import ProtectedViewObjectMixin
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.interfaces import IColumn
from pyams_utils.adapter import ContextRequestViewAdapter, NullAdapter, adapter_config
from pyams_utils.interfaces.intids import IUniqueID
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_row_add_callback, \
    get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectIcon, IObjectLabel, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle, IPropertiesEditForm
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IToolbarViewletManager
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_hint, get_object_label

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='add-mailto-link.menu',
                context=IMenuLinksContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IContextAddingsViewletManager, weight=60)
class MenuLinksContainerMailtoLinkAddMenu(NullAdapter):
    """Menu links container mailto link add menu"""


@adapter_config(name='size',
                required=(IMenuLinksContainer, IAdminLayer, IAssociationsTable),
                provides=IColumn)
class MenuLinksContainerSizeColumn(NullAdapter):
    """Disabled size column in menu links container"""


#
# Menu add form
#

@viewlet_config(name='add-menu.menu',
                context=IMenusContainerTarget, layer=IAdminLayer, view=IAssociationsTable,
                manager=IToolbarViewletManager, weight=10)
class MenuAddAction(ProtectedViewObjectMixin, ContextAddAction):
    """Menu add action"""

    label = Menu.icon_hint
    href = 'add-menu.html'

    def get_href(self):
        """Menu URL target getter"""
        container = IMenusContainer(self.context)
        return absolute_url(container, self.request, self.href)


@ajax_form_config(name='add-menu.html',
                  context=IMenusContainer, layer=IPyAMSLayer)
class MenuAddForm(AdminModalAddForm):
    """Menu add form"""

    modal_class = 'modal-xl'

    subtitle = _("New navigation menu")
    legend = _("New menu properties")

    fields = Fields(IMenu).omit('__parent__', '__name__', 'visible')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget

    content_factory = IMenu

    def add(self, obj):
        oid = IUniqueID(obj).oid
        self.context[oid] = obj


@adapter_config(required=(IMenusContainer, IAdminLayer, MenuAddForm),
                provides=IFormTitle)
def menu_add_form_title(context, request, form):
    """Menu add form title getter"""
    parent = get_parent(context, IMenusContainerTarget)
    hint = get_object_hint(parent, request, form)
    label = get_object_label(parent, request, form)
    return TITLE_SPAN_BREAK.format(hint, label)


@adapter_config(required=(IMenusContainer, IAdminLayer, MenuAddForm),
                provides=IAJAXFormRenderer)
class MenuAddFormRenderer(ContextRequestViewAdapter):
    """Menu add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                IMenusTable, changes)
            ]
        }


@adapter_config(required=(IMenu, IAdminLayer, Interface),
                provides=IObjectIcon)
def menu_icon(context, request, view):
    """Menu icon getter"""
    return Menu.icon_class


@adapter_config(required=(IMenu, IAdminLayer, Interface),
                provides=IObjectHint)
def menu_hint(context, request, view):
    """Menu hint getter"""
    return request.localizer.translate(Menu.icon_hint)


@adapter_config(required=(IMenu, IAdminLayer, Interface),
                provides=IObjectLabel)
def menu_label(context, request, view):
    """Menu label getter"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=(IMenu, IAdminLayer, IMenusTable),
                provides=ITableElementEditor)
class MenuTableElementEditor(TableElementEditor):
    """Menu table element editor"""


@ajax_form_config(name='properties.html',
                  context=IMenu, layer=IPyAMSLayer)
@implementer(IPropertiesEditForm)
class MenuPropertiesEditForm(AdminModalEditForm):
    """Menu properties edit form"""

    @property
    def subtitle(self):
        return get_object_label(self.context, self.request, self)

    legend = _("Menu properties")

    fields = Fields(IMenu).omit('__parent__', '__name__', 'visible')
    fields['pictogram_name'].widget_factory = PictogramSelectFieldWidget


@adapter_config(required=(IMenu, IAdminLayer, IPropertiesEditForm),
                provides=IFormTitle)
def menu_edit_form_title(context, request, view):
    """Menu properties edit form title getter"""
    parent = get_parent(context, IMenusContainerTarget)
    hint = get_object_hint(parent, request, view)
    label = get_object_label(parent, request, view)
    return TITLE_SPAN_BREAK.format(hint, label)


@adapter_config(required=(IMenu, IAdminLayer, MenuPropertiesEditForm),
                provides=IAJAXFormRenderer)
class MenuEditFormRenderer(ContextRequestViewAdapter):
    """Menu edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        parent = get_parent(self.context, IMenusContainer)
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_refresh_callback(parent, self.request,
                                                    IMenusTable, self.context)
            ]
        }
