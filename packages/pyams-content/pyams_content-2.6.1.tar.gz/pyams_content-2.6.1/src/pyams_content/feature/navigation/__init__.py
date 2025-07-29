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

"""PyAMS_content.feature.navigation module

This module defines base navigation menus components.
"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import alsoProvides
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.association import IAssociationContainer
from pyams_content.component.association.container import AssociationContainer
from pyams_content.component.association.interfaces import ASSOCIATION_CONTAINER_KEY
from pyams_content.component.illustration import ILinkIllustrationTarget
from pyams_content.component.links import IInternalLink
from pyams_content.feature.navigation.interfaces import IDynamicMenu, IMenu, IMenuLinksContainer, \
    IMenuLinksContainerTarget, IMenusContainer, IMenusContainerTarget, MENUS_CONTAINER_KEY, \
    MENU_ICON_CLASS, MENU_ICON_HINT
from pyams_content.reference.pictogram import IPictogramTable
from pyams_content.shared.site.interfaces import ISiteContainer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_sequence.reference import InternalReferenceMixin
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import query_utility
from pyams_utils.request import check_request
from pyams_utils.traversing import get_parent
from pyams_utils.url import canonical_url, relative_url
from pyams_utils.zodb import volatile_property
from pyams_workflow.interfaces import IWorkflowPublicationInfo
from pyams_zmi.interfaces import IAdminLayer


@factory_config(IMenuLinksContainer)
class MenuLinksContainer(AssociationContainer):
    """Menu links container"""


@adapter_config(required=IMenuLinksContainerTarget,
                provides=IMenuLinksContainer)
def menu_links_container_factory(context):
    """Menu links container factory"""
    return get_annotation_adapter(context, ASSOCIATION_CONTAINER_KEY, IMenuLinksContainer,
                                  name='++ass++')


@subscriber(IObjectAddedEvent, parent_selector=IMenuLinksContainer)
def handle_added_navigation_link(event):
    alsoProvides(event.object, ILinkIllustrationTarget)


@factory_config(IMenu)
class Menu(InternalReferenceMixin, Persistent, Contained):
    """Navigation menu"""

    icon_class = MENU_ICON_CLASS
    icon_hint = MENU_ICON_HINT

    visible = FieldProperty(IMenu['visible'])
    title = FieldProperty(IMenu['title'])
    reference = FieldProperty(IMenu['reference'])
    dynamic_menu = FieldProperty(IMenu['dynamic_menu'])
    force_canonical_url = FieldProperty(IMenu['force_canonical_url'])
    _pictogram_name = FieldProperty(IMenu['pictogram_name'])

    @property
    def links(self):
        """Menu links getter"""
        return IMenuLinksContainer(self)

    @property
    def pictogram_name(self):
        """Pictogram name getter"""
        return self._pictogram_name

    @pictogram_name.setter
    def pictogram_name(self, value):
        """Pictogram name setter"""
        if value != self._pictogram_name:
            self._pictogram_name = value
            del self.pictogram

    @volatile_property
    def pictogram(self):
        """Pictogram getter"""
        table = query_utility(IPictogramTable)
        if table is not None:
            return table.get(self._pictogram_name)
        return None

    def is_visible(self, request=None):
        """Menu visibility checker"""
        if not self.reference:
            return True
        target = self.get_target()
        if target is not None:
            publication_info = IWorkflowPublicationInfo(target, None)
            if publication_info is not None:
                return publication_info.is_visible(request)
        return False

    def get_visible_items(self, request=None):
        """Visible items iterator getter"""
        if self.dynamic_menu and ISiteContainer.providedBy(self.target):
            for item in filter(None,
                               map(lambda x: IDynamicMenu(x, None),
                                   self.target.get_visible_items(request))):
                if IInternalLink.providedBy(item):
                    item.force_canonical_url = self.force_canonical_url
                yield item
        yield from IMenuLinksContainer(self).get_visible_items(request)

    def get_url(self, request=None, view_name=None):
        """Target URL getter"""
        target = self.get_target()
        if target is not None:
            if request is None:
                request = check_request()
            if self.force_canonical_url:
                return canonical_url(target, request, view_name=view_name)
            return relative_url(target, request, view_name=view_name)
        return None


@adapter_config(required=IMenu,
                provides=IViewContextPermissionChecker)
class MenuPermissionChecker(ContextAdapter):
    """Menu permission checker"""

    @property
    def edit_permission(self):
        """Edit permission getter"""
        parent = get_parent(self.context, IMenusContainer)
        return IViewContextPermissionChecker(parent).edit_permission


@factory_config(IMenusContainer)
class MenusContainer(AssociationContainer):
    """Associations menus container"""

    def get_visible_items(self, request=None):
        """Visible items iterator"""
        for menu in filter(lambda x: IMenu(x).visible, self.values()):
            if IAdminLayer.providedBy(request) or menu.is_visible(request):
                yield menu


@adapter_config(required=IMenusContainer,
                provides=IViewContextPermissionChecker)
class MenusContainerPermissionChecker(ContextAdapter):
    """Menus container permission checker"""

    @property
    def edit_permission(self):
        """Edit permission getter"""
        parent = get_parent(self.context, IMenusContainerTarget)
        return IViewContextPermissionChecker(parent).edit_permission


@adapter_config(required=IMenusContainerTarget,
                provides=IMenusContainer)
@adapter_config(name='menus',
                required=IMenusContainerTarget,
                provides=IAssociationContainer)
def menus_container_factory(target):
    """Navigation menus container factory"""
    return get_annotation_adapter(target, MENUS_CONTAINER_KEY, IMenusContainer,
                                  name='++ass++menus')
