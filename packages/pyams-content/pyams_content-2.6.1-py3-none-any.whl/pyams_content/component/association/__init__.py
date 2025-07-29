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

"""PyAMS_content.component.association module

Associations are components which are used to associate elements to a given context.
These *elements* can be internal or external links, external files...
"""

from persistent import Persistent
from pyramid.events import subscriber
from zope.container.contained import Contained
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent, \
    ObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.component.association.interfaces import IAssociationContainer, \
    IAssociationContainerTarget, IAssociationItem
from pyams_content.shared.common import IWfSharedContent
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import get_pyramid_registry
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_workflow.content import HiddenContentPublicationInfo
from pyams_workflow.interfaces import IWorkflowPublicationInfo

__docformat__ = 'restructuredtext'


@implementer(IAssociationItem)
class AssociationItem(Persistent, Contained):
    """Base association item persistent class"""

    icon_class = ''
    icon_hint = ''

    visible = FieldProperty(IAssociationItem['visible'])

    def is_visible(self, request=None):
        """Visibility getter"""
        return self.visible

    def get_url(self, request=None, view_name=None):
        """URL getter"""
        return absolute_url(self, request, view_name)


@adapter_config(required=IAssociationItem,
                provides=IViewContextPermissionChecker)
@adapter_config(required=IAssociationContainer,
                provides=IViewContextPermissionChecker)
class AssociationPermissionChecker(ContextAdapter):
    """Association permission checker"""

    @property
    def edit_permission(self):
        """Edit permission getter"""
        parent = get_parent(self.context, IAssociationContainerTarget)
        if parent is not None:
            return IViewContextPermissionChecker(parent).edit_permission
        return None


@subscriber(IObjectAddedEvent, context_selector=IAssociationItem)
@subscriber(IObjectModifiedEvent, context_selector=IAssociationItem)
@subscriber(IObjectRemovedEvent, context_selector=IAssociationItem)
def handle_association_event(event):
    """Handle added association item"""
    target = get_parent(event.object, IAssociationContainerTarget)
    if target is not None:
        get_pyramid_registry().notify(ObjectModifiedEvent(target))
    content = get_parent(target if target is not None else event.object, IWfSharedContent)
    if content is not None:
        get_pyramid_registry().notify(ObjectModifiedEvent(content))


@adapter_config(required=IAssociationItem,
                provides=IWorkflowPublicationInfo)
def association_item_publication_info(context):
    """Association item publication info"""
    if not context.visible:
        return HiddenContentPublicationInfo()
    return None
