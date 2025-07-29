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

"""PyAMS_content.shared.view.manager module

This module defines views manager shared tool.
"""

from pyramid.events import subscriber
from zope.component.interfaces import ISite
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from pyams_content.shared.common.manager import SharedTool
from pyams_content.shared.view.interfaces import IViewManager, VIEW_CONTENT_TYPE
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'


@factory_config(IViewManager)
class ViewManager(SharedTool):
    """View manager class"""

    shared_content_type = VIEW_CONTENT_TYPE
    shared_content_menu = False


@subscriber(IObjectAddedEvent, context_selector=IViewManager)
def handle_added_view_manager(event):
    """Register view manager when added"""
    site = get_parent(event.newParent, ISite)
    registry = site.getSiteManager()
    if registry is not None:
        registry.registerUtility(event.object, IViewManager)
