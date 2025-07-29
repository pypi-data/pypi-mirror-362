# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from pyramid.events import subscriber
from zope.component.interfaces import ISite
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from pyams_content.component.paragraph.interfaces import IParagraphFactorySettingsTarget
from pyams_content.component.thesaurus import IThemesManagerTarget
from pyams_content.reference.pictogram.interfaces import IPictogramManagerTarget
from pyams_content.shared.common.manager import SharedTool
from pyams_content.shared.common.types import TypedSharedToolMixin
from pyams_content.shared.resource import IResourceInfo
from pyams_content.shared.resource.interfaces import IResourceManager, RESOURCE_CONTENT_TYPE
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'


@factory_config(IResourceManager)
@implementer(IParagraphFactorySettingsTarget, IThemesManagerTarget, IPictogramManagerTarget)
class ResourceManager(SharedTool, TypedSharedToolMixin):
    """Resource manager class"""
    
    shared_content_type = RESOURCE_CONTENT_TYPE
    
    shared_content_info_factory = IResourceInfo
    
    
@subscriber(IObjectAddedEvent, context_selector=IResourceManager)
def handle_added_resource_manager(event):
    """Register resource manager when added"""
    site = get_parent(event.newParent, ISite)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, IResourceManager)
