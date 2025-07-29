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

"""PyAMS_content.shared.site.zmi.tree module

This module defines components which are used to display the whole site tree.
"""

import json

from pyramid.decorator import reify
from pyramid.interfaces import IView
from pyramid.location import lineage
from pyramid.view import view_config
from zope.interface import implementer
from zope.intid import IIntIds
from zope.lifecycleevent import ObjectMovedEvent

from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION, MANAGE_SITE_PERMISSION
from pyams_content.shared.site.interfaces import IBaseSiteItem, ISiteContainer, ISiteElement, \
    ISiteManager, SITE_CONTAINER_REDIRECT_MODE
from pyams_content.shared.site.zmi.interfaces import ISiteTreeTable
from pyams_content.zmi import content_js
from pyams_content.zmi.dashboard import DashboardContentNumberColumn, DashboardContentOwnerColumn, \
    DashboardContentStatusColumn, DashboardContentStatusDatetimeColumn, \
    DashboardContentStatusPrincipalColumn, DashboardContentTimestampColumn, \
    DashboardContentTypeColumn, DashboardContentVersionColumn, DashboardLabelColumn, \
    DashboardVisibilityColumn
from pyams_content.zmi.interfaces import IDashboardColumn, IDashboardContentType, \
    IDashboardContentVisibility, IDashboardTable, IDashboardView
from pyams_layer.interfaces import IPyAMSLayer
from pyams_layer.skin import apply_skin
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_site.interfaces import ISiteRoot
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.fanstatic import get_resource_path
from pyams_utils.interfaces.traversing import IPathElements
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_workflow.interfaces import IWorkflowPublicationInfo
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import IReorderColumn
from pyams_zmi.interfaces.viewlet import ISiteManagementMenu
from pyams_zmi.skin import AdminSkin
from pyams_zmi.table import ReorderColumn, Table, TableAdminView, TrashColumn, get_table_id
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

__docformat__ = 'restructuredtext'

from pyams_content import _


def get_item_order(item):
    """Get item order value"""
    for site_item in reversed(list(lineage(item))):
        parent = get_parent(site_item, ISiteContainer)
        if parent is None:
            continue
        index = list(site_item.__parent__.keys()).index(site_item.__name__)
        yield f'{index:03}'


@implementer(IDashboardTable, ISiteTreeTable, IView)
class SiteContainerTreeTable(Table):
    """Site container tree table"""

    @property
    def id(self):
        """Table id getter"""
        manager = get_parent(self.context, ISiteManager)
        return get_table_id(self, manager)

    permission = MANAGE_SITE_PERMISSION
    display_if_empty = True

    can_sort = False

    @property
    def css_classes(self):
        classes = super().css_classes.copy()
        classes.update({
            'tr.selected': lambda item, col, row: 'bg-secondary' if item is self.context else ''
        })
        return classes

    @reify
    def data_attributes(self):
        attributes = super().data_attributes
        intids = get_utility(IIntIds)
        manager = get_parent(self.context, ISiteManager)
        attributes.setdefault('table', {}).update({
            'data-ams-modules': json.dumps({
                'tree': 'tree',
                'content': {
                    'src': get_resource_path(content_js)
                }
            }),
            'data-ams-location': absolute_url(self.context, self.request),
            'data-searching': 'false',
            'data-length-change': 'false',
            'data-info': 'false',
            'data-paging': 'false',
            'data-ams-order': '0,asc',
            'data-ams-visible': json.dumps(IWorkflowPublicationInfo(self.context).is_published()),
            'data-ams-tree-node-id': intids.queryId(manager)
        })
        attributes.setdefault('tr', {}).update({
            'data-ams-location': lambda x, col: absolute_url(x.__parent__, self.request),
            'data-ams-tree-node-id': lambda x, col: intids.queryId(x),
            'data-ams-tree-node-parent-id': lambda x, col: intids.queryId(x.__parent__)
        })
        attributes.setdefault('td', {}).update({
            'data-order': lambda x, col: ':'.join(get_item_order(x))
                if IReorderColumn.providedBy(col) else None
        })
        permission = self.permission
        if self.can_sort and \
                ((not permission) or
                 self.request.has_permission(permission, self.context)):
            attributes['table'].update({
                'data-row-reorder': json.dumps({
                    'update': False
                }),
                'data-ams-reordered': 'MyAMS.tree.sortTree',
                'data-ams-reorder-url': 'set-site-order.json'
            })
            attributes['tr'].update({
                'data-ams-row-value': lambda x, col: x.__name__
            })
        return attributes


