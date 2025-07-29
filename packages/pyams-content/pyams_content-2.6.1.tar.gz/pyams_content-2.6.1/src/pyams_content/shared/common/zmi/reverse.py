# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import Eq, Or
from pyramid.interfaces import IView
from zope.interface import implementer

from pyams_catalog.query import CatalogResultSet
from pyams_content.shared.common.interfaces import IWfSharedContent
from pyams_content.shared.site.interfaces import ISiteContainer
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentType, IDashboardTable
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.interfaces import IPortalTemplate
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_table.interfaces import IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.list import unique_iter_max
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflowState
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IContentManagementMenu
from pyams_zmi.table import Table, TableAdminView
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _  # pylint: disable=ungrouped-imports


@viewlet_config(name='reverse-links.menu',
                context=IWfSharedContent, layer=IAdminLayer,
                manager=IContentManagementMenu, weight=40,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedContentReverseLinksMenu(NavigationMenuItem):
    """Shared content reverse links menu"""
    
    label = _("Reverse links")
    icon_class = 'fas fa-anchor'
    href = '#reverse-links.html'
    
    
@implementer(IView, IDashboardTable)
class SharedContentReverseLinksTable(Table):
    """Shared content reverse links table"""
    
    object_data = {
        'responsive': True,
        'auto-width': False,
        'searching': False,
        'length-change': False
    }
    
    sort_on = None


@adapter_config(required=(IPortalTemplate, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentType)
def portal_template_content_type(context, request, column):
    """Portal template content type adapter"""
    return _("Portal template")


@adapter_config(required=(IWfSharedContent, IAdminLayer, SharedContentReverseLinksTable),
                provides=IValues)
class SharedContentReverseLinksValuesAdapter(ContextRequestViewAdapter):
    """Shared content reverse links values adapter"""

    @property
    def values(self):
        """Reverse links getter"""

        def get_item(result):
            parent = get_parent(result, IWfSharedContent)
            if parent is not None:
                return parent
            parent = get_parent(result, IPortalTemplate)
            if parent is None:
                parent = get_parent(result, ISiteContainer)
            if parent is None:
                parent = self.request.root
            return parent
        
        def get_key(item):
            return getattr(ISequentialIdInfo(item, None), 'oid', None) or ICacheKeyValue(item)
        
        def get_sort_key(item):
            return getattr(IWorkflowState(item, None), 'version_id', None) or ICacheKeyValue(item)
        
        catalog = get_utility(ICatalog)
        oid = ISequentialIdInfo(self.context).hex_oid
        params = Or(Eq(catalog['link_reference'], oid),
                    Eq(catalog['link_references'], oid))
        yield from unique_iter_max(map(get_item,
                                       CatalogResultSet(CatalogQuery(catalog).query(params))),
                                   key=get_key,
                                   sort_key=get_sort_key)


@pagelet_config(name='reverse-links.html',
                context=IWfSharedContent, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
class SharedContentReverseLinksView(TableAdminView):
    """Shared content reverse links view"""
    
    title = _("Shared content reverse links")
    
    table_class = SharedContentReverseLinksTable
    table_label = _("List of internal links")
    