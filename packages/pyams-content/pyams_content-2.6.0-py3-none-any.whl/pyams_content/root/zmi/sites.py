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

"""PyAMS_content.root.zmi.sites module

This module provides site's root view of sites, hubs and blogs.
"""

from pyramid.decorator import reify
from pyramid.interfaces import IView
from pyramid.view import view_config
from zope.container.interfaces import IContainer
from zope.interface import implementer

from pyams_content.interfaces import MANAGE_SITE_TREE_PERMISSION
from pyams_content.shared.common import IBaseSharedTool
from pyams_content.shared.common.interfaces import IDeletableElement
from pyams_content.zmi.dashboard import DashboardLabelColumn
from pyams_content.zmi.interfaces import IDashboardTable
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflowPublicationInfo
from pyams_zmi.helper.container import delete_container_element
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import ISiteManagementMenu
from pyams_zmi.table import IconColumn, Table, TableAdminView, TrashColumn
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


@implementer(IDashboardTable, IView)
class SiteRootSitesTable(Table):
    """Site root sub-sites table"""

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        attributes['table'].update({
            'data-ams-order': '1,asc'
        })
        return attributes

    display_if_empty = True


@adapter_config(required=(ISiteRoot, IAdminLayer, SiteRootSitesTable),
                provides=IValues)
class SiteRootSitesTableValues(ContextRequestViewAdapter):
    """Site root sites table values"""

    @property
    def values(self):
        """Site root sites tables values getter"""
        yield from filter(IBaseSharedTool.providedBy,
                          IContainer(self.context).values())


@adapter_config(name='visible',
                required=(ISiteRoot, IAdminLayer, SiteRootSitesTable),
                provides=IColumn)
class SiteRootSitesTableVisibleColumn(IconColumn):
    """Site root sites table visible column"""

    weight = 1

    def get_icon_class(self, item):
        info = IWorkflowPublicationInfo(item, None)
        if info is None:
            return None
        if info.is_published():
            return 'fas fa-eye'
        return 'fas fa-eye-slash text-danger opaque'

    def get_icon_hint(self, item):
        info = IWorkflowPublicationInfo(item, None)
        if info is None:
            return None
        translate = self.request.localizer.translate
        if info.is_published():
            return translate(_("Visible site"))
        return translate(_("Not visible site"))


@adapter_config(name='name',
                required=(ISiteRoot, IAdminLayer, SiteRootSitesTable),
                provides=IColumn)
class SiteRootSitesNameColumn(DashboardLabelColumn):
    """Site root site name column"""

    css_classes = {
        'td': 'text-truncate'
    }


@adapter_config(name='trash',
                required=(ISiteRoot, IAdminLayer, SiteRootSitesTable),
                provides=IColumn)
class SiteRootSitesTrashColumn(TrashColumn):
    """Site root sites trash column"""

    hint = _("Delete shared site")
    permission = MANAGE_SITE_TREE_PERMISSION

    def checker(self, item):
        """Trash column checker"""
        deletable = IDeletableElement(item, None)
        if (deletable is not None) and not deletable.is_deletable():
            return False
        return super().has_permission(item)


@viewlet_config(name='root-sites.menu',
                context=ISiteRoot, layer=IAdminLayer,
                manager=ISiteManagementMenu, weight=5,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootSitesMenu(NavigationMenuItem):
    """Site root sites menu"""

    label = _("Site tree")
    icon_class = 'fas fa-sitemap'
    href = '#root-sites.html'


@pagelet_config(name='root-sites.html',
                context=ISiteRoot, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteRootSitesView(TableAdminView):
    """Site root sites view"""

    title = _("Sites, hubs and blogs")

    table_class = SiteRootSitesTable
    table_label = _("Site content")


@view_config(name='delete-element.json',
             context=ISiteRoot, request_type=IPyAMSLayer,
             permission=MANAGE_SITE_TREE_PERMISSION,
             renderer='json', xhr=True)
def delete_siteroot_element(request):
    """Site root delete view"""
    return delete_container_element(request)