@adapter_config(required=(IBaseSiteItem, IAdminLayer, SiteContainerTreeTable),
                provides=IValues)
class SiteContainerTreeTableValues(ContextRequestViewAdapter):
    """Site container tree table values"""

    @property
    def values(self):
        """Site container tree table values getter"""

        def get_values(container, result):
            if container not in result:
                result.append(container)
            if ISiteContainer.providedBy(container) and (container in lineage(self.context)):
                for child in container.values():
                    get_values(child, result)
            return result

        manager = get_parent(self.context, ISiteManager)
        values = []
        for item in manager.values():
            values.append(item)
            if ISiteContainer.providedBy(item):
                get_values(item, values)
        yield from values


@adapter_config(name='reorder',
                required=(IBaseSiteItem, IAdminLayer, SiteContainerTreeTable),
                provides=IColumn)
class SiteContainerTreeReorderColumn(ReorderColumn):
    """Site container tree reorder column"""

    permission = MANAGE_SITE_PERMISSION

    def render_cell(self, item):
        if not self.table.can_sort:
            return ''
        return super().render_cell(item)


@adapter_config(name='visible',
                required=(IBaseSiteItem, IAdminLayer, SiteContainerTreeTable),
                provides=IColumn)
class SiteContainerTreeVisibleColumn(DashboardVisibilityColumn):
    """Site container tree visible column"""


