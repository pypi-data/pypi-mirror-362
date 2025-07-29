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

"""PyAMS_content.shared.site.zmi.folder module

"""

from zope.interface import Interface
from zope.intid import IIntIds
from zope.schema import Int, Text

from pyams_content.interfaces import IBaseContent, MANAGE_SITE_PERMISSION
from pyams_content.shared.common.interfaces import IBaseSharedTool
from pyams_content.zmi.properties import PropertiesEditForm
from pyams_content.shared.site.interfaces import ISiteContainer, ISiteFolder, ISiteManager
from pyams_content.shared.site.zmi.interfaces import ISiteTreeTable
from pyams_content.shared.site.zmi.widget.folder import SiteManagerFoldersSelectorFieldWidget
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IGroup
from pyams_i18n.interfaces import II18n, INegotiator
from pyams_i18n.schema import I18nTextLineField
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_skin.interfaces.viewlet import IBreadcrumbItem
from pyams_skin.viewlet.breadcrumb import BreadcrumbItem
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.adapter import adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_utils.unicode import translate_string
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel, TITLE_SPAN_BREAK
from pyams_zmi.interfaces.form import IFormTitle
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IPropertiesMenu, \
    ISiteManagementMenu
from pyams_zmi.table import TableElementEditor
from pyams_zmi.utils import get_object_label
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_content import _


@adapter_config(required=(ISiteFolder, IAdminLayer, Interface),
                provides=IObjectLabel)
def site_folder_label(context, request, view):
    """Site folder label"""
    return II18n(context).query_attribute('title', request=request)


@viewlet_config(name='add-site-folder.menu',
                context=ISiteContainer, layer=IAdminLayer, view=ISiteTreeTable,
                manager=IContextAddingsViewletManager, weight=10,
                permission=MANAGE_SITE_PERMISSION)
class SiteFolderAddMenu(MenuItem):
    """Site folder add menu"""

    label = _("Add site folder...")
    icon_class = 'far fa-folder'

    href = 'add-site-folder.html'
    modal_target = True


class ISiteFolderAddFormFields(Interface):
    """Site folder add form fields interface"""

    title = I18nTextLineField(title=_("Title"),
                              description=_("Visible label used to display content"),
                              required=True)

    parent = Int(title=_("Parent"),
                 description=_("Folder's parent"),
                 required=True)

    notepad = Text(title=_("Notepad"),
                   description=_("Internal information to be known about this content"),
                   required=False)


@ajax_form_config(name='add-site-folder.html',
                  context=ISiteContainer, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_PERMISSION)
class SiteFolderAddForm(AdminModalAddForm):
    """Site folder add form"""

    subtitle = _("New site folder")
    legend = _("New site folder properties")

    fields = Fields(ISiteFolderAddFormFields)
    fields['parent'].widget_factory = SiteManagerFoldersSelectorFieldWidget
    content_factory = ISiteFolder

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'parent' in self.widgets:
            self.widgets['parent'].permission = MANAGE_SITE_PERMISSION

    def update_content(self, content, data):
        data = data.get(self, data)
        # initialize new folder
        content.title = data['title']
        content.short_name = data['title']
        content.notepad = data['notepad']
        intids = get_utility(IIntIds)
        parent = intids.queryObject(data.get('parent'))
        if parent is not None:
            negotiator = get_utility(INegotiator)
            title = II18n(content).get_attribute('title', lang=negotiator.server_language)
            name = translate_string(title, force_lower=True, spaces='-')
            if name in parent:
                index = 1
                new_name = '{name}-{index:02}'.format(name=name, index=index)
                while new_name in parent:
                    index += 1
                    new_name = '{name}-{index:02}'.format(name=name, index=index)
                name = new_name
            parent[name] = content

    def add(self, content):
        """Don't do anything as folder was added in `update_content` method!"""


@adapter_config(required=(ISiteContainer, IAdminLayer, SiteFolderAddForm),
                provides=IFormTitle)
def site_folder_add_form_title(context, request, form):
    """Site folder add form title"""
    manager = get_parent(context, ISiteManager)
    if manager is context:
        return get_object_label(manager, request, form)
    return TITLE_SPAN_BREAK.format(
        get_object_label(manager, request, form),
        get_object_label(context, request, form))


@adapter_config(required=(ISiteFolder, IAdminLayer, Interface),
                provides=ITableElementEditor)
class SiteFolderTableElementEditor(TableElementEditor):
    """Site folder table element editor"""

    view_name = 'admin'
    modal_target = False


@adapter_config(required=(ISiteFolder, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class SiteFolderBreadcrumbs(BreadcrumbItem):
    """Site folder breadcrumb item"""

    @property
    def label(self):
        return II18n(self.context).query_attribute('short_name', request=self.request)

    view_name = 'admin'


@viewletmanager_config(name='properties.menu',
                       context=ISiteFolder, layer=IAdminLayer,
                       manager=ISiteManagementMenu, weight=10,
                       provides=IPropertiesMenu,
                       permission=VIEW_SYSTEM_PERMISSION)
class SiteFolderPropertiesMenu(NavigationMenuItem):
    """Site folder properties menu"""

    label = _("Properties")
    icon_class = 'fas fa-edit'
    href = '#properties.html'


@ajax_form_config(name='properties.html',
                  context=ISiteFolder, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SiteFolderPropertiesEditForm(PropertiesEditForm):
    """Site folder properties edit form"""

    title = _("Site folder properties")
    legend = _("Main folder properties")

    fields = Fields(ISiteFolder).select('title', 'short_name', 'header', 'description') + \
        Fields(IBaseSharedTool).select('shared_content_workflow') + \
        Fields(ISiteFolder).select('notepad')


@adapter_config(required=(ISiteFolder, IAdminLayer, SiteFolderPropertiesEditForm),
                provides=IAJAXFormRenderer)
class SiteFolderPropertiesEditFormRenderer(AJAXFormRenderer):
    """Site folder properties edit form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        if 'title' in changes.get(IBaseContent, ()):
            return {
                'status': 'reload',
                'message': self.request.localizer.translate(self.form.success_message)
            }
        return super().render(changes)


@adapter_config(name='navigation',
                required=(ISiteFolder, IAdminLayer, SiteFolderPropertiesEditForm),
                provides=IGroup)
class SiteFolderPropertiesEditFormNavigationGroup(FormGroupSwitcher):
    """Site folder properties edit form navigation group"""

    legend = _("Navigation properties")
    weight = 10

    fields = Fields(ISiteFolder).select('visible_in_list', 'navigation_title', 'navigation_mode')
