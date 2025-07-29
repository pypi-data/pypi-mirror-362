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

"""PyAMS_content.shared.site.zmi.manager module

This module provides site manager management interface components.
"""

from pyramid.events import subscriber
from zope.interface import Interface, Invalid

from pyams_content.interfaces import IBaseContent, MANAGE_SITE_TREE_PERMISSION
from pyams_content.root.zmi.sites import SiteRootSitesTable
from pyams_content.shared.common.interfaces import IBaseSharedTool, ISharedSite
from pyams_content.shared.site.interfaces import ISiteManager
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentType, \
    ISiteRootDashboardContentType
from pyams_content.zmi.properties import PropertiesEditForm
from pyams_form.ajax import AJAXFormRenderer, ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_i18n.interfaces import II18n, INegotiator
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_skin.interfaces.viewlet import IBreadcrumbItem
from pyams_skin.viewlet.breadcrumb import BreadcrumbItem
from pyams_skin.viewlet.menu import MenuItem
from pyams_table.interfaces import ITable
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.unicode import translate_string
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm
from pyams_zmi.helper.event import get_json_table_row_add_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectLabel
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, \
    IMenuHeader, IPropertiesMenu, ISiteManagementMenu
from pyams_zmi.table import TableElementEditor
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@viewlet_config(name='add-site-manager.menu',
                context=ISiteRoot, layer=IAdminLayer, view=SiteRootSitesTable,
                manager=IContextAddingsViewletManager,
                permission=MANAGE_SITE_TREE_PERMISSION)
class SiteManagerAddMenu(MenuItem):
    """Site manager add menu"""

    label = _("Add site manager")
    icon_class = 'fas fa-sitemap'

    href = 'add-site-manager.html'
    modal_target = True


@ajax_form_config(name='add-site-manager.html',
                  context=ISiteRoot, layer=IPyAMSLayer,
                  permission=MANAGE_SITE_TREE_PERMISSION)
class SiteManagerAddForm(AdminModalAddForm):
    """Site manager add form"""

    title = _("Add site manager")
    legend = _("New site properties")

    fields = Fields(ISiteManager).select('title', 'short_name')
    content_factory = ISiteManager

    _edit_permission = MANAGE_SITE_TREE_PERMISSION

    def add(self, obj):
        short_name = II18n(obj).query_attribute('short_name', request=self.request)
        name = translate_string(short_name, force_lower=True, spaces='-')
        self.context[name] = obj


@subscriber(IDataExtractedEvent, form_selector=SiteManagerAddForm)
def handle_new_site_manager_data(event):
    """Handle new site manager data"""
    data = event.data
    negotiator = get_utility(INegotiator)
    name = data.get('short_name', {}).get(negotiator.server_language)
    if not name:
        event.form.widgets.errors += (Invalid(_("Site name is required!")),)
    else:
        name = translate_string(name, force_lower=True, spaces='-')
        if name in event.form.context:
            event.form.widgets.errors += (Invalid(_("A site manager is already registered with "
                                                    "this name!")),)


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteManagerAddForm),
                provides=IAJAXFormRenderer)
class SiteManagerAddFormRenderer(ContextRequestViewAdapter):
    """Site manager add form renderer"""

    def render(self, changes):
        if changes is None:
            return None
        return {
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                SiteRootSitesTable, changes)
            ]
        }


@adapter_config(required=(ISiteManager, IAdminLayer, Interface),
                provides=IObjectLabel)
def site_manager_label(context, request, view):
    """Site manager table element name"""
    return II18n(context).query_attribute('title', request=request)


@adapter_config(required=(ISiteManager, IAdminLayer, ITable),
                provides=ITableElementEditor)
class SiteManagerTableElementEditor(TableElementEditor):
    """Site manager table element editor"""

    view_name = 'admin'
    modal_target = False


@adapter_config(required=(ISiteManager, IAdminLayer, Interface),
                provides=IBreadcrumbItem)
class SiteManagerBreadcrumbs(BreadcrumbItem):
    """Site manager breadcrumb item"""

    @property
    def label(self):
        return II18n(self.context).query_attribute('short_name', request=self.request)

    view_name = 'admin'
    css_class = 'breadcrumb-item persistent strong'


@adapter_config(required=(ISiteManager, IAdminLayer, Interface, ISiteManagementMenu),
                provides=IMenuHeader)
def site_manager_management_menu_header(context, request, view, manager):
    """Site manager management menu header adapter"""
    return _("Site management")


@viewletmanager_config(name='properties.menu',
                       context=ISiteManager, layer=IAdminLayer,
                       manager=ISiteManagementMenu, weight=10,
                       provides=IPropertiesMenu,
                       permission=VIEW_SYSTEM_PERMISSION)
class SiteManagerPropertiesMenu(NavigationMenuItem):
    """Site manager properties menu"""

    label = _("Properties")
    icon_class = 'fas fa-edit'
    href = '#properties.html'


@ajax_form_config(name='properties.html',
                  context=ISiteManager, layer=IPyAMSLayer,
                  permission=VIEW_SYSTEM_PERMISSION)
class SiteManagerPropertiesEditForm(PropertiesEditForm):
    """Site manager properties edit form"""

    title = _("Site manager properties")
    legend = _("Main site properties")

    fields = Fields(ISiteManager).select('title', 'short_name', 'header', 'description') + \
        Fields(IBaseSharedTool).select('shared_content_workflow') + \
        Fields(ISiteManager).select('navigation_mode', 'indexation_mode', 'notepad')


@adapter_config(required=(ISiteManager, IAdminLayer, SiteManagerPropertiesEditForm),
                provides=IAJAXFormRenderer)
class SiteManagerPropertiesEditFormRenderer(AJAXFormRenderer):
    """Site manager properties edit form renderer"""

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


#
# Dashboards management adapters
#

@adapter_config(required=(ISharedSite, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentType)
@adapter_config(required=(ISharedSite, IAdminLayer, IDashboardColumn),
                provides=ISiteRootDashboardContentType)
def site_manager_content_type(context, request, column):
    """Site manager content-type getter"""
    return request.localizer.translate(context.content_name)
