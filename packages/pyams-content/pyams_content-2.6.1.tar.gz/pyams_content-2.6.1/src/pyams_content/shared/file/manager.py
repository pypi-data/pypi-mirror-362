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
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from pyams_content.shared.common.manager import SharedTool
from pyams_content.shared.file.interfaces import FILE_CONTENT_TYPE, IFileManager
from pyams_content.shared.logo.interfaces import ILogoManager, LOGO_CONTENT_TYPE
from pyams_utils.factory import factory_config

__docformat__ = 'restructuredtext'

from pyams_utils.traversing import get_parent


@factory_config(IFileManager)
class FileManager(SharedTool):
    """File manager class"""
    
    shared_content_type = FILE_CONTENT_TYPE
    shared_content_menu = False
    
    
@subscriber(IObjectAddedEvent, context_selector=IFileManager)
def handle_added_file_manager(event):
    """Register file manager utility"""
    site = get_parent(event.newParent, ISite)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, IFileManager)
        