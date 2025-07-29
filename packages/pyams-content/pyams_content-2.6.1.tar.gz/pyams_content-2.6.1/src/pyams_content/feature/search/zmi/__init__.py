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

"""PyAMS_content.feature.search.zmi module

This module defines management components for search folders.
"""

from zope.interface import Interface

from pyams_content.feature.search import ISearchFolder
from pyams_content.interfaces import CREATE_CONTENT_PERMISSION, MANAGE_CONTENT_PERMISSION, MANAGE_SITE_PERMISSION
from pyams_content.shared.site.interfaces import ISiteContainer
from pyams_content.shared.site.zmi.folder import ISiteFolderAddFormFields, SiteFolderAddForm
from pyams_content.shared.site.zmi.interfaces import ISiteTreeTable
from pyams_content.shared.site.zmi.widget.folder import SiteManagerFoldersSelectorFieldWidget
from pyams_content.shared.view.zmi import ViewPropertiesEditForm, ViewPropertiesGroup
from pyams_content.workflow.zmi.publication import SiteItemPublicationDatesMenu
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security_views.zmi.interfaces import IObjectSecurityMenu
from pyams_skin.interfaces.viewlet import IBreadcrumbItem, IHelpViewletManager
from pyams_skin.viewlet.breadcrumb import BreadcrumbItem
from pyams_skin.viewlet.menu import MenuDivider, MenuItem
from pyams_utils.adapter import NullAdapter, adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.form import IPropertiesEditForm
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContentManagementMenu, IContextActionsDropdownMenu, \
    IContextAddingsViewletManager, IMenuHeader, IPropertiesMenu
from pyams_zmi.table import TableElementEditor

__docformat__ = 'restructuredtext'

from pyams_content import _
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


@viewlet_config(name='add-search-folder.divider',
                context=ISiteContainer, layer=IAdminLayer, view=ISiteTreeTable,
                manager=IContextAddingsViewletManager, weight=89,
                permission=MANAGE_SITE_PERMISSION)
class SearchFolderAddMenuDivider(MenuDivider):
    """Search folder add menu divider"""


@viewlet_config(name='add-search-folder.menu',
                context=ISiteContainer, layer=IAdminLayer, view=ISiteTreeTable,
                manager=IContextAddingsViewletManager, weight=90,
                permission=MANAGE_SITE_PERMISSION)
class SearchFolderAddMenu(MenuItem):
    """Search folder add menu"""

    label = _("Add search folder...")
    icon_class = 'fas fa-search'

    href = 'add-search-folder.html'
    modal_target = True


class ISearchFolderAddFormFields(ISiteFolderAddFormFields):
    """Search folder add form fields interface"""


@ajax_form_config(name='add-search-folder.html',
                  context=ISiteContainer, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_PERMISSION)
class SearchFolderAddForm(SiteFolderAddForm):
    """Search folder add form"""

    subtitle = _("New search folder")
    legend = _("New search folder properties")

    fields = Fields(ISearchFolderAddFormFields)
    fields['parent'].widget_factory = SiteManagerFoldersSelectorFieldWidget
    content_factory = ISearchFolder

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        if 'parent' in self.widgets:
            self.widgets['parent'].permission = MANAGE_SITE_PERMISSION


@adapter_config(required=(ISearchFolder, IAdminLayer, Interface),
                provides=IObjectLabel)
def search_folder_label(context, request, view):
    """Search folder label"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=(ISearchFolder, IAdminLayer, Interface, IContentManagementMenu),
                provides=IMenuHeader)
def search_folder_management_menu_header(context, request, view, manager):
    """Search folder management menu header"""
    return request.localizer.translate(_("Search folder management"))


@adapter_config(required=(ISearchFolder, IAdminLayer, Interface),
                provides=ITableElementEditor)
class SearchFolderTableElementEditor(TableElementEditor):
    """Search folder table element editor"""

    view_name = 'admin'
    modal_target = False


@viewlet_config(name='workflow-publication.menu',
                context=ISearchFolder, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=510,
                permission=MANAGE_SITE_PERMISSION)
class SearchFolderPublicationDatesMenu(SiteItemPublicationDatesMenu):
    """Search folder publication dates menu"""

    def __new__(cls, context, request, view, manager):
        return NavigationMenuItem.__new__(cls)


@adapter_config(required=(ISearchFolder, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class SearchFolderBreadcrumbs(BreadcrumbItem):
    """Search folder breadcrumb item"""

    @property
    def label(self):
        return II18n(self.context).query_attribute('short_name', request=self.request)

    view_name = 'admin'


@adapter_config(name='view-properties',
                required=(ISearchFolder, IAdminLayer, ViewPropertiesEditForm),
                provides=IGroup)
class SearchFolderPropertiesGroup(ViewPropertiesGroup):
    """View properties group"""

    legend = _("Folder search settings")

    fields = Fields(ISearchFolder).select('selected_content_types', 'selected_datatypes',
                                          'excluded_content_types', 'excluded_datatypes', 'allow_user_params',
                                          'order_by', 'reversed_order', 'limit', 'age_limit')


@viewlet_config(name='view-properties.help',
                context=ISearchFolder, layer=IAdminLayer, view=ViewPropertiesGroup,
                manager=IHelpViewletManager, weight=10)
class SearchFolderPropertiesHelp(NullAdapter):
    """Search folder properties help"""


@adapter_config(name='navigation',
                required=(ISearchFolder, IAdminLayer, IPropertiesEditForm),
                provides=IGroup)
class SearchFolderPropertiesEditFormNavigationGroup(FormGroupSwitcher):
    """Search folder properties edit form navigation group"""

    legend = _("Navigation properties")
    weight = 10

    fields = Fields(ISearchFolder).select('visible_in_list', 'navigation_title')


@viewlet_config(name='change-owner.menu',
                context=ISearchFolder, layer=IAdminLayer, view=Interface,
                manager=IObjectSecurityMenu, weight=300,
                permission=MANAGE_SITE_PERMISSION)
class SearchFolderOwnerChangeMenu(NullAdapter):
    """Search folder owner change menu is disabled"""


@viewlet_config(name='duplicate-content.divider',
                context=ISearchFolder, layer=IAdminLayer,
                manager=IContextActionsDropdownMenu, weight=49,
                permission=CREATE_CONTENT_PERMISSION)
class SearchFolderDuplicateMenuDivider(NullAdapter):
    """Search folder duplication menu divider is disabled"""


@viewlet_config(name='duplicate-content.menu',
                context=ISearchFolder, layer=IAdminLayer,
                manager=IContextActionsDropdownMenu, weight=50,
                permission=CREATE_CONTENT_PERMISSION)
class SearchFolderDuplicateMenu(NullAdapter):
    """Search folder duplication menu item is disabled"""


@viewlet_config(name='content-review.menu',
                context=ISearchFolder, layer=IAdminLayer,
                manager=IContextActionsDropdownMenu, weight=10,
                permission=MANAGE_CONTENT_PERMISSION)
class SearchFolderReviewMenu(NullAdapter):
    """Search folder review menu is disabled"""