@adapter_config(required=(IBaseSiteItem, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentVisibility)
def site_item_dashboard_visibility(context, request, column):
    """Site item dashboard visibility"""
    info = IWorkflowPublicationInfo(context, None)
    if info is None:
        return False, ''
    if info.is_published():
        icon_class = f"{column.object_data.get('ams-icon-on')}"
    else:
        icon_class = f"{column.object_data.get('ams-icon-off')} text-danger opaque"
    hint = column.get_icon_hint(context)
    return False, f'<i class="fa-fw {icon_class} hint align-base" title="{hint}"></i>'


@adapter_config(name='name',
                required=(IBaseSiteItem, IAdminLayer, SiteContainerTreeTable),
                provides=IColumn)
class SiteContainerTreeNameColumn(DashboardLabelColumn):
    """Site container tree name column"""

    i18n_header = _("Folders contents")
    sortable = 'false'

    css_classes = {
        'td': 'text-truncate'
    }

    def render_head_cell(self):
        return '''<span data-ams-stop-propagation="true"
            data-ams-click-handler="MyAMS.tree.switchTree">
            <span class="small hint" title="{hint}" data-ams-hint-gravity="e">
                <span class="switcher">
                    <i class="far fa-plus-square"></i>
                </span>
            </span>&nbsp;&nbsp;{title}
        </span>'''.format(
            hint=self.request.localizer.translate(_("Click to open/close all folders")),
            title=super().render_head_cell())

    def render_cell(self, item, name=None):
        depth = -3
        for _node in lineage(item):
            depth += 1
        intids = get_utility(IIntIds)
        item_id = intids.queryId(item)
        new_parent = int(self.request.params.get('parent', 0))
        if new_parent == 0:
            parents = map(lambda x: intids.queryId(x), lineage(self.context))
        else:
            parents = map(lambda x: intids.queryId(x), lineage(intids.queryObject(new_parent)))
        translate = self.request.localizer.translate
        expanded = (item is self.context) or (item_id == new_parent) or (item_id in parents)
        return '''<div class="name">
            {padding}
            <span class="small hint tree-switcher" title="{hint}" data-ams-hint-gravity="e" 
                  data-ams-click-handler="MyAMS.tree.switchTreeNode"
                  data-ams-stop-propagation="true">{switch}</span>
            &nbsp;&nbsp;<span class="title">{title}</span> {arrow}
        </div>'''.format(
            padding='<span class="tree-node-padding"></span>' * depth,
            hint=translate(_("Click to show/hide inner folders")),
            switch='<span class="switcher {switch_state}">'
                   '<i class="far fa-{state}-square switch"></i>'
                   '</span>'.format(
                switch_state='expanded' if expanded else '',
                state=getattr(item, '_v_state',
                              'minus' if expanded else 'plus'))
                    if ISiteContainer.providedBy(item) else '',
            title=name or super().render_cell(item),
            arrow='<i class="ml-1 fas fa-share fa-rotate-90 text-muted hint" '
                  '   data-original-title="{title}"></i>'.format(
                title=translate(_("This container automatically redirects navigation to "
                                  "it's first visible content"))) if
                    ISiteContainer.providedBy(item) and
                    (item.navigation_mode == SITE_CONTAINER_REDIRECT_MODE) else '')


@adapter_config(name='content-type',
                required=(IBaseSiteItem, IAdminLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerContentTypeColumn(DashboardContentTypeColumn):
    """Site container content type column"""

    sortable = 'false'


@adapter_config(required=(ISiteElement, IAdminLayer, IDashboardColumn),
                provides=IDashboardContentType)
def site_item_content_type(context, request, column):
    """Site item content type getter"""
    return request.localizer.translate(context.content_name)


@adapter_config(name='sequence',
                required=(IBaseSiteItem, IAdminLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerContentNumberColumn(DashboardContentNumberColumn):
    """Site container content number column"""

    sortable = 'false'


@adapter_config(name='status',
                required=(IBaseSiteItem, IAdminLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerContentStatusColumn(DashboardContentStatusColumn):
    """Site container content status column"""

    sortable = 'false'


@adapter_config(name='status-datetime',
                required=(IBaseSiteItem, IAdminLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerStatusDatetimeColumn(DashboardContentStatusDatetimeColumn):
    """Site container content status datetime column"""

    sortable = 'false'


@adapter_config(name='version',
                required=(IBaseSiteItem, IAdminLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerVersionColumn(DashboardContentVersionColumn):
    """Site container content version column"""

    sortable = 'false'


@adapter_config(name='status-principal',
                required=(IBaseSiteItem, IAdminLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerStatusPrincipalColumn(DashboardContentStatusPrincipalColumn):
    """Site container content status principal column"""

    sortable = 'false'


@adapter_config(name='owner',
                required=(IBaseSiteItem, IAdminLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerOwnerColumn(DashboardContentOwnerColumn):
    """Site container content owner column"""

    sortable = 'false'


@adapter_config(name='timestamp',
                required=(IBaseSiteItem, IAdminLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerTimestampColumn(DashboardContentTimestampColumn):
    """Site container content timestamp column"""

    sortable = 'false'


@adapter_config(name='trash',
                required=(IBaseSiteItem, IPyAMSLayer, ISiteTreeTable),
                provides=IColumn)
class SiteContainerTreeTrashColumn(TrashColumn):
    """Site container tree trash column"""

    hint = _("Delete site item")
    permission = MANAGE_SITE_PERMISSION

    def has_permission(self, item):
        if (item is self.context) or (item in lineage(self.context)):
            return False
        return super().has_permission(item) and item.is_deletable()


@pagelet_config(name='site-tree.html',
                context=IBaseSiteItem, layer=IPyAMSLayer,
                permission=VIEW_SYSTEM_PERMISSION)
@implementer(IDashboardView)
class SiteManagerTreeView(TableAdminView):
    """Site manager tree view"""

    title = _("Site tree")

    table_class = SiteContainerTreeTable
    table_label = _("Site content")

    def __init__(self, context, request, *args, **kwargs):
        super().__init__(context, request, *args, **kwargs)
        self.table.can_sort = ISiteManager.providedBy(context)


@viewlet_config(name='site-tree.menu',
                context=IBaseSiteItem, layer=IAdminLayer,
                manager=ISiteManagementMenu, weight=5,
                permission=VIEW_SYSTEM_PERMISSION)
class SiteManagerTreeMenu(NavigationMenuItem):
    """Site manager tree menu"""

    label = _("Site tree")
    icon_class = 'fas fa-sitemap'
    href = '#site-tree.html'


@view_config(name='get-tree-nodes.json',
             context=ISiteContainer, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION, renderer='json', xhr=True)
def get_tree_nodes(request):
    """Get tree nodes"""
    apply_skin(request, AdminSkin)
    table = SiteContainerTreeTable(request.context, request)
    table.can_sort = json.loads(request.params.get('can_sort', 'false'))
    table.update()
    result = []
    for item in request.context.values():
        row = table.setup_row(item)
        result.append(table.render_row(row).strip())
    return result


@view_config(name='get-tree.json',
             context=IBaseSiteItem, request_type=IPyAMSLayer,
             permission=VIEW_SYSTEM_PERMISSION, renderer='json', xhr=True)
def get_tree(request):
    """Get whole tree nodes"""

    def get_tree_values(parent):
        """Iterator over container tree items"""
        for item in parent.values():
            setattr(item, '_v_state', 'minus')
            yield item
            delattr(item, '_v_state')
            if ISiteContainer.providedBy(item):
                yield from get_tree_values(item)

    apply_skin(request, AdminSkin)
    table = SiteContainerTreeTable(request.context, request)
    table.can_sort = json.loads(request.params.get('can_sort', 'false'))
    table.update()
    result = []
    manager = get_parent(request.context, ISiteManager)
    for item in get_tree_values(manager):
        row = table.setup_row(item)
        result.append(table.render_row(row).strip())
    return result


@view_config(name='set-site-order.json',
             context=IBaseSiteItem, request_type=IPyAMSLayer,
             permission=MANAGE_SITE_PERMISSION, renderer='json', xhr=True)
def set_site_order(request):
    """Set site elements order"""
    apply_skin(request, AdminSkin)
    intids = get_utility(IIntIds)
    action = request.params.get('action')
    parent_oid = int(request.params.get('parent'))
    old_parent = None
    new_parent = intids.queryObject(parent_oid)
    # check for changing parent
    if action == 'reparent':
        child_oid = int(request.params.get('child'))
        child = intids.queryObject(child_oid)
        # check if new parent is not a previous child
        parent_path = IPathElements(new_parent)
        if child_oid in parent_path.parents:
            return {
                'status': 'reload',
                'smallbox': {
                    'status': 'error',
                    'message': request.localizer.translate(_("Can't reparent object to one of "
                                                             "it's children. Reloading...")),
                    'timeout': 5000
                }
            }
        old_parent = child.__parent__
        new_name = old_name = child.__name__
        if old_name in new_parent:
            index = 1
            new_name = '{name}-{index:02}'.format(name=old_name, index=index)
            while new_name in new_parent:
                index += 1
                new_name = '{name}-{index:02}'.format(name=old_name, index=index)
        new_parent[new_name] = child
        del old_parent[old_name]
        request.registry.notify(ObjectMovedEvent(child, old_parent, old_name,
                                                 new_parent, new_name))
    # Re-define order
    if len(new_parent.keys()) > 1:
        names = [
            child.__name__
            for child in [
                intids.queryObject(oid)
                for oid in map(int, json.loads(request.params.get('order')))
            ]
            if (child is not None) and (child.__parent__ is new_parent)
        ]
        if names:
            new_parent.updateOrder(names)
    # get old and new parents children
    table = SiteContainerTreeTable(request.context, request)
    table.can_sort = json.loads(request.params.get('can_sort', 'false'))
    table.update()
    result = []
    items = set()
    parents = [new_parent]
    if action == 'reparent':
        parents.append(old_parent)
    for parent in parents:
        for item in reversed(list(lineage(parent))):
            if ISiteRoot.providedBy(item) or (item in items):
                continue
            if not ISiteManager.providedBy(item):
                setattr(item, '_v_state', 'minus')
                row = table.setup_row(item)
                result.append(table.render_row(row).strip())
                items.add(item)
                delattr(item, '_v_state')
            for child in item.values():
                row = table.setup_row(child)
                result.append(table.render_row(row).strip())
    return result


@view_config(name='switch-visible-item.json',
             context=ISiteContainer, request_type=IPyAMSLayer,
             permission=MANAGE_CONTENT_PERMISSION,
             renderer='json', xhr=True)
def switch_visible_item(request):
    """Switch visible item"""
    result = switch_element_attribute(request)
    if result['status'] == 'success':
        result.pop('status')
        result.pop('message')
        intids = get_utility(IIntIds)
        name = request.params.get('object_name')
        container = request.context
        node_id = intids.queryId(container[name])
        result.setdefault('callbacks', []).append({
            'module': 'content',
            'callback': 'MyAMS.content.tree.switchVisibleElement',
            'options': {
                'node_id': node_id,
                'state': result.pop('state')
            }
        })
    return result


@view_config(name='delete-element.json',
             context=ISiteContainer, request_type=IPyAMSLayer,
             permission=MANAGE_SITE_PERMISSION, renderer='json', xhr=True)
def delete_site_item(request):
    """Delete item from site container"""
    intids = get_utility(IIntIds)
    container = request.context
    name = request.params.get('object_name')
    node_id = intids.queryId(container[name]) if name in container else None
    result = delete_container_element(request, ignore_permission=True)
    if result.get('status') == 'success':
        result.setdefault('callbacks', []).append({
            'module': 'tree',
            'callback': 'MyAMS.tree.deleteElement',
            'options': {
                'node_id': node_id
            }
        })
        result['handle_json'] = True
    return result
