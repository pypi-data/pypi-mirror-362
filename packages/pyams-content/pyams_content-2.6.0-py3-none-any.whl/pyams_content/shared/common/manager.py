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

"""PyAMS_content.shared.common.manager module

"""

from pyramid.events import subscriber
from zope.component.interfaces import ISite
from zope.container.folder import Folder
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_content.interfaces import MANAGE_TOOL_PERMISSION
from pyams_content.shared.common.interfaces import IBaseSharedTool, ISharedContent, ISharedTool, \
    ISharedToolContainer
from pyams_i18n.content import I18nManagerMixin
from pyams_security.interfaces import IDefaultProtectionPolicy, IViewContextPermissionChecker
from pyams_security.security import ProtectedObjectMixin
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.factory import factory_config, get_object_factory
from pyams_utils.registry import query_utility
from pyams_utils.traversing import get_parent
from pyams_workflow.interfaces import IWorkflow

__docformat__ = 'restructuredtext'


@factory_config(ISharedToolContainer)
class SharedToolContainer(Folder):
    """Shared tools container"""

    title = FieldProperty(ISharedToolContainer['title'])
    short_name = FieldProperty(ISharedToolContainer['short_name'])


@implementer(IDefaultProtectionPolicy, IBaseSharedTool)
class BaseSharedTool(ProtectedObjectMixin, I18nManagerMixin):
    """Base shared tool class"""

    title = FieldProperty(IBaseSharedTool['title'])
    short_name = FieldProperty(IBaseSharedTool['short_name'])

    shared_content_menu = True
    shared_content_workflow = FieldProperty(IBaseSharedTool['shared_content_workflow'])
    inner_folders_mode = FieldProperty(IBaseSharedTool['inner_folders_mode'])


@implementer(ISharedTool)
class SharedTool(Folder, BaseSharedTool):
    """Shared tool class"""

    shared_content_type = None
    '''Shared content type must be defined by subclasses'''

    label = FieldProperty(ISharedTool['label'])
    navigation_label = FieldProperty(ISharedTool['navigation_label'])
    facets_label = FieldProperty(ISharedTool['facets_label'])
    facets_type_label = FieldProperty(ISharedTool['facets_type_label'])
    dashboard_label = FieldProperty(ISharedTool['dashboard_label'])
    

    @property
    def shared_content_factory(self):
        return get_object_factory(ISharedContent, name=self.shared_content_type)


@subscriber(IObjectAddedEvent, context_selector=ISharedTool)
def handle_added_shared_tool(event):
    """Register shared tool after """
    site = get_parent(event.newParent, ISite)
    if site is not None:
        registry = site.getSiteManager()
        if registry is not None:
            tool = event.object
            registry.registerUtility(tool, ISharedTool, name=tool.shared_content_type)


@adapter_config(required=IBaseSharedTool,
                provides=IWorkflow)
def shared_tool_workflow_adapter(context):
    """Shared tool workflow adapter"""
    return query_utility(IWorkflow, name=context.shared_content_workflow)


@adapter_config(required=IBaseSharedTool,
                provides=IViewContextPermissionChecker)
class SharedToolPermissionChecker(ContextAdapter):
    """Shared tool permission checker"""

    edit_permission = MANAGE_TOOL_PERMISSION
